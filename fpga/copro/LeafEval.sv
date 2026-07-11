// Dr. Mario depth-3 LEAF EVAL accelerator. Computes the full endgame leaf
// (shape + spawn + setup + buried + readiness_ext + vrdy + pollution + combine)
// over a 128-bcell board in ~1.5-4k clocks -- replaces ~50k cycles of 6502 walks.
//
// Cell encoding (written by the host/copro): 0 = empty, else {vir, color[1:0]}
// with color 1..3 (NES low nibble + 1). Interface:
//   write board[i]  : wr=1, waddr=i (0..127), wdata[2:0]
//   start           : pulse start=1 (loads nothing; board regs already written)
//   done            : high when finished; sco[15:0] (signed) & win valid
// Bit-exact contract (validated vs the python goldens in tb_leafeval):
//   sco = 5000 - 12*maxh - 20*holes - 90*toprisk - 150*spawn + 60*setup
//         - 30*buried + 12*rdy_ext + 12*vrdy - 6*pollution   (16-bit wrap)
//   win = (no virus on board)
module LeafEval(
	input             clk,
	input             rst,
	input             wr,
	input       [6:0] waddr,
	input       [2:0] wdata,
	input             start,
	output reg        done,
	output reg [15:0] sco,
	output reg        win
);

// board register file: 128 x {vir, color[1:0]}
reg [2:0] bcell [0:127];
always @(posedge clk) if (wr) bcell[waddr] <= wdata;

wire [1:0] col_of  [0:127];
wire       occ_of  [0:127];
wire       vir_of  [0:127];
genvar gi;
generate for (gi = 0; gi < 128; gi = gi + 1) begin : g
	assign col_of[gi] = bcell[gi][1:0];
	assign occ_of[gi] = bcell[gi][1:0] != 2'd0;
	assign vir_of[gi] = bcell[gi][2] && bcell[gi][1:0] != 2'd0;
end endgenerate

// squares 0..16
function [8:0] sq(input [4:0] n);
	sq = n * n;
endfunction

// ------------------------------------------------------------------ FSM
localparam S_IDLE=0, S_COLWALK=1, S_VNEXT=2, S_HRUN_L=3, S_HSPAN_L=4, S_HRUN_R=5,
           S_HSPAN_R=6, S_VRUN_U=7, S_VSPAN_U=8, S_VRUN_D=9, S_VSPAN_D=10,
           S_POLROW=11, S_POLCOL=12, S_VFIN=13, S_SETUP_H=14, S_SETUP_V=15, S_DONE=16;
reg [4:0] st;

reg  [3:0] wc, wr_;            // column/row walk indices
reg  [4:0] maxh /*verilator public_flat_rd*/;
reg  [7:0] holes /*verilator public_flat_rd*/, toprisk /*verilator public_flat_rd*/, spawn /*verilator public_flat_rd*/, setup /*verilator public_flat_rd*/;
reg [10:0] pollution /*verilator public_flat_rd*/;   // up to 48 viruses x 22 cells = 1056
reg  [9:0] buried /*verilator public_flat_rd*/;   // up to 48 x 15 = 720
reg [15:0] rdy_ext /*verilator public_flat_rd*/, vrdy /*verilator public_flat_rd*/;
reg        anyvir;
reg        seen;               // column walk: first-occupied seen
reg  [4:0] fillcnt;            // filled-so-far in this column (for buried)

reg  [6:0] vo;                 // current virus bcell offset
wire [3:0] v_r = vo[6:3];
wire [2:0] v_c = vo[2:0];
wire [1:0] v_col = col_of[vo];

reg  [4:0] run_h, run_v;       // same-color runs through the virus
reg  [4:0] p;                  // walk pointer (row 0..15 or col 0..7 as needed)
reg  [4:0] span_lo, span_hi;   // span bounds (exclusive), horizontal: -1..8 as 5-bit signed-ish
reg  [4:0] vspan_lo, vspan_hi;

wire signed [17:0] rdy_h_sq = (span_hi - span_lo - 1 >= 4) ? sq(run_h) : 9'd0;
// (assigned in-state below; wire above only for readability of the gate)

integer i;

always @(posedge clk) begin
	if (rst) begin
		st <= S_IDLE; done <= 1'b0;
	end else begin
		case (st)
		S_IDLE: if (start) begin
			maxh <= 0; holes <= 0; toprisk <= 0; spawn <= 0; setup <= 0;
			pollution <= 0; buried <= 0; rdy_ext <= 0; vrdy <= 0; anyvir <= 0;
			wc <= 0; wr_ <= 0; seen <= 0; fillcnt <= 0;
			done <= 1'b0;
			st <= S_COLWALK;
		end

		// ---- one bcell per cycle, column-major: shape + buried + toprisk + spawn + anyvir
		S_COLWALK: begin
			if (occ_of[{wr_[3:0], wc[2:0]}]) begin
				if (!seen) begin
					seen <= 1'b1;
					if (5'd16 - wr_ > maxh) maxh <= 5'd16 - wr_;
				end
				if (vir_of[{wr_[3:0], wc[2:0]}]) begin
					anyvir <= 1'b1;
					buried <= buried + fillcnt;
				end
				fillcnt <= fillcnt + 1'b1;
				if (wr_ < 3) toprisk <= toprisk + 1'b1;
				if (wr_ < 4 && (wc == 3 || wc == 4)) spawn <= spawn + 1'b1;
			end else if (seen)
				holes <= holes + 1'b1;
			// advance row-major within the column
			if (wr_ == 4'd15) begin
				wr_ <= 0; seen <= 0; fillcnt <= 0;
				if (wc == 3'd7) begin
					vo <= 0; st <= S_VNEXT;
				end else
					wc <= wc + 1'b1;
			end else
				wr_ <= wr_ + 1'b1;
		end

		// ---- per-virus terms: iterate all cells, process viruses
		S_VNEXT: begin
			if (vir_of[vo]) begin
				run_h <= 1; run_v <= 1;
				p <= {2'b0, v_c};      // horizontal left walk from c-1
				st <= S_HRUN_L;
			end else if (vo == 7'd127) begin
				wc <= 0; wr_ <= 0; st <= S_SETUP_H;
			end else
				vo <= vo + 1'b1;
		end

		// horizontal: same-color run leftwards, then span leftwards
		S_HRUN_L: begin
			if (p != 0 && col_of[{v_r, p[2:0] - 3'd1}] == v_col && occ_of[{v_r, p[2:0]-3'd1}]) begin
				run_h <= run_h + 1'b1; p <= p - 1'b1;
			end else begin
				span_lo <= p; st <= S_HSPAN_L;    // continue span from p-1 downward
			end
		end
		S_HSPAN_L: begin
			if (span_lo != 0 &&
			    (!occ_of[{v_r, span_lo[2:0] - 3'd1}] || col_of[{v_r, span_lo[2:0] - 3'd1}] == v_col))
				span_lo <= span_lo - 1'b1;
			else begin
				p <= {2'b0, v_c}; st <= S_HRUN_R;
			end
		end
		S_HRUN_R: begin
			if (p != 5'd7 && occ_of[{v_r, p[2:0] + 3'd1}] && col_of[{v_r, p[2:0] + 3'd1}] == v_col) begin
				run_h <= run_h + 1'b1; p <= p + 1'b1;
			end else begin
				span_hi <= p; st <= S_HSPAN_R;
			end
		end
		S_HSPAN_R: begin
			if (span_hi != 5'd7 &&
			    (!occ_of[{v_r, span_hi[2:0] + 3'd1}] || col_of[{v_r, span_hi[2:0] + 3'd1}] == v_col))
				span_hi <= span_hi + 1'b1;
			else begin
				p <= {1'b0, v_r}; st <= S_VRUN_U;
			end
		end

		// vertical: run up, span up, run down, span down
		S_VRUN_U: begin
			if (p != 0 && occ_of[{p[3:0] - 4'd1, v_c}] && col_of[{p[3:0] - 4'd1, v_c}] == v_col) begin
				run_v <= run_v + 1'b1; p <= p - 1'b1;
			end else begin
				vspan_lo <= p; st <= S_VSPAN_U;
			end
		end
		S_VSPAN_U: begin
			if (vspan_lo != 0 &&
			    (!occ_of[{vspan_lo[3:0] - 4'd1, v_c}] || col_of[{vspan_lo[3:0] - 4'd1, v_c}] == v_col))
				vspan_lo <= vspan_lo - 1'b1;
			else begin
				p <= {1'b0, v_r}; st <= S_VRUN_D;
			end
		end
		S_VRUN_D: begin
			if (p != 5'd15 && occ_of[{p[3:0] + 4'd1, v_c}] && col_of[{p[3:0] + 4'd1, v_c}] == v_col) begin
				run_v <= run_v + 1'b1; p <= p + 1'b1;
			end else begin
				vspan_hi <= p; st <= S_VSPAN_D;
			end
		end
		S_VSPAN_D: begin
			if (vspan_hi != 5'd15 &&
			    (!occ_of[{vspan_hi[3:0] + 4'd1, v_c}] || col_of[{vspan_hi[3:0] + 4'd1, v_c}] == v_col))
				vspan_hi <= vspan_hi + 1'b1;
			else begin
				p <= 0; st <= S_POLROW;
			end
		end

		// pollution: differently-colored NON-virus occupied cells in row then column
		S_POLROW: begin
			if (p[2:0] != v_c && occ_of[{v_r, p[2:0]}] && !vir_of[{v_r, p[2:0]}]
			    && col_of[{v_r, p[2:0]}] != v_col)
				pollution <= pollution + 1'b1;
			if (p == 5'd7) begin p <= 0; st <= S_POLCOL; end
			else p <= p + 1'b1;
		end
		S_POLCOL: begin
			if (p[3:0] != v_r && occ_of[{p[3:0], v_c}] && !vir_of[{p[3:0], v_c}]
			    && col_of[{p[3:0], v_c}] != v_col)
				pollution <= pollution + 1'b1;
			if (p == 5'd15) st <= S_VFIN;
			else p <= p + 1'b1;
		end

		S_VFIN: begin
			// readiness_ext: max(run^2 per direction, gated on span >= 4)
			begin : fin
				reg [8:0] hq, vq, mx;
				// python gates on (hi - lo - 1) >= 4 with EXCLUSIVE blocker endpoints;
				// span_lo/hi here are INCLUSIVE span cells -> width = hi - lo + 1.
				hq = ((span_hi  - span_lo  + 5'd1) >= 5'd4) ? sq(run_h) : 9'd0;
				vq = ((vspan_hi - vspan_lo + 5'd1) >= 5'd4) ? sq(run_v) : 9'd0;
				mx = (hq > vq) ? hq : vq;
				rdy_ext <= rdy_ext + mx;
				vrdy    <= vrdy + sq(run_v);
			end
			if (vo == 7'd127) begin
				wc <= 0; wr_ <= 0; st <= S_SETUP_H;
			end else begin
				vo <= vo + 1'b1; st <= S_VNEXT;
			end
		end

		// ---- setup: 3-in-a-row same color touching a same-color virus (win extendable)
		// horizontal windows: rows 0..15, i 0..5 ; vertical: cols 0..7, i 0..13
		S_SETUP_H: begin : suh
			reg [1:0] c0;
			reg t;
			c0 = col_of[{wr_[3:0], wc[2:0]}];
			if (c0 != 0 && col_of[{wr_[3:0], wc[2:0] + 3'd1}] == c0
			            && col_of[{wr_[3:0], wc[2:0] + 3'd2}] == c0) begin
				t = (vir_of[{wr_[3:0], wc[2:0]}]        && col_of[{wr_[3:0], wc[2:0]}] == c0)
				  || (vir_of[{wr_[3:0], wc[2:0] + 3'd1}] && col_of[{wr_[3:0], wc[2:0] + 3'd1}] == c0)
				  || (vir_of[{wr_[3:0], wc[2:0] + 3'd2}] && col_of[{wr_[3:0], wc[2:0] + 3'd2}] == c0);
				if (!t && wc != 0)
					t = vir_of[{wr_[3:0], wc[2:0] - 3'd1}] && col_of[{wr_[3:0], wc[2:0] - 3'd1}] == c0;
				if (!t && wc < 3'd5)
					t = vir_of[{wr_[3:0], wc[2:0] + 3'd3}] && col_of[{wr_[3:0], wc[2:0] + 3'd3}] == c0;
				if (t) setup <= setup + 1'b1;
			end
			if (wc == 3'd5) begin
				wc <= 0;
				if (wr_ == 4'd15) begin wr_ <= 0; st <= S_SETUP_V; end
				else wr_ <= wr_ + 1'b1;
			end else
				wc <= wc + 1'b1;
		end
		S_SETUP_V: begin : suv
			reg [1:0] c0;
			reg t;
			c0 = col_of[{wr_[3:0], wc[2:0]}];
			if (c0 != 0 && col_of[{wr_[3:0] + 4'd1, wc[2:0]}] == c0
			            && col_of[{wr_[3:0] + 4'd2, wc[2:0]}] == c0) begin
				t = (vir_of[{wr_[3:0], wc[2:0]}]         && col_of[{wr_[3:0], wc[2:0]}] == c0)
				  || (vir_of[{wr_[3:0] + 4'd1, wc[2:0]}] && col_of[{wr_[3:0] + 4'd1, wc[2:0]}] == c0)
				  || (vir_of[{wr_[3:0] + 4'd2, wc[2:0]}] && col_of[{wr_[3:0] + 4'd2, wc[2:0]}] == c0);
				if (!t && wr_ != 0)
					t = vir_of[{wr_[3:0] - 4'd1, wc[2:0]}] && col_of[{wr_[3:0] - 4'd1, wc[2:0]}] == c0;
				if (!t && wr_ < 4'd13)
					t = vir_of[{wr_[3:0] + 4'd3, wc[2:0]}] && col_of[{wr_[3:0] + 4'd3, wc[2:0]}] == c0;
				if (t) setup <= setup + 1'b1;
			end
			if (wr_ == 4'd13) begin
				wr_ <= 0;
				if (wc == 3'd7) st <= S_DONE;
				else wc <= wc + 1'b1;
			end else
				wr_ <= wr_ + 1'b1;
		end

		S_DONE: begin
			// combine (16-bit wrap semantics, same as the 6502)
			sco <= 16'd5000
			     - 16'd12  * maxh
			     - 16'd20  * holes
			     - 16'd90  * toprisk
			     - 16'd150 * spawn
			     + 16'd60  * setup
			     - 16'd30  * buried
			     + 16'd12  * rdy_ext
			     + 16'd12  * vrdy
			     - 16'd6   * pollution;
			win  <= !anyvir;
			done <= 1'b1;
			st <= S_IDLE;
		end
		default: st <= S_IDLE;
		endcase
	end
end

endmodule

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
//         - 30*buried + 12*rdy_ext + 24*vrdy - 6*pollution + matched60   (16-bit wrap; buried color-aware + nearest-2 cap, R6 matched-cover pre-scaled)
//   win = (no virus on board)
module LeafEval(
	input             clk,
	input             rst,
	input             wr,          // board-window write into slot `wslot`
	input       [6:0] waddr,
	input       [2:0] wdata,
	input       [1:0] wslot,       // 0=CUR 1=LIVE 2=WORK1 3=WORK2
	input             start,       // legacy: LEAF on CUR
	input       [3:0] cmd,         // 1=LEAF 2=CUR<-slot(a_sl) 3=slot(a_sl)<-CUR
	                               // 4=NODE(land+place+resolve+leaf) 5=LAND_RESOLVE (no leaf)
	input             cmd_go,
	input       [1:0] a_sl,        // slot argument for copies
	input       [1:0] a_o4,        // orient4 (0..3)
	input       [2:0] a_col,       // column 0..7
	input       [1:0] a_ca,        // colors, ENGINE encoding 1..3 handled by wrapper (pass nibble+1)
	input       [1:0] a_cb,
	output reg        done,
	output reg [15:0] sco,
	output reg        win,
	output reg        legal,
	output reg  [5:0] rv_cells,
	output reg  [3:0] rv_vir,
	output reg [15:0] imm
);

// CUR as registers (the eval/scan walks index it combinationally); the 3 snapshot
// slots in ONE inferred BRAM (sequential access only: window writes + 130-cyc copies)
// -- 3 register files didn't fit the device (fitter: 4246/4191 LABs).
reg [2:0] bcell [0:127] /*verilator public_flat_rd*/;
// snapshot slots in an EXPLICIT dpram (behavioral arrays fail BRAM inference in
// Quartus Std -> got synthesized as 1.5k registers and blew the LAB budget).
// port A = writes (host window / copy-out walk), port B = registered reads (copy-in).
reg  [8:0] sr_addr;
reg  [6:0] cpw_p;
wire [8:0] sr_waddr = {wslot, waddr};
wire       sl_we    = (wr && wslot != 2'd0) || sl_cpw;
reg        sl_cpw;                    // S_CP_W write strobe
wire [8:0] sl_wa    = sl_cpw ? {a_sl, cpw_p} : sr_waddr;
wire [7:0] sl_wd    = sl_cpw ? {5'd0, bcell[cpw_p]} : {5'd0, wdata};
wire [7:0] sl_qb;
wire [2:0] slotq = sl_qb[2:0];
dpram #(.widthad_a(9), .width_a(8)) slotram (
	.clock_a  (clk),
	.address_a(sl_wa),
	.data_a   (sl_wd),
	.wren_a   (sl_we),
	.q_a      (),
	.clock_b  (clk),
	.address_b(sr_addr),
	.data_b   (8'd0),
	.wren_b   (1'b0),
	.q_b      (sl_qb)
);

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
           S_POLROW=11, S_POLCOL=12, S_VFIN=13, S_SETUP_H=14, S_SETUP_V=15, S_DONE=16,
           S_COPY=17, S_FO1=18, S_FO2=19, S_PLACE=20, S_SCAN=21, S_EOL=22,
           S_APPLY=23, S_GRAV=24, S_RESDONE=25, S_CP_R=26, S_CP_W=27, S_CP_P=28, S_DONE2=29;
reg [3:0] cmd_l;
reg [4:0] st;
reg       node_leaf;           // CMD_NODE: run the leaf after resolve
// land/resolve working regs
reg [4:0]   fo1, fo2, fwp;     // first-occ results + walk pointer
reg [6:0]   off_a, off_b;      // placed cell offsets
reg [127:0] markb;             // targeted-clear mark bits
reg [1:0]   li;                // scan line index 0..3
reg [7:0]   soff;              // scan offset
reg [3:0]   sstep;             // scan step (1 or 8)
reg [4:0]   scnt;              // cells left in line
reg [4:0]   srun;              // current run length
reg [1:0]   smcol;             // current run color (0 = none)
reg [7:0]   srstart;           // run start offset
reg [6:0]   fwp2;              // apply sweep pointer 0..127
reg [4:0]   gdest;             // gravity dest row
reg         anyclear;

reg  [3:0] wc, wr_;            // column/row walk indices
reg  [4:0] maxh /*verilator public_flat_rd*/;
reg  [7:0] holes /*verilator public_flat_rd*/, toprisk /*verilator public_flat_rd*/, spawn /*verilator public_flat_rd*/, setup /*verilator public_flat_rd*/;
reg [10:0] pollution /*verilator public_flat_rd*/;   // up to 48 viruses x 22 cells = 1056
reg  [9:0] buried /*verilator public_flat_rd*/;   // up to 48 x 15 = 720
reg [12:0] matched60 /*verilator public_flat_rd*/; // R6 matched-cover pre-scaled: +60 per virus w/ same-color cover directly on top
reg [15:0] rdy_ext /*verilator public_flat_rd*/, vrdy /*verilator public_flat_rd*/;
reg        anyvir;
reg        seen;               // column walk: first-occupied seen
reg  [4:0] fillcnt;            // filled-so-far in this column (for buried)
reg  [1:0] curcol;            // R1 color-aware buried: color of the contiguous same-color
reg  [4:0] curlen;            // non-virus cover run ending at the previous cell (0 = none)
reg  [4:0] vseen;             // R7b: viruses seen so far this column (buried charge caps at 2)
// combine-pipeline: registered multiplier inputs (S_DONE stage1) -> combine in S_DONE2
reg  [4:0] maxh_p; reg [7:0] holes_p, toprisk_p, spawn_p, setup_p;
reg [10:0] pollution_p; reg [9:0] buried_p; reg [15:0] rdy_ext_p, vrdy_p; reg [12:0] matched60_p;

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
		st <= S_IDLE; done <= 1'b0; sl_cpw <= 1'b0;
	end else begin
		if (wr && wslot == 2'd0) bcell[waddr] <= wdata;   // slot writes go via the dpram port
		case (st)
		S_IDLE: if (start || cmd_go) begin
			done <= 1'b0;
			if (start || cmd == 4'd1) begin                      // LEAF on CUR
				maxh <= 0; holes <= 0; toprisk <= 0; spawn <= 0; setup <= 0;
				pollution <= 0; buried <= 0; rdy_ext <= 0; vrdy <= 0; anyvir <= 0; matched60 <= 13'd0;
				wc <= 0; wr_ <= 0; seen <= 0; fillcnt <= 0; curcol <= 2'd0; curlen <= 5'd0; vseen <= 5'd0;
				st <= S_COLWALK;
			end else if (cmd == 4'd2 || cmd == 4'd3) begin       // slot copies
				cmd_l <= cmd; st <= S_COPY;
			end
			else if (cmd == 4'd4) begin                          // NODE: land+place+resolve+leaf
				node_leaf <= 1'b1;
				legal <= 1'b0; rv_cells <= 0; rv_vir <= 0; imm <= 0;
				markb <= 128'd0; anyclear <= 1'b0;
				fwp <= 0;
				st <= S_FO1;
			end
		end

		// copy CUR <- slot: pipelined BRAM read (addr set cycle N, data cycle N+1)
		S_COPY: begin
			fwp2 <= 0; cpw_p <= 0;
			sr_addr <= {a_sl, 7'd0};
			if (cmd_l == 4'd2) st <= S_CP_P;
			else begin sl_cpw <= 1'b1; st <= S_CP_W; end
		end
		S_CP_P: begin                             // prime: cell 0 lands in slotq next cycle
			sr_addr <= sr_addr + 1'b1;
			st <= S_CP_R;
		end
		S_CP_R: begin
			bcell[fwp2] <= slotq;                 // slotq = cell fwp2
			sr_addr <= sr_addr + 1'b1;
			if (fwp2 == 7'd127) begin done <= 1'b1; st <= S_IDLE; end
			else fwp2 <= fwp2 + 1'b1;
		end
		// copy slot <- CUR: drive the dpram write port, 128 cycles
		S_CP_W: begin
			if (cpw_p == 7'd127) begin sl_cpw <= 1'b0; done <= 1'b1; st <= S_IDLE; end
			else cpw_p <= cpw_p + 1'b1;
		end

		// ---- landing: first_occ walks (col, then col+1 for horizontal) ----
		S_FO1: begin
			if (fwp == 5'd16 || occ_of[{fwp[3:0], a_col}]) begin
				fo1 <= fwp; fwp <= 0;
				if (a_o4[1]) begin                               // horizontal
					if (a_col == 3'd7) begin done <= 1'b1; st <= S_IDLE; end  // illegal (legal=0)
					else st <= S_FO2;
				end else begin                                   // vertical: legal iff fo>=2
					if (fwp >= 5'd2) begin
						off_b <= {fwp[3:0] - 4'd1, a_col};
						off_a <= {fwp[3:0] - 4'd2, a_col};
						legal <= 1'b1; st <= S_PLACE;
					end else begin done <= 1'b1; st <= S_IDLE; end
				end
			end else
				fwp <= fwp + 1'b1;
		end
		S_FO2: begin
			if (fwp == 5'd16 || occ_of[{fwp[3:0], a_col + 3'd1}]) begin : fo2b
				reg [4:0] fom;
				fom = (fo1 < fwp) ? fo1 : fwp;
				if (fom >= 5'd1) begin
					off_a <= {fom[3:0] - 4'd1, a_col};
					off_b <= {fom[3:0] - 4'd1, a_col + 3'd1};
					legal <= 1'b1; st <= S_PLACE;
				end else begin done <= 1'b1; st <= S_IDLE; end
			end else
				fwp <= fwp + 1'b1;
		end
		S_PLACE: begin
			// orient4 odd = color swap (B goes to offa/top/left)
			bcell[off_a] <= {1'b0, a_o4[0] ? a_cb : a_ca};
			bcell[off_b] <= {1'b0, a_o4[0] ? a_ca : a_cb};
			li <= 0; st <= S_SCAN;
			// initialize line 0 (row of off_a)
			soff <= {1'b0, off_a[6:3], 3'd0}; sstep <= 4'd1; scnt <= 5'd8;
			srun <= 0; smcol <= 0;
		end

		// ---- targeted find-clears: 4 lines (rowA, colA, rowB, colB) ----
		// One cell per cycle; a completed run >= 4 marks its cells COMBINATIONALLY
		// (16 conditional bit-sets along the stride) -- no flush sub-state, no re-scan.
		S_SCAN: begin : scan
			reg brk;      // run break at this cell (empty or color change)
			reg [1:0] c_;
			c_  = col_of[soff[6:0]];
			brk = (c_ == 2'd0) || (c_ != smcol);
			if (brk && srun >= 5'd4)
				for (i = 0; i < 16; i = i + 1)
					if (i < srun) markb[srstart[6:0] + i * sstep] <= 1'b1;
			if (c_ == 2'd0) begin
				srun <= 0; smcol <= 0;
			end else if (c_ != smcol) begin
				smcol <= c_; srstart <= soff; srun <= 5'd1;
			end else
				srun <= srun + 1'b1;
			if (scnt == 5'd1)
				st <= S_EOL;
			else begin
				soff <= soff + {4'd0, sstep};
				scnt <= scnt - 1'b1;
			end
		end
		S_EOL: begin
			if (srun >= 5'd4)
				for (i = 0; i < 16; i = i + 1)
					if (i < srun) markb[srstart[6:0] + i * sstep] <= 1'b1;
			srun <= 0; smcol <= 0;
			case (li)
				2'd0: begin soff <= {5'd0, off_a[2:0]}; sstep <= 4'd8; scnt <= 5'd16; li <= 2'd1; st <= S_SCAN; end
				2'd1: begin soff <= {1'b0, off_b[6:3], 3'd0}; sstep <= 4'd1; scnt <= 5'd8; li <= 2'd2; st <= S_SCAN; end
				2'd2: begin soff <= {5'd0, off_b[2:0]}; sstep <= 4'd8; scnt <= 5'd16; li <= 2'd3; st <= S_SCAN; end
				default: begin fwp2 <= 0; st <= S_APPLY; end
			endcase
		end

		S_APPLY: begin : apl
			if (markb[fwp2]) begin
				rv_cells <= rv_cells + 1'b1;
				if (vir_of[fwp2]) rv_vir <= rv_vir + 1'b1;
				bcell[fwp2] <= 3'd0;
				anyclear <= 1'b1;
			end
			if (fwp2 == 7'd127) begin
				wc <= 0; gdest <= 5'd15; fwp <= 5'd15;   // gravity: col wc, read row fwp
				st <= (anyclear || markb[7'd127]) ? S_GRAV : S_RESDONE;
			end else
				fwp2 <= fwp2 + 1'b1;
		end

		// gravity: per column bottom-up; viruses anchor (dest = read-1); pills fall to dest
		S_GRAV: begin : grv
			reg [2:0] t;
			t = bcell[{fwp[3:0], wc[2:0]}];
			if (t != 3'd0) begin
				if (t[2]) begin                       // virus: fixed anchor
					gdest <= fwp - 1'b1;
				end else begin
					if (gdest != fwp) begin
						bcell[{gdest[3:0], wc[2:0]}] <= t;
						bcell[{fwp[3:0], wc[2:0]}] <= 3'd0;
					end
					gdest <= gdest - 1'b1;
				end
			end
			if (fwp == 5'd0) begin
				if (wc == 3'd7) st <= S_RESDONE;
				else begin wc <= wc + 1'b1; gdest <= 5'd15; fwp <= 5'd15; end
			end else
				fwp <= fwp - 1'b1;
		end

		S_RESDONE: begin
			imm <= 16'd180 * rv_vir + 16'd10 * rv_cells;
			if (node_leaf) begin
				maxh <= 0; holes <= 0; toprisk <= 0; spawn <= 0; setup <= 0;
				pollution <= 0; buried <= 0; rdy_ext <= 0; vrdy <= 0; anyvir <= 0; matched60 <= 13'd0;
				wc <= 0; wr_ <= 0; seen <= 0; fillcnt <= 0; curcol <= 2'd0; curlen <= 5'd0; vseen <= 5'd0;
				st <= S_COLWALK;
			end else begin
				done <= 1'b1; st <= S_IDLE;
			end
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
					// R6 matched-cover setup: a same-color non-virus cell resting directly on the virus
					// (== the R1 exemption condition) counts a started vertical clear.
					if (curcol == col_of[{wr_[3:0], wc[2:0]}]) matched60 <= matched60 + 13'd60;
					// R1 color-aware buried; R7b: charge only the 2 topmost viruses in the column.
					if (vseen < 5'd2)
						buried <= buried + fillcnt - ((curcol == col_of[{wr_[3:0], wc[2:0]}]) ? curlen : 5'd0);
					vseen <= vseen + 1'b1;
					curcol <= 2'd0; curlen <= 5'd0;                 // virus breaks the cover run
				end else begin                                     // occupied non-virus: extend/restart run
					if (curcol == col_of[{wr_[3:0], wc[2:0]}])
						curlen <= curlen + 1'b1;
					else begin
						curcol <= col_of[{wr_[3:0], wc[2:0]}]; curlen <= 5'd1;
					end
				end
				fillcnt <= fillcnt + 1'b1;
				if (wr_ < 3) toprisk <= toprisk + 1'b1;
				if (wr_ < 4 && (wc == 3 || wc == 4)) spawn <= spawn + 1'b1;
			end else begin
				if (seen) holes <= holes + 1'b1;
				curcol <= 2'd0; curlen <= 5'd0;                    // empty cell breaks the cover run
			end
			// advance row-major within the column
			if (wr_ == 4'd15) begin
				wr_ <= 0; seen <= 0; fillcnt <= 0; curcol <= 2'd0; curlen <= 5'd0; vseen <= 5'd0;
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

		S_DONE: begin       // stage 1: register combine (multiplier) inputs near the DSPs
			maxh_p <= maxh; holes_p <= holes; toprisk_p <= toprisk; spawn_p <= spawn; setup_p <= setup;
			pollution_p <= pollution; buried_p <= buried; rdy_ext_p <= rdy_ext; vrdy_p <= vrdy; matched60_p <= matched60;
			win  <= !anyvir;
			st <= S_DONE2;
		end
		S_DONE2: begin      // stage 2: combine from registered inputs (same sco, +1 leaf cycle)
			sco <= 16'd5000
			     - 16'd12  * maxh_p
			     - 16'd20  * holes_p
			     - 16'd90  * toprisk_p
			     - 16'd150 * spawn_p
			     + 16'd60  * setup_p
			     + matched60_p
			     - 16'd30  * buried_p
			     + 16'd12  * rdy_ext_p
			     + 16'd24  * vrdy_p
			     - 16'd6   * pollution_p;
			done <= 1'b1;
			st <= S_IDLE;
		end
		default: st <= S_IDLE;
		endcase
	end
end

endmodule

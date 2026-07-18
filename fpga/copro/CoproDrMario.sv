// rebuild-tag: BoardEngine dpram-slots (fit fix) 2026-07-11e
// Dr. Mario depth-2 AI coprocessor (mapper 100 = MMC1 banking + this block).
// A second 6502 (Arlet core, renamed copro6502) free-runs at the core master clock
// (~85.9 MHz vs the game CPU's 1.79 MHz) computing the depth-2 pill placement.
//
// Memory (BRAM-friendly: 4KB TDP work RAM + 16KB SP ROM, not a flat 64KB):
//   copro $0000-$0FFF -> wram[0x000+a[11:0]]   (zp/stack/boards/mark)
//   copro $6100-$61FF -> wram[0x800+a[7:0]]    (search state, DONE=$61FF)
//   copro $8000-$BFFF -> rom[a[13:0]]          (firmware; stub @$BF80, SQ tables @$B000)
//   copro $FFFC/D     -> logic ($BF80 reset vector)
//
// Host (game CPU) register window at $5000-$51FF (open bus on stock MMC1):
//   $5000-$507F  W  board bytes 0..127      -> copro $0500+i
//   $5080-$5083  W  cA / cB / nA / nB       -> copro $6124-$6127
//   $5084       W   GO: clears DONE, pulses coprocessor reset (re-runnable per pill)
//   $5084       R   DONE flag               <- copro $61FF (1 = result ready)
//   $5085       R   best_col                <- copro $6134
//   $5086       R   best_orient(0..3)       <- copro $6135
//
// Proven in simulation (fpga/copro in dr-mario-mods): handshake 6/6 vs the py65 machine,
// 13-23M copro clocks per pill -> ~0.15-0.35s at 85.9MHz.
module CoproDrMario #(parameter [6:0] WIN = 7'b0101_000) (   // WIN = prg_ain[15:9] window select
	input         clk,        // host/bridge clock (NES system clock ~21.5MHz)
	input         clk_cpu,    // coprocessor clock (clk85 ~85.9MHz): 6502 + ROM + RAM port A
	input         ce,         // M2 (game-CPU cycle enable) for host-side sampling
	input         enable,     // me[100]
	input  [15:0] prg_ain,
	input         prg_read,
	input         prg_write,
	input   [7:0] prg_din,
	output  [7:0] prg_dout,   // valid when copro_sel && prg_read (cart_top overrides)
	output        copro_sel   // host window hit (WIN: copro1=$5000-$51FF, copro2=$5200-$53FF)
);

assign copro_sel = enable && (prg_ain[15:9] == WIN);   // window-relative offset = prg_ain[8:0]

// ------------------------------------------------------------------ coprocessor CPU
wire [15:0] AB;
wire  [7:0] DO;
wire        WE;
reg   [4:0] rst_cnt = 5'h1F;    // parked in reset until first GO (host clk domain)
reg         parked  = 1'b1;
wire        cpu_rst_src = (rst_cnt != 0) || parked;
// 2FF sync into the fast CPU domain (reset pulse is 31 host clocks = ~124 clk_cpu: plenty)
reg         rst_m = 1'b1, cpu_rst = 1'b1;
always @(posedge clk_cpu) begin rst_m <= cpu_rst_src; cpu_rst <= rst_m; end
wire  [7:0] DI;

copro6502 cpu6502(
	.clk(clk_cpu), .reset(cpu_rst), .AB(AB), .DI(DI), .DO(DO), .WE(WE),
	.IRQ(1'b0), .NMI(1'b0), .RDY(1'b1)
);

// copro-side address decode
wire        a_ram_lo = (AB[15:12] == 4'h0);          // $0000-$0FFF
wire        a_ram_st = (AB[15:8]  == 8'h61);         // $6100-$61FF
wire        a_ram    = a_ram_lo | a_ram_st;
wire        a_rom    = (AB[15:14] == 2'b10);         // $8000-$BFFF
wire        a_vec    = (AB[15:1]  == 15'h7FFE);      // $FFFC/$FFFD
wire        a_lev    = (AB[15:8]  == 8'h70);         // $7000-$70FF: LeafEval accelerator
wire [11:0] a_addr   = a_ram_st ? {4'h8, AB[7:0]} : AB[11:0];

// ---------------------------------------------------------- LeafEval/BoardEngine
// $7000-$707F W: board bytes into slot `wslot` (NES encoding -> 3-bit cells)
// $70E0-$70E4 W: args o4/col/ca/cb/slot ; $70F3 W: wslot ; $70F4 W: command (pulse)
// $70F8 W: legacy LEAF start. Reads: $70F0/1 sco, $70F2 win, $70E8 legal,
// $70E9/EA rv_cells/vir, $70EB/EC imm, $70F8 done.
wire       lev_wr_board = WE && !cpu_rst && a_lev && !AB[7];
wire       lev_start    = WE && !cpu_rst && a_lev && (AB[7:0] == 8'hF8);
wire       lev_cmd_go   = WE && !cpu_rst && a_lev && (AB[7:0] == 8'hF4);
wire       lev_wr_arg   = WE && !cpu_rst && a_lev && (AB[7:4] == 4'hE) && !AB[3];
wire [2:0] lev_enc = (DO == 8'hFF) ? 3'd0
                   : {(DO[7:4] == 4'hD), (DO[1:0] == 2'd0) ? 2'd1
                                        : (DO[1:0] == 2'd1) ? 2'd2 : 2'd3};
wire [1:0] lev_colenc = (DO[1:0] == 2'd0) ? 2'd1 : (DO[1:0] == 2'd1) ? 2'd2 : 2'd3;
reg  [1:0] lev_wslot;
reg  [1:0] lev_a_o4, lev_a_sl, lev_a_ca, lev_a_cb;
reg  [2:0] lev_a_col;
always @(posedge clk_cpu) begin
	if (WE && !cpu_rst && a_lev && (AB[7:0] == 8'hF3)) lev_wslot <= DO[1:0];
	if (lev_wr_arg)
		case (AB[2:0])
			3'd0: lev_a_o4  <= DO[1:0];
			3'd1: lev_a_col <= DO[2:0];
			3'd2: lev_a_ca  <= lev_colenc;
			3'd3: lev_a_cb  <= lev_colenc;
			default: lev_a_sl <= DO[1:0];
		endcase
end
wire        lev_done, lev_win, lev_legal;
wire [15:0] lev_sco, lev_imm;
wire  [5:0] lev_rvc;
wire  [3:0] lev_rvv;
LeafEval leafeval(
	.clk   (clk_cpu),
	.rst   (cpu_rst),
	.wr    (lev_wr_board),
	.waddr (AB[6:0]),
	.wdata (lev_enc),
	.wslot (lev_wslot),
	.start (lev_start),
	.cmd   (DO[3:0]),
	.cmd_go(lev_cmd_go),
	.a_sl  (lev_a_sl),
	.a_o4  (lev_a_o4),
	.a_col (lev_a_col),
	.a_ca  (lev_a_ca),
	.a_cb  (lev_a_cb),
	.done  (lev_done),
	.sco   (lev_sco),
	.win   (lev_win),
	.legal (lev_legal),
	.rv_cells(lev_rvc),
	.rv_vir(lev_rvv),
	.imm   (lev_imm)
);
reg [7:0] lev_q;
always @(posedge clk_cpu)
	case (AB[3:0])
		4'h0: lev_q <= lev_sco[7:0];
		4'h1: lev_q <= lev_sco[15:8];
		4'h2: lev_q <= {7'b0, lev_win};
		4'h8: lev_q <= (AB[7:4] == 4'hE) ? {7'b0, lev_legal} : {7'b0, lev_done};
		4'h9: lev_q <= {2'b0, lev_rvc};
		4'hA: lev_q <= {4'b0, lev_rvv};
		4'hB: lev_q <= lev_imm[7:0];
		4'hC: lev_q <= lev_imm[15:8];
		default: lev_q <= {7'b0, lev_done};
	endcase

// ------------------------------------------------------------------ 16KB firmware ROM (copro-only)
reg [7:0] rom [0:16383];
initial $readmemh("copro_rom.hex", rom);
reg [7:0] rom_q;
always @(posedge clk_cpu) rom_q <= rom[AB[13:0]];

// ------------------------------------------------------------------ 4KB TDP work RAM
// Port A: coprocessor. Port B: host bridge. Explicit altsyncram via the core's dpram
// wrapper (behavioral TDP templates fail inference in Quartus Std -> 33k regs -> no fit).
// q_* = synchronous read, 1-cycle latency: exactly what Arlet's DI and the bridge expect.
// Neither side reads an address it is writing in the same cycle, so RDW mode is moot.
wire [7:0] ram_a_q, ram_b_q;
dpram #(.widthad_a(12), .width_a(8)) wram (
	.clock_a  (clk_cpu),
	.address_a(a_addr),
	.data_a   (DO),
	.wren_a   (WE && !cpu_rst && a_ram),
	.q_a      (ram_a_q),
	.clock_b  (clk),
	.address_b(hb_addr),
	.data_b   (hb_din),
	.wren_b   (hb_we),
	.q_b      (ram_b_q)
);

// registered DI mux (data + selects all registered -> DI valid 1 cycle after AB, as Arlet expects)
reg sel_ram_d, sel_rom_d, sel_vec_d, sel_lev_d, ab0_d;
always @(posedge clk_cpu) begin
	sel_ram_d <= a_ram; sel_rom_d <= a_rom; sel_vec_d <= a_vec; sel_lev_d <= a_lev; ab0_d <= AB[0];
end
assign DI = sel_vec_d ? (ab0_d ? 8'hBF : 8'h80) :
            sel_rom_d ? rom_q :
            sel_lev_d ? lev_q :
            sel_ram_d ? ram_a_q : 8'hFF;

// ------------------------------------------------------------------ host bridge (port B control)
// game-window offset -> copro folded RAM address
function [11:0] xlate(input [8:0] a);
	begin
		if (!a[8] && !a[7])      xlate = {5'b01010, a[6:0]};   // $5000-7F -> $0500+i
		else if (!a[8] && a[7])
			case (a[6:0])
				7'h00: xlate = 12'h824;    // $6124 cA
				7'h01: xlate = 12'h825;    // cB
				7'h02: xlate = 12'h826;    // nA
				7'h03: xlate = 12'h827;    // nB
				7'h04: xlate = 12'h8FF;    // $61FF DONE
				7'h05: xlate = 12'h834;    // $6134 best_col
				7'h06: xlate = 12'h835;    // $6135 best_orient
				default: xlate = 12'h8FE;  // scratch
			endcase
		else                     xlate = 12'h8FE;
	end
endfunction

reg [11:0] hb_addr;
reg  [7:0] hb_din;
reg        hb_we;

always @(posedge clk) begin
	hb_we <= 1'b0;
	if (ce && prg_write && copro_sel) begin
		if (prg_ain[8:0] == 9'h084) begin
			// GO: clear DONE and (re)start the coprocessor
			hb_addr <= 12'h8FF; hb_din <= 8'h00; hb_we <= 1'b1;
			rst_cnt <= 5'h1F; parked <= 1'b0;
		end else begin
			hb_addr <= xlate(prg_ain[8:0]); hb_din <= prg_din; hb_we <= 1'b1;
		end
	end else begin
		hb_addr <= xlate(prg_ain[8:0]);    // idle: track read address
		if (rst_cnt != 0 && !parked) rst_cnt <= rst_cnt - 1'b1;
	end
end

assign prg_dout = ram_b_q;

endmodule

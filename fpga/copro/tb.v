// Coprocessor proof: Arlet 6502 + 64KB mem running the depth-2 search firmware.
// The 6502 boots (reset vector -> stub -> JSR search), computes the move, writes
// best_col($6134)/best_orient($6135), sets DONE($6140)=1. We count clocks to DONE.
`timescale 1ns/1ps
module tb;
  reg clk = 0, reset = 1;
  wire [15:0] AB;
  wire [7:0]  DO;
  wire        WE;
  reg  [7:0]  DI;
  reg  [7:0]  mem [0:65535];
  integer cyc = 0;

  cpu u(.clk(clk), .reset(reset), .AB(AB), .DI(DI), .DO(DO), .WE(WE),
        .IRQ(1'b0), .NMI(1'b0), .RDY(1'b1));

  always #5 clk = ~clk;                 // 100 MHz sim clock

  always @(posedge clk) begin
    if (WE) mem[AB] <= DO;              // synchronous write
    DI <= mem[AB];                      // synchronous read (Arlet's 1-cycle read latency)
  end

  initial begin
    $readmemh("firmware.hex", mem);
    repeat (8) @(posedge clk);          // hold reset
    reset = 0;
    while (mem[16'h6140] == 8'h00 && cyc < 32'd300000000) begin
      @(posedge clk); cyc = cyc + 1;
      if (cyc % 5000000 == 0) $display("... running, clk=%0d", cyc);
    end
    if (mem[16'h6140] != 8'h00)
      $display("RESULT done_clocks=%0d best_col=%0d best_orient=%0d", cyc, mem[16'h6134], mem[16'h6135]);
    else
      $display("TIMEOUT clk=%0d (never set DONE)", cyc);
    $finish;
  end
endmodule

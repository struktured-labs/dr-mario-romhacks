// Top for sim: Arlet 6502 + 64KB mem running the search firmware. Exposes done + result.
module top(input clk, input reset, output [7:0] done, output [7:0] rc, output [7:0] ro);
  wire [15:0] AB;
  wire [7:0]  DO;
  wire        WE;
  reg  [7:0]  DI;
  reg  [7:0]  mem [0:65535];
  cpu u(.clk(clk), .reset(reset), .AB(AB), .DI(DI), .DO(DO), .WE(WE),
        .IRQ(1'b0), .NMI(1'b0), .RDY(1'b1));
  always @(posedge clk) begin
    if (WE) mem[AB] <= DO;
    DI <= mem[AB];
  end
  initial $readmemh("firmware.hex", mem);
  assign done = mem[16'h6140];
  assign rc   = mem[16'h6134];
  assign ro   = mem[16'h6135];
endmodule

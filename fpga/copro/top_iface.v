// Task 2: host<->coprocessor handshake block — the shape of the real mapper.
// Coprocessor: Arlet 6502 + 64KB RAM (ROM image preloaded, board region empty).
// Host port (= what the NES game CPU sees as mapper registers / shared RAM):
//   host_we/host_addr/host_wdata : write shared RAM (board, colors, clear DONE)
//   host_raddr -> host_rdata     : read shared RAM (poll DONE, read move)
//   go                           : pulse = reset coprocessor and start a fresh search
// While the coprocessor runs, host reads/writes are interleaved on idle cycles (sim
// simplification; the real mapper uses a dual-port BRAM so both sides are concurrent).
module top_iface(
  input        clk,
  input        go,           // pulse: (re)start coprocessor
  input        host_we,
  input [15:0] host_addr,
  input  [7:0] host_wdata,
  input [15:0] host_raddr,
  output [7:0] host_rdata
);
  wire [15:0] AB;
  wire [7:0]  DO;
  wire        WE;
  reg  [7:0]  DI;
  reg  [3:0]  rst_cnt = 4'hF;            // hold coprocessor in reset until first GO
  wire        cpu_rst = |rst_cnt || hold;
  reg         hold = 1;                  // parked until first GO
  reg  [7:0]  mem [0:65535];

  cpu u(.clk(clk), .reset(cpu_rst), .AB(AB), .DI(DI), .DO(DO), .WE(WE),
        .IRQ(1'b0), .NMI(1'b0), .RDY(1'b1));

  always @(posedge clk) begin
    if (go) begin rst_cnt <= 4'hF; hold <= 1'b0; end       // GO: pulse reset, then run
    else if (rst_cnt != 0) rst_cnt <= rst_cnt - 1'b1;
    if (WE && !cpu_rst) mem[AB] <= DO;
    DI <= mem[AB];
    if (host_we) mem[host_addr] <= host_wdata;   // host write port
  end

  assign host_rdata = mem[host_raddr];

  initial $readmemh("firmware_rom.hex", mem);
endmodule

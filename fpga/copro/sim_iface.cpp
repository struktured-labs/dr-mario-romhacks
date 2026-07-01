// Task 2 host: acts as the NES game CPU against the mapper's shared-RAM interface.
// For each problem in hostdata.txt: write board($0500)+colors($6124-27), clear DONE($61FF),
// pulse GO, poll DONE, read move ($6134/$6135), compare to the oracle. Re-uses ONE
// coprocessor instance across all problems (proves re-runnability).
#include "Vtop_iface.h"
#include "verilated.h"
#include <cstdio>
#include <cstdlib>

static Vtop_iface* t;
static long total_clocks = 0;

static void tick() { t->clk = 0; t->eval(); t->clk = 1; t->eval(); total_clocks++; }

static void host_write(int addr, int data) {
  t->host_we = 1; t->host_addr = addr; t->host_wdata = data; tick(); t->host_we = 0;
}
static int host_read(int addr) { t->host_raddr = addr; t->eval(); return t->host_rdata; }

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  t = new Vtop_iface;
  t->go = 0; t->host_we = 0; tick();

  FILE* f = fopen("hostdata.txt", "r");
  if (!f) { printf("FAIL no hostdata.txt\n"); return 1; }
  int n; if (fscanf(f, "%d", &n) != 1) { printf("FAIL bad header\n"); return 1; }

  int pass = 0;
  for (int k = 0; k < n; k++) {
    int cA, cB, nA, nB, ec, eo, b[128];
    fscanf(f, "%d %d %d %d %d %d", &cA, &cB, &nA, &nB, &ec, &eo);
    for (int i = 0; i < 128; i++) fscanf(f, "%x", &b[i]);

    for (int i = 0; i < 128; i++) host_write(0x0500 + i, b[i]);   // board
    host_write(0x6124, cA); host_write(0x6125, cB);               // colors
    host_write(0x6126, nA); host_write(0x6127, nB);
    host_write(0x61FF, 0);                                        // clear DONE
    t->go = 1; tick(); t->go = 0;                                 // GO pulse

    long c0 = total_clocks;
    while (host_read(0x61FF) == 0 && total_clocks - c0 < 200000000L) tick();
    long clocks = total_clocks - c0;
    int rc = host_read(0x6134), ro = host_read(0x6135);
    bool ok = (host_read(0x61FF) != 0) && rc == ec && ro == eo;
    if (ok) pass++;
    printf("case %d: copro=(%d,%d) oracle=(%d,%d) clocks=%ld  %s\n",
           k, rc, ro, ec, eo, clocks, ok ? "ok" : "MISMATCH");
  }
  printf("HANDSHAKE %d/%d passed, one coprocessor instance, re-armed per pill\n", pass, n);
  fclose(f); delete t;
  return pass == n ? 0 : 1;
}

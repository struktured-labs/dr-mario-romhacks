// Functional verification of the REAL MiSTer mapper module (CoproDrMario.sv) before Quartus.
// Emulates the NES-side bus: ce pulses once per 48 clk (1.79MHz vs 85.9MHz), prg_ain/prg_din
// held across the whole CPU cycle like a real 6502 write. Streams the same hostdata.txt
// problems through the $5000-$51FF window. Expect 6/6 vs the py65 machine oracle.
#include "VCoproDrMario.h"
#include "verilated.h"
#include <cstdio>

static VCoproDrMario* t;
static long clocks = 0;

static void tick() { t->clk = 0; t->eval(); t->clk = 1; t->eval(); clocks++; }

// one NES CPU cycle = 48 master clocks, ce high on exactly one of them
static void nes_cycle(int addr, int data, bool we) {
  t->prg_ain = addr; t->prg_din = data; t->prg_write = we; t->prg_read = !we;
  for (int i = 0; i < 48; i++) { t->ce = (i == 24); tick(); }
  t->ce = 0; t->prg_write = 0; t->prg_read = 0;
}

static int nes_read(int addr) {
  t->prg_ain = addr; t->prg_read = 1; t->prg_write = 0;
  for (int i = 0; i < 48; i++) { t->ce = (i == 24); tick(); }
  int v = t->prg_dout;                       // sampled at end of the CPU cycle
  t->ce = 0; t->prg_read = 0;
  return v;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  t = new VCoproDrMario;
  t->enable = 1; t->ce = 0; tick();

  FILE* f = fopen("hostdata.txt", "r");
  if (!f) { printf("FAIL no hostdata.txt\n"); return 1; }
  int n; fscanf(f, "%d", &n);
  int pass = 0;
  for (int k = 0; k < n; k++) {
    int cA, cB, nA, nB, ec, eo, b[128];
    fscanf(f, "%d %d %d %d %d %d", &cA, &cB, &nA, &nB, &ec, &eo);
    for (int i = 0; i < 128; i++) fscanf(f, "%x", &b[i]);

    for (int i = 0; i < 128; i++) nes_cycle(0x5000 + i, b[i], true);
    nes_cycle(0x5080, cA, true); nes_cycle(0x5081, cB, true);
    nes_cycle(0x5082, nA, true); nes_cycle(0x5083, nB, true);
    nes_cycle(0x5084, 1, true);                       // GO

    long c0 = clocks;
    long polls = 0;
    while (nes_read(0x5084) == 0 && clocks - c0 < 16000000000L) polls++;   // d3: dense ~0.5G clks
    long used = clocks - c0;
    int rc = nes_read(0x5085), ro = nes_read(0x5086);
    bool ok = rc == ec && ro == eo && used < 16000000000L;
    if (ok) pass++;
    printf("case %d: copro=(%d,%d) oracle=(%d,%d) clocks=%ld (%.2fs @85.9MHz eff/2) %s\n",
           k, rc, ro, ec, eo, used, used / 85.9e6, ok ? "ok" : "MISMATCH");
  }
  printf("MISTER MODULE %d/%d\n", pass, n);
  fclose(f); delete t;
  return pass == n ? 0 : 1;
}

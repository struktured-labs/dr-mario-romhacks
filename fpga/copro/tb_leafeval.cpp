// LeafEval vs the python leaf_d3 golden: reads leafeval_cases.txt
// (per line: 128 hex cell bytes in NES encoding + expected sco (signed) + win),
// converts to the module's 3-bit encoding, runs, compares.
#include "VLeafEval.h"
#include "VLeafEval___024root.h"
#include "verilated.h"
#include <cstdio>

static VLeafEval* t;
static void tick() { t->clk = 0; t->eval(); t->clk = 1; t->eval(); }

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  t = new VLeafEval;
  t->rst = 1; t->wr = 0; t->start = 0; tick(); tick(); t->rst = 0; tick();

  FILE* f = fopen("leafeval_cases.txt", "r");
  if (!f) { printf("FAIL no leafeval_cases.txt\n"); return 1; }
  int n; if (fscanf(f, "%d", &n) != 1) return 1;
  int pass = 0;
  for (int k = 0; k < n; k++) {
    int exp_sco, exp_win, b[128];
    for (int i = 0; i < 128; i++) if (fscanf(f, "%x", &b[i]) != 1) return 1;
    if (fscanf(f, "%d %d", &exp_sco, &exp_win) != 2) return 1;

    for (int i = 0; i < 128; i++) {
      int enc = 0;
      if (b[i] != 0xFF) {
        int col = (b[i] & 0x0F) + 1;               // NES nibble 0..2 -> 1..3
        int vir = ((b[i] & 0xF0) == 0xD0) ? 1 : 0;
        enc = (vir << 2) | col;
      }
      t->wr = 1; t->waddr = i; t->wdata = enc; tick();
    }
    t->wr = 0;
    t->start = 1; tick(); t->start = 0;
    long cyc = 0;
    while (!t->done && cyc < 100000) { tick(); cyc++; }
    short got = (short)t->sco;
    bool ok = t->done && (int)t->win == exp_win && (exp_win || got == (short)exp_sco);
    if (ok) pass++;
    else if (k < 8 || pass + 8 > k)
      printf("case %d: got sco=%d win=%d (cyc=%ld) exp sco=%d win=%d MISMATCH rdy_ext=%d vrdy=%d\n",
             k, got, (int)t->win, cyc, exp_sco, exp_win,
             (int)t->rootp->LeafEval__DOT__rdy_ext, (int)t->rootp->LeafEval__DOT__vrdy),
      printf("   mh=%d ho=%d tr=%d spawn=%d setup=%d buried=%d pol=%d\n",
             (int)t->rootp->LeafEval__DOT__maxh, (int)t->rootp->LeafEval__DOT__holes,
             (int)t->rootp->LeafEval__DOT__toprisk, (int)t->rootp->LeafEval__DOT__spawn,
             (int)t->rootp->LeafEval__DOT__setup, (int)t->rootp->LeafEval__DOT__buried,
             (int)t->rootp->LeafEval__DOT__pollution);
    if (k == 0) printf("case 0 latency: %ld cycles\n", cyc);
  }
  printf("LEAFEVAL %d/%d\n", pass, n);
  fclose(f); delete t;
  return pass == n ? 0 : 1;
}

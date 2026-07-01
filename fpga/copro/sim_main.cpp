#include "Vtop.h"
#include "verilated.h"
#include <cstdio>
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Vtop* t = new Vtop;
  t->reset = 1;
  for (int i = 0; i < 16; i++) { t->clk = 0; t->eval(); t->clk = 1; t->eval(); }
  t->reset = 0;
  long cyc = 0;
  while (t->done == 0 && cyc < 300000000L) {
    t->clk = 0; t->eval(); t->clk = 1; t->eval(); cyc++;
  }
  if (t->done) printf("RESULT done_clocks=%ld best_col=%d best_orient=%d\n", cyc, t->rc, t->ro);
  else         printf("TIMEOUT clocks=%ld\n", cyc);
  delete t; return 0;
}

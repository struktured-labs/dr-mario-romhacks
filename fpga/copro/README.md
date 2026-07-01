# Dr. Mario depth-2 AI as an out-of-band 6502 coprocessor — HDL proof

Proves the "put a second CPU in the cartridge" answer to the latency problem. A bare 6502
(Arlet Ottens' Verilog core) runs the **exact same** validated depth-2 search binary
(`test_depth2.build_search`) as standalone firmware — free-running, NOT limited to the NES
NMI's ~8k cycles/frame. Verilated; correctness checked against the Python oracle `decide_d2_4`.

## Result (verilator, 6/6 random boards)

| seed | oracle (col,orient) | coprocessor | clocks (full search) |
|---|---|---|---|
| 1 | 6,0 | 6,0 ✓ | 52.8M |
| 7 | 1,2 | 1,2 ✓ | 56.0M |
| 42 | 1,0 | 1,0 ✓ | 57.1M |
| 100 | 2,0 | 2,0 ✓ | 50.4M |
| 321 | 0,2 | 0,2 ✓ | 56.4M |
| 777 | 0,2 | 0,2 ✓ | 48.2M |

**Exact move match on every board.** ~48–57M clocks for the *full* (non-incremental) search.

## What it means for latency

The in-cart NMI-resumable 6502 is capped at ~8k cyc/frame → ~4700 frames → **~78s/pill**.
A coprocessor is free-running; the SAME work at an FPGA clock:

| clock | full search (~54M clk, measured) | incremental search (~13–23M clk, MEASURED) |
|---|---|---|
| 21.5 MHz (NES master) | ~2.5 s | ~0.6–1.1 s |
| 50 MHz | ~1.1 s | **~0.27–0.46 s** |
| 100 MHz (easy on Cyclone V) | ~0.55 s | **~0.13–0.23 s** |

Incremental measured via `build_firmware_incr.py` (drives `build_resumable_incr` to completion:
`JSR arm; loop{JSR step} while ARMED`). drop_setup=0 matches the oracle exactly; drop_setup=1
(the shipping ~66%-clear variant) ~13–23M clk. An *atomic* incremental (no resumable phase
dispatch overhead) would shave another ~2–3× → ~50–80ms, but ~150ms is already instant.

i.e. **~50–1000× faster than the frame-limited cart**, running unchanged 6502 code — and it
deletes the resumable phase-machine, NMI budget, and zp-remap complexity entirely.

## Files
- `build_firmware.py` — assembles `build_search` + a reset stub + SQ tables into a 64KB image
  (`firmware.hex`), preloads a test board, and writes the oracle's expected move (`expected.txt`).
- `top_v.v` / `sim_main.cpp` — verilator harness: 6502 + 64KB mem, boots, runs to DONE, prints move+clocks.
- `tb.v` — equivalent iverilog testbench (slower; use verilator for the multi-M-clock search).
- `cpu.v`, `ALU.v` — Arlet Ottens' 6502 (vendored; his public 6502 core). Later swapped for the
  NES core's T65 in the MiSTer mapper / cart FPGA.

## Build + run
```
python build_firmware.py <seed>
verilator --cc --build --exe -Wno-fatal --top-module top top_v.v cpu.v ALU.v sim_main.cpp -o copro_vsim
./obj_dir/copro_vsim     # reads firmware.hex from CWD
```

## Next (productization)
1. Incremental search firmware → sub-100ms clocks (extrapolation above).
2. go/done handshake + dual-port shared board RAM = the real memory-mapped mapper interface
   (host writes board+colors+GO, polls DONE, reads move — ~30 bytes of 6502 on the game side).
3. Wrap as a custom NES mapper (T65 + block RAM) in `NES_MiSTer/rtl/cart.sv` (`me[N]` enable),
   build the RBF (Quartus — pending PLL-IP regen for the non-17.0 toolchain), deploy to MiSTer.
   Same design drops into a small FPGA on a real plastic cart.

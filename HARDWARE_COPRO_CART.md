# Physical Coprocessor Cartridge — Design Doc

**Status:** exploratory design (2026-07-12). Not committed to a build. Captures the
architecture for taking the MiSTer depth-3 coprocessor to other hardware: a custom NES
cartridge, a pass-through adapter, and the Analogue Pocket.

## 0. Context

The depth-3 AI runs today as an RTL block inside the MiSTer NES core: a second 6502
(`copro6502.v`) plus the `LeafEval`/BoardEngine accelerator, integrated as mapper 100 with a
host register window at `$5000–$53FF`. It reaches ~1 second per move (validated py65 →
verilator → Quartus → hardware). Everything below is about running *that same RTL* somewhere
other than a DE10-Nano.

The single most important enabling fact: **our host window already lives in cartridge-native
address space.** `$5000–$53FF` is inside the `$4020–$5FFF` expansion region — the exact range
Nintendo's own **MMC5** uses for its registers. The NES routes the CPU address bus (A0–A14),
data bus (D0–D7), R/W, and the M2 clock to the 72-pin cart connector, and the cart decodes
that region itself. So a real cartridge can host the copro window with **no console
modification**. We chose that address range partly for this reason.

## 1. Custom cartridge (recommended real-hardware path)

### 1.1 Architecture

One FPGA on the cart runs the entire existing design — the MMC1 mapper logic, both
`CoproDrMario` instances, and the BoardEngine. It is all RTL already; porting is a
fit-and-timing exercise on the chosen part, not a redesign.

```
  NES 72-pin bus ──┬── level shifters (5V ↔ 3.3V) ──┬── FPGA
   A0..A14, D0..D7 │                                 │   ├─ mapper 100 (MMC1 + decode)
   R/W, M2, /ROMSEL│                                 │   ├─ CoproDrMario x1-2  (6502 + copro)
   PPU A0..A13, ...─┘                                 │   └─ LeafEval / BoardEngine (accel)
                    on-cart oscillator ──────────────┘   (copro free-runs on this clock)
  game ROM (flash/mask) ── FPGA or direct to bus
  config flash (FPGA bitstream) ── FPGA
  regulators (5V -> 3.3/1.8/1.0V) ── FPGA rails
```

### 1.2 Clock domains — ports verbatim

The MiSTer design already separates the copro clock (`clk85`, ~85.9 MHz) from the host bridge
(M2/CE). On a cart, the copro free-runs on an on-cart oscillator; the host bridge synchronizes
to M2. The existing 2-FF reset synchronizer and the DONE-after-results ordering carry over
unchanged. **No new clock-domain work** beyond choosing the oscillator frequency.

### 1.3 FPGA selection

- On the MiSTer (Cyclone V `5CSEBA6`, ~110K LE) the two-copro + BoardEngine design filled
  ~4191 LABs — "nearly full," and timing closed at 85.9 MHz only after a fitter reseed
  (worst slack +0.056 ns).
- Candidate cart parts: **Lattice ECP5** (LFE5U-25/45, cheap, good toolchain via
  open-source `prjtrellis`/`nextpnr`, 5V-tolerant with shifters) or **Intel Cyclone 10 LP**
  (same tool family as our Quartus flow → least porting friction).
- **Clock headroom is now huge.** At ~1s/pill we do not need 85.9 MHz. A cart oscillator of
  25–50 MHz still gives ~1.5–3.5s/pill, which is fine. Lower clock → far easier timing
  closure on a smaller/cheaper part.

### 1.4 One vs two coprocessors

- **Two** = true parallelism (both players think simultaneously) — nicest for the CPU-vs-CPU
  demo, but costs FPGA area.
- **One, time-shared** = ~2s/pill effective at BoardEngine speed — perfectly acceptable now,
  and fits a smaller/cheaper part. This was the original architecture before we split them.
- **Recommendation:** design for one; add the second only if the chosen part has comfortable
  room. The quality/pace argument for two evaporated once we hit ~1s/pill.

### 1.5 Physical design checklist

- 72-pin edge connector (PRG: A0–A14, D0–D7, R/W, /ROMSEL, M2; CHR/PPU: A0–A13, D0–D7,
  /RD, /WR, CIRAM /A13; +5V, GND).
- **Level shifting** — NES bus is 5V, FPGA I/O is 3.3V or lower. Bidirectional shifters on
  D0–D7; the address/control lines are console→cart (inputs to the FPGA) so simpler
  unidirectional shifting or 5V-tolerant inputs suffice.
- On-cart **oscillator** (copro clock) + **config flash** (bitstream) + **regulators**
  (5V → FPGA rails).
- **Game ROM** — flash (reprogrammable) or mask. The patched auto-nav Dr. Mario image.
- Homebrew cart infrastructure exists for the mechanical/bus layer: InfiniteNesLives (INL)
  cart PCBs, Sealie Computing manufacturing.

### 1.6 Precedent

On-cart coprocessors are a well-trodden path: the SNES **SA-1** was a faster 65816 running on
Star Fox/Kirby carts; **SuperFX**, **DSP-1**, and Nintendo's own **MMC5** all put compute on
the cartridge. A two-6502-copro Dr. Mario cart is that same enhancement-chip pattern, applied
to the NES. This is precedented engineering, not a moonshot.

## 2. Pass-through adapter (Game-Genie form factor)

Concept: a device between console and cart that carries the coprocessor, so (ideally) a stock
cart becomes "smart." Analyzed honestly, the wall is **output, not input**.

- **Sensing works.** A0–A14 and D0–D7 are on the bus every cycle, so the adapter can *snoop
  the CPU writing the board* to internal RAM (`$0400–$05FF`, the two playfields) and shadow
  it — reconstructing full game state **without the game cooperating.** (Counterintuitive: the
  board is console-side RAM, but the write cycles are visible on the cart bus.)
- **Acting is the wall.** To play, the copro must press buttons, but the controller ports are
  read via `$4016/$4017` **inside the console** — not on the cart bus. A cart/adapter cannot
  cleanly inject input. The options are both poor:
  - drive the data bus during the game's `$4016` read to spoof the controller — bus
    contention, console-revision-fragile;
  - patch the ROM so the game reads input from the copro — clean, but then it is not a
    *stock* cart.

  Our MiSTer build dodges this by patching the ROM to inject at the game's own input
  variables. A stock cart has no such hook.

- **The honest variant: a modular copro base.** Split the custom cart into two boards — a
  cheap **ROM-only cart** (the patched game, no copro) that plugs into a reusable **copro
  base** (the FPGA). One base serves many game carts; load a different bitstream per game.
  Both pieces are custom, but the expensive FPGA is amortized. This is the pass-through idea
  made buildable.

**Verdict:** a pass-through cannot make a *stock* cart smart (blocked on input injection). A
modular copro-base + patched-ROM-cart split is a legitimate design if reusability is the goal.

## 3. Analogue Pocket port (low-risk next step)

- Same FPGA family as MiSTer — both are Cyclone V (Pocket `5CEBA4`, DE10 `5CSEBA6`). The copro
  RTL should port with minimal change.
- Work is the **openFPGA** framework wrapper (video/controls/interaction) instead of MiSTer's;
  fork an existing openFPGA NES core and drop in mapper 100 + the copro, same surgery as
  `NES_MiSTer`.
- **Constraints:** the Pocket's part has roughly *half* the logic (~49K vs ~110K LE), so
  likely **one time-shared copro**, not two; and if 85.9 MHz doesn't close, drop the copro
  clock (huge headroom now). Confirm the exact LAB budget of the `5CEBA4` before committing.
- Payoff: the demo, portable, in hand.

## 4. Recommended sequencing

1. **Analogue Pocket port** — same silicon family, weeks, portable demo.
2. **Speculative next-pill search** (firmware/driver-only) — search pill N+1 during pill N's
   fall using the known preview; makes even the current MiSTer *feel* zero-latency.
3. **Custom cart** — start with a *design doc → dev-board bring-up* (drive the `$5xxx` window
   from a real NES with a logic analyzer before committing a PCB), one copro, cheap FPGA.
4. **Modular copro base** — only if reusability across games becomes a goal.

## 5. Open questions / risks

- Exact FPGA part + toolchain (ECP5/open-source vs Cyclone/Quartus) — trades cost against
  porting friction.
- 5V bus timing margins through level shifters at the chosen copro clock.
- CHR/PPU-side handling — the current mapper passes CHR through; confirm the physical cart
  reproduces it (CHR-RAM vs CHR-ROM, banking).
- Whether one copro at a lower clock is genuinely enough for the *shipped* demo cadence
  (measure against the ~1s target with margin).

# Depth-2 cart build plan (autonomous run toward playable L11 ~67%)

## Status
- DONE+validated (py65): atomic depth-2 search `tests/test_depth2.py::build_search` 14/14 vs
  oracle `decide_d2_4`. Eval (`primitives.emit_eval::leaf_score`) 500/500. land_place 12800/12800.
  Commit 99c7a11 on branch claude/live-planner-control.
- The atomic search is the GOLD reference for the resumable version: the resumable phase machine
  must, driven frame-by-frame, pick the SAME (best_col,best_orient4) as `build_search`/`decide_d2_4`.

## The problem
Atomic search ~50M cyc/pill. NMI-hook budget ~8k cyc/frame usable (freeze above ~10-13k, proven by
the depth-1 cart). So every per-frame chunk must be <=8k. Resumable = one bounded phase per frame,
state persists in RAM ($6000 PRG-RAM, free: original Dr.Mario has no RAM chip). Slow (~hundreds of
frames/pill) but PLAYABLE; caching later.

## RAM layout (all in free $6000-$7FFF PRG-RAM + game-safe zp)
- $0500 LIVE (game settled board, read for first-ply landing). DO NOT WRITE.
- $6000-$607F CUR  (working board; all primitives operate here; first_occ reads here)
- $6080-$60FF WORK1 (board-after-first-ply, persists across the inner loop)
- $6100-$610F MARK  (find_clears bit-packed)
- $6110-$611F eval term outputs (EV_BUR/RDY/SET/VIRFLAG/WIN/SCO/M/P) -- already in primitives.py
- $6120-$613F search state (cursors, imm, best_leaf, best_value, cand) -- already in test_depth2.py
- $6140-$615F resumable extras: ST2_PC (phase counter), region cursors for split primitives
- $7A00 square table (readiness) -- for cart, copy to RAM at boot or put a ROM copy + index
- zp $CA-$E1 pool for in-phase temps (each phase self-contained, no cross-frame zp reliance)

## Resolve choice: TARGETED (DECIDED 2026-06-30)
MEASURED on L11 (faithful cart_d2_golden, rich+compact): targeted=67.5%/25% vs full=67.2%/17%.
Targeted costs NOTHING -> USE TARGETED (resolve_capped, find_clears_targeted, ~6k, ONE phase).
Atomic reference build_search keeps a `resolve` param: 'full' (=14/14 vs decide_d2_4 oracle) and
'targeted' (the cart's). Resumable cart validates vs build_search(resolve='targeted'); the
targeted primitive is independently validated (test_kernel [targeted] 4500/4500) and gives 67.5%
on L11, so atomic_targeted is the trusted reference (no separate NES targeted oracle needed).

## Phase machine (ST2_PC), per the atomic search flow
Outer cursor (O1 0..3, C1 0..7), inner cursor (O2 0..3, C2 0..7), all in RAM.
0  LAND1:  copy LIVE->CUR; land_place(O1,C1,CA,CB). illegal -> advance O1/C1, stay. legal -> PC=1.
1  RES1:   resolve (targeted=1 phase, or full=split). -> RV. (if cleared, gravity sub-phase)
2  IMM1:   calc_imm -> S_IMM; has_virus. if won -> set CAND=(1,imm1), PC=CMP.
3  SAVE1:  copy CUR->WORK1; init inner (O2=C2=0, best_leaf unset, any2=0); PC=4.
4  LAND2:  copy WORK1->CUR; land_place(O2,C2,NA,NB). illegal -> advance O2/C2, stay. legal -> PC=5.
5  RES2:   resolve. -> RV.
6  LEAF_SHAPE:   shape (~5k)            } leaf_score split so each <=8k.
7  LEAF_BURIED:  buried (~5.6k)
8  LEAF_READ_A:  readiness cells 0..63  (accumulate EO in RAM)
9  LEAF_READ_B:  readiness cells 64..127
10 LEAF_SETUP_A: setup rows pass
11 LEAF_SETUP_B: setup cols pass
12 LEAF_COMB:    has_virus + combine -> EV_WIN/EV_SCO; leaf=(EV_WIN, imm2+EV_SCO);
                 update best_leaf; advance O2/C2 -> if more PC=4 else PC=13.
13 VALUE:   value=(best_leaf_win, imm1+best_leaf_score) (or leaf(WORK1) if !any2); CAND set.
14 CMP:     cmp_update; advance O1/C1 -> if more PC=0 else PUBLISH.
15 PUBLISH: write best_col->$DD, best_orient4->$DA(via $03A5 map), ST_MODE=DONE.

NOTE: readiness/setup currently single routines; need split variants that take a region arg and
accumulate into a RAM cell across the two phases. shape/buried fit one phase as-is (<8k).

## Validation
`tests/test_depth2.py::validate_resumable`: drive arm->step*->DONE in py65, confirm
(best_col,best_orient4) == decide_d2_4 over N boards, AND every step's cycle count <=8000.

## Cart integration (patch_cartridge.py)
- slicer(depth2) in unit-1; dispatch edge+arm+step. Boards/state in $6000 (enable MMC1 PRG-RAM;
  verify writes land). 4-state wrapper: rotate $03A5 to published $DA (4 states, not 2); move to $DD.
- Keep 0x37CF->$FB00 blob (preserves P2 leveling -- DO NOT bypass). Blob JMP $FF54 = our wrapper.
- v28cs stays ship until live L11 >= v28cs.

## Eval ablation (L11, compact+targeted, 12 seeds) -- SPEED LEVERS
- full rich (shape+setup+buried+readiness): 67.5% / 25%  <- current
- drop readiness: 64.9% / 16.7%  (-2.6pp, saves the 17.5k term / 3 phases) <- best speed/acc trade
- drop setup:     60.9% / 16.7%  (setup is the KEY term -- keep it)
- setup ONLY (shape+setup): 63.9% / 8.3%   ;  buried ONLY: 38.5% (craters)
DECISION: keep full eval for now (readiness split already written+validated). When optimizing
for speed, DROP readiness first (coordinated: nes_d2_golden leaf_shape_score, 6502 combine/
leaf_score, test_leaf_score golden, then re-validate build_search vs updated oracle) -> 64.9%.
Term costs: shape 5k, buried 5.6k, setup 18k(split 2-3), readiness 17.5k(split 3: readiness_rg
done, 500/500). setup still needs a resumable rows/cols-pass split.

## RESUMABLE MACHINE STATUS (2026-06-30) -- tests/test_resumable.py
WORKS: 3/3 vs decide_d2_4. ~11000 steps/board (~100s/pill -- correct but slow; needs
incremental eval for real-time). Per-PC max cyc (must all be <=8k for the cart):
  LAND1 2879, RES1 4674, IMM1 8011, LAND2 2900, RES2 16921(!!), SHAPE 5301, BURIED 4961,
  READ 5540, SETUP 4442, COMB 5650, VALUE 124, CMP 207.
NEXT FIXES (before cart integration, else freeze):
  1. SPLIT RES2 (PC5, 16921 = find_clears_targeted ~6k + gravity ~6k + calc_imm): ->
     CLEAR2 (fct + RV + calc_imm + init-leaf; if cleared PC=15 else PC=6) + GRAV2 (PC15
     gravity -> PC6). Also split RES1 (PC1->CLEAR1+GRAV1 PC14) for safety; RES1's RV must
     survive the GRAV1 frame -> stash RV in RAM (ST2_RVC/RVV ~$6146/7), reload in IMM1.
  2. calc_imm: currently X=180 (180 iters ~2k). Optimize to M=180,X=RV_VIR(<=4) + M=10,
     X=RV_CELLS(<=8) with X==0 guards -> ~0.1k. (affects atomic build_search too; re-spot-check.)
  3. leaf_score_full (no-legal-p2 VALUE path, ~52k) NOT hit in test boards but WILL freeze
     if hit -> make that path phased too (rare; copy WORK1->CUR and run the leaf phases).
  4. Validate resumable == build_search(resolve='targeted') (apples-to-apples; both targeted).

## Build order
1. (measure targeted L11) 2. split readiness/setup into region phases (validate cell-exact)
3. resumable phase machine + validate vs atomic 4. cart integrate 5. live L11 test 6. cache.

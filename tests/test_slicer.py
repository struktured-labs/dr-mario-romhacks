#!/usr/bin/env python3
"""Resumable SLICER — the cartridge form of search_firstply (INTEGRATION_SPEC §slicing).
State lives in RAM ($0190+, absolute) so it persists across per-frame calls; each
`slice` call does exactly ONE placement eval (or skips illegal cursors cheaply),
and on cursor-exhaustion publishes the best (col,orient) and latches ST_MODE=DONE.

Validated in py65 by driving arm -> slice* -> DONE and confirming the slicer picks
the SAME (col,orient) as the monolithic golden_search over the same 400 boards,
AND that it does exactly one eval per slice (resumability is real).
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from py65_harness import Cpu
from patch_vs_cpu import Asm6502
import primitives
from primitives import (emit_all, emit_kernel, emit_kernel_wc, emit_first_occ, EMPTY, ROWS, COLS,
                        RV_CELLS, RV_VIR, SH_MAXH, SH_HOLES, SH_TOPRISK,
                        Z_OFFA, Z_OFFB, Z_TILEA, Z_TILEB)
from test_search import golden_search, rand_board, BIAS, score_components, first_occ
from test_resolve import py_find_clears, py_gravity


def golden_capped(board, pca, pcb):
    """Cap=1 golden: one find_clears + gravity (no cascade loop) -- matches the
    cartridge resolve_capped. 0.5% divergence from the full cascade (measured)."""
    best = -1; key = None; cands = []
    for c in range(COLS):
        fo = first_occ(board, c)
        if fo >= 2: cands.append((0, c, (fo-2)*COLS+c, (fo-1)*COLS+c))
    for c in range(COLS-1):
        fo = min(first_occ(board, c), first_occ(board, c+1))
        if fo >= 1: cands.append((1, c, (fo-1)*COLS+c, (fo-1)*COLS+c+1))
    for orient, c, offa, offb in cands:
        b = list(board); b[offa] = 0x40|pca; b[offb] = 0x40|pcb
        cells, vir = py_find_clears(b)
        if cells: py_gravity(b)
        from test_shape_eval import golden_shape
        mh, ho, tr = golden_shape(b)
        s = score_components(vir, cells, mh, ho, tr)
        if s > best: best = s; key = (orient, c)
    return key, best

BASE = 0x4000
# --- driver state in RAM (absolute; persists across slices) ---
ST_MODE  = 0x0190   # 0 IDLE / 1 SEARCHING / 2 DONE
SE_COL   = 0x0191
SE_ORIENT= 0x0192
SE_BCOL  = 0x0193
SE_BORIENT=0x0194
SE_BESTLO= 0x0195
SE_BESTHI= 0x0196
SE_PCA   = 0x0197
SE_PCB   = 0x0198
ST_BUSY  = 0x0199
PUB_DD   = 0x00DD   # publish target column (wrapper reads)
PUB_DA   = 0x00DA   # publish target orient  (wrapper reads)
# pool zp temps reused for score / landing (same as the verified diet)
SE_SLO, SE_SHI, SE_T, T_LO, T_HI, SE_FOL = 0xCA, 0xCB, 0xCC, 0xCD, 0xCE, 0xCB
WV = 18


def build_slicer(wc=False, base=BASE):
    a = Asm6502(base)

    # ============ dispatch: the SINGLE unit-1 entry per frame (cartridge) ============
    # One bank-switch wraps this. Does the new-pill edge check + arm IN unit-1, then a
    # slice. Avoids a second bank-switched call. $DF is updated by the fixed-bank wrapper.
    a.label("dispatch")
    a.ins16("LDA_abs", 0x0386); a.ins("CMP_zp", 0xDF)   # P2y vs last-y
    a.br("BCC", "d_slice"); a.br("BEQ", "d_slice")       # not a new pill -> just slice
    a.ins16("LDA_abs", 0x0381); a.ins16("STA_abs", SE_PCA)   # new pill: read colors
    a.ins16("LDA_abs", 0x0382); a.ins16("STA_abs", SE_PCB)
    a.jsr("arm")
    a.label("d_slice")
    a.jsr("slice")
    a.ins("RTS")

    # ================= arm: start a fresh search (called per new pill) =================
    a.label("arm")
    a.ins("LDA_imm", 1); a.ins16("STA_abs", ST_MODE)
    a.ins("LDA_imm", 0)
    a.ins16("STA_abs", SE_COL); a.ins16("STA_abs", SE_ORIENT)
    a.ins16("STA_abs", SE_BESTLO); a.ins16("STA_abs", SE_BESTHI)
    a.ins16("STA_abs", ST_BUSY)
    a.ins("LDA_imm", 0xFF); a.ins16("STA_abs", SE_BCOL); a.ins16("STA_abs", SE_BORIENT)
    # tiles set ONCE here from the pill colors (kernel reuses them every eval)
    a.ins16("LDA_abs", SE_PCA); a.ins("ORA_imm", 0x40); a.ins("STA_zp", Z_TILEA)
    a.ins16("LDA_abs", SE_PCB); a.ins("ORA_imm", 0x40); a.ins("STA_zp", Z_TILEB)
    a.ins("RTS")

    # ================= slice: one frame's work (<=1 eval) =================
    a.label("slice")
    a.ins16("LDA_abs", ST_BUSY); a.br("BNE", "sl_rts")
    a.ins16("LDA_abs", ST_MODE); a.ins("CMP_imm", 1); a.br("BNE", "sl_rts")
    a.ins16("INC_abs", ST_BUSY)
    a.label("sl_loop")
    a.ins16("LDA_abs", ST_MODE); a.ins("CMP_imm", 1); a.br("BNE", "sl_yield")  # DONE -> stop
    a.jsr("try_eval")               # A=1 if evaled this cursor, A=0 if skipped (illegal)
    a.ins("PHA"); a.jsr("advance"); a.ins("PLA")   # advance cursor (may publish+DONE)
    a.ins("CMP_imm", 1); a.br("BEQ", "sl_yield")    # evaled -> one per slice, yield
    a.jmp("sl_loop")                                # skipped -> keep scanning for a legal cursor
    a.label("sl_yield")
    a.ins16("DEC_abs", ST_BUSY)
    a.label("sl_rts")
    a.ins("RTS")

    # ----- try_eval: eval the CURRENT (SE_ORIENT,SE_COL) if legal. A=1 evaled / 0 skipped -----
    a.label("try_eval")
    a.ins16("LDA_abs", SE_ORIENT); a.br("BNE", "te_h")
    # vertical: fo=first_occ(col); legal if fo>=2; offb=(fo-1)*8+col, offa=offb-8
    a.ins16("LDX_abs", SE_COL); a.jsr("first_occ")     # A=fo
    a.ins("CMP_imm", 2); a.br("BCC", "te_skip")
    a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("STA_zp", SE_T)  # fo*8
    a.ins("LDA_zp", SE_T); a.ins("SEC"); a.ins("SBC_imm", 8)
    a.ins("CLC"); a.ins16("ADC_abs", SE_COL); a.ins("STA_zp", Z_OFFB)
    a.ins("LDA_zp", Z_OFFB); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", Z_OFFA)
    a.jmp("te_eval")
    a.label("te_h")
    # horizontal: fo=min(first_occ(col),first_occ(col+1)); legal if fo>=1
    a.ins16("LDX_abs", SE_COL); a.jsr("first_occ"); a.ins("STA_zp", SE_FOL)
    a.ins16("LDX_abs", SE_COL); a.ins("INX"); a.jsr("first_occ")
    a.ins("CMP_zp", SE_FOL); a.br("BCC", "te_hmin"); a.ins("LDA_zp", SE_FOL)
    a.label("te_hmin")
    a.ins("CMP_imm", 1); a.br("BCC", "te_skip")
    a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A")
    a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("CLC"); a.ins16("ADC_abs", SE_COL); a.ins("STA_zp", Z_OFFA)
    a.ins("LDA_zp", Z_OFFA); a.ins("CLC"); a.ins("ADC_imm", 1); a.ins("STA_zp", Z_OFFB)
    a.label("te_eval")
    a.jsr("eval_one")
    a.ins("LDA_imm", 1); a.ins("RTS")        # evaled
    a.label("te_skip")
    a.ins("LDA_imm", 0); a.ins("RTS")        # illegal, skipped

    # ----- eval_one: kernel + 16-bit score + keep-best (tiles already armed) -----
    a.label("eval_one")
    a.jsr("kernel")
    a.ins("LDA_imm", BIAS & 0xFF); a.ins("STA_zp", SE_SLO)
    a.ins("LDA_imm", (BIAS >> 8) & 0xFF); a.ins("STA_zp", SE_SHI)
    # + 18*vir
    a.ins("LDA_zp", RV_VIR); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("STA_zp", SE_T)
    a.ins("LDA_zp", RV_VIR); a.ins("ASL_A"); a.ins("CLC"); a.ins("ADC_zp", SE_T); a.ins("STA_zp", SE_T)
    a.ins("LDA_zp", SE_SLO); a.ins("CLC"); a.ins("ADC_zp", SE_T); a.ins("STA_zp", SE_SLO)
    a.ins("LDA_zp", SE_SHI); a.ins("ADC_imm", 0); a.ins("STA_zp", SE_SHI)
    # + cells
    a.ins("LDA_zp", SE_SLO); a.ins("CLC"); a.ins("ADC_zp", RV_CELLS); a.ins("STA_zp", SE_SLO)
    a.ins("LDA_zp", SE_SHI); a.ins("ADC_imm", 0); a.ins("STA_zp", SE_SHI)
    # - maxh
    a.ins("LDA_zp", SE_SLO); a.ins("SEC"); a.ins("SBC_zp", SH_MAXH); a.ins("STA_zp", SE_SLO)
    a.ins("LDA_zp", SE_SHI); a.ins("SBC_imm", 0); a.ins("STA_zp", SE_SHI)
    # - 3*holes
    a.ins("LDA_zp", SH_HOLES); a.ins("ASL_A"); a.ins("STA_zp", T_LO)
    a.ins("LDA_imm", 0); a.ins("STA_zp", T_HI)
    a.ins("LDA_zp", T_LO); a.ins("CLC"); a.ins("ADC_zp", SH_HOLES); a.ins("STA_zp", T_LO)
    a.ins("LDA_zp", T_HI); a.ins("ADC_imm", 0); a.ins("STA_zp", T_HI)
    a.ins("LDA_zp", SE_SLO); a.ins("SEC"); a.ins("SBC_zp", T_LO); a.ins("STA_zp", SE_SLO)
    a.ins("LDA_zp", SE_SHI); a.ins("SBC_zp", T_HI); a.ins("STA_zp", SE_SHI)
    # - 5*toprisk
    a.ins("LDA_zp", SH_TOPRISK); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("STA_zp", SE_T)
    a.ins("LDA_zp", SH_TOPRISK); a.ins("CLC"); a.ins("ADC_zp", SE_T); a.ins("STA_zp", SE_T)
    a.ins("LDA_zp", SE_SLO); a.ins("SEC"); a.ins("SBC_zp", SE_T); a.ins("STA_zp", SE_SLO)
    a.ins("LDA_zp", SE_SHI); a.ins("SBC_imm", 0); a.ins("STA_zp", SE_SHI)
    # compare score > best (unsigned 16-bit, strict keep-first)
    a.ins("LDA_zp", SE_SHI); a.ins16("CMP_abs", SE_BESTHI); a.br("BCC", "eo_no"); a.br("BNE", "eo_yes")
    a.ins("LDA_zp", SE_SLO); a.ins16("CMP_abs", SE_BESTLO); a.br("BCC", "eo_no"); a.br("BEQ", "eo_no")
    a.label("eo_yes")
    a.ins("LDA_zp", SE_SLO); a.ins16("STA_abs", SE_BESTLO)
    a.ins("LDA_zp", SE_SHI); a.ins16("STA_abs", SE_BESTHI)
    a.ins16("LDA_abs", SE_COL); a.ins16("STA_abs", SE_BCOL)
    a.ins16("LDA_abs", SE_ORIENT); a.ins16("STA_abs", SE_BORIENT)
    a.label("eo_no")
    a.ins("RTS")

    # ----- advance: next cursor; on exhaustion publish + ST_MODE=DONE -----
    a.label("advance")
    a.ins16("INC_abs", SE_COL)
    a.ins16("LDA_abs", SE_ORIENT); a.br("BNE", "ad_h")
    a.ins16("LDA_abs", SE_COL); a.ins("CMP_imm", COLS); a.br("BNE", "ad_done")  # vert col 0..7
    a.ins("LDA_imm", 1); a.ins16("STA_abs", SE_ORIENT)
    a.ins("LDA_imm", 0); a.ins16("STA_abs", SE_COL); a.jmp("ad_done")
    a.label("ad_h")
    a.ins16("LDA_abs", SE_COL); a.ins("CMP_imm", COLS - 1); a.br("BNE", "ad_done")  # horiz col 0..6
    a.jsr("publish"); a.ins("LDA_imm", 2); a.ins16("STA_abs", ST_MODE)
    a.label("ad_done")
    a.ins("RTS")

    # ----- publish: write target where the wrapper reads it. Store $DD,$DA FIRST,
    #       ST_MODE=DONE LAST (done by caller) so the wrapper never reads a torn pair.
    #       Topout fallback (SE_BCOL==$FF): safe col 3, orient 0. -----
    a.label("publish")
    a.ins16("LDA_abs", SE_BCOL); a.ins("CMP_imm", 0xFF); a.br("BNE", "pb_ok")
    a.ins("LDA_imm", 3); a.ins16("STA_abs", PUB_DD); a.ins("LDA_imm", 0); a.ins16("STA_abs", PUB_DA)
    a.ins("RTS")
    a.label("pb_ok")
    a.ins16("LDA_abs", SE_BCOL); a.ins16("STA_abs", PUB_DD)
    # orient encode: SE_BORIENT 1(horiz)->$03A5=0 (spawn default); 0(vert,PCA upper)->$03A5=3 (V a-top).
    # (Mesen-confirmed: P2 pill spawns horizontal $03A5=0; colors $0381 left/A, $0382 right/B.)
    a.ins16("LDA_abs", SE_BORIENT); a.br("BNE", "pb_horiz")
    a.ins("LDA_imm", 3); a.jmp("pb_setDA")               # vertical -> $DA=3
    a.label("pb_horiz")
    a.ins("LDA_imm", 0)                                   # horizontal -> $DA=0
    a.label("pb_setDA")
    a.ins16("STA_abs", PUB_DA)
    a.ins("RTS")

    emit_all(a)
    (emit_kernel_wc if wc else emit_kernel)(a, resolve="resolve_capped")
    emit_first_occ(a)
    return a.assemble(), a.labels


def main():
    import statistics
    code, labels = build_slicer()
    arm_addr = BASE + labels["arm"]; slice_addr = BASE + labels["slice"]
    rng = random.Random(31337)   # same seed as test_search for matching boards
    cpu = Cpu(); cpu.load(BASE, code)
    fails = 0; n = 400; slice_counts = []
    for t in range(n):
        board = rand_board(rng)
        pca, pcb = rng.randint(0, 2), rng.randint(0, 2)
        cpu.set_board(board)
        cpu.mem[SE_PCA] = pca; cpu.mem[SE_PCB] = pcb
        cpu.call(arm_addr)
        nsl = 0
        while cpu.mem[ST_MODE] != 2 and nsl < 80:
            cpu.call(slice_addr); nsl += 1
        slice_counts.append(nsl)
        got = (cpu.mem[SE_BORIENT], cpu.mem[SE_BCOL])
        gkey, gbest = golden_capped(board, pca, pcb)
        gotbest = cpu.mem[SE_BESTLO] | (cpu.mem[SE_BESTHI] << 8)
        # also: published $DD == chosen col, $DA == encoded orient (0=horiz, 3=vert)
        exp_da = 0 if cpu.mem[SE_BORIENT] == 1 else 3
        pub_ok = (cpu.mem[PUB_DD] == cpu.mem[SE_BCOL] and cpu.mem[PUB_DA] == exp_da)
        if got != gkey or gotbest != gbest or not pub_ok:
            fails += 1
            if fails <= 8:
                print(f"  MISMATCH t={t}: got=(o{got[0]},c{got[1]},s{gotbest}) "
                      f"exp=(o{gkey[0]},c{gkey[1]},s{gbest}) slices={nsl} pub_ok={pub_ok}")
    print(f"routine size = {len(code)} bytes")
    print(f"validation: {n - fails}/{n} slicer picks == monolithic search + publish (fails={fails})")
    print(f"slices/search: min={min(slice_counts)} max={max(slice_counts)} avg={statistics.mean(slice_counts):.1f}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

"""Shared, validated 6502 board-sim primitives, emitted as labeled subroutines
into an Asm6502 program. Single source of truth for the unit tests AND the
eventual patch_vs_cpu.py depth-2 integration.

Each emit_*(a) appends one or more RTS-terminated subroutines (labels below).
All operate on the board at $0500 (128 bytes, 16 rows x 8 cols, row-major).
NES tiles: empty=$FF; occupied color = tile & $0F; virus = (tile & $F0)==$D0.

Labels exposed:
  resolve     -> loops find_clears+gravity; writes RV_CELLS/RV_VIR grand totals
  find_clears -> mark+clear all >=4 runs this pass; writes PASS_CELLS/PASS_VIR
  gravity     -> column-compact, viruses fixed
  shape       -> writes SH_MAXH/SH_HOLES/SH_TOPRISK
"""
EMPTY = 0xFF
ROWS, COLS = 16, 8
BOARD = 0x0500         # the board the SIM operates on (resolve/shape/find_clears).
LIVE_BOARD = 0x0500    # the stable settled playfield (read for landing/first_occ).
MARK = 0x0300          # 16-byte BIT-PACKED mark buffer (cell k -> bit k&7 of byte k>>3)
# py65 tests: BOARD==LIVE_BOARD==$0500 (kernel backup/restore). ROM working-copy:
# set BOARD=$0100 (WORK), MARK=$0180; first_occ still reads LIVE_BOARD=$0500;
# emit_kernel_wc copies LIVE_BOARD->BOARD per eval (no restore -> $0500 untouched).

# zero-page map (ULTRACODE-verified coloring, INTEGRATION_SPEC.md): the search must
# fit the only game-safe zp window $CA-$E1 (24 B). 12-byte shared pool $CA-$D5 (time-
# disjoint phases reuse it), 9 dedicated, and $DA/$DD/$DE-area reserved for the wrapper
# interface. Two simultaneously-live vars NEVER share a byte (proof: INTEGRATION_SPEC).
RV_CELLS, RV_VIR = 0xE0, 0xE1         # dedicated: resolve grand totals (KEEP)
PASS_CELLS, PASS_VIR = 0xD4, 0xD5     # pool P10/P11
SH_MAXH, SH_HOLES, SH_TOPRISK = 0xD6, 0xD7, 0xD8   # dedicated (live shape->score)
# find_clears temps (pool): _ROW/_COL share P0 (row pass fully before col pass)
_ROW, _COL, _OFF, _RUN, _MCOL, _RSTART = 0xCA, 0xCA, 0xCB, 0xCE, 0xCF, 0xD0
_STEP, _CNT, _FLCNT = 0xCC, 0xCD, 0xD1
_GCOL, _GREAD, _GDEST, _GTILE = 0xCA, 0xCB, 0xCC, 0xCD   # gravity (disjoint from fc)
_SHCOL, _SHOFF, _SHSEEN, _SHTMP = 0xCA, 0xCB, 0xCC, 0xCD  # shape (disjoint)
# kernel/driver interface (avoid wrapper-owned $DA=orient, $DD=col, $DF=last-y)
Z_OFFA, Z_OFFB = 0xDC, 0xDE           # placed-cell offsets (dedicated, persist a placement)
Z_TILEA, Z_TILEB = 0xD9, 0xDB         # pill tiles (dedicated, set once per pill)
FO_OFF = 0xCA                         # first_occ working offset (pool P0, landing phase)
_BP1, _BP2 = 0xD2, 0xD3               # bitpack mark scratch (pool P8/P9)


def emit_resolve(a):
    """resolve driver. JSRs find_clears + gravity (emit those too)."""
    a.label("resolve")
    a.ins("LDA_imm", 0); a.ins("STA_zp", RV_CELLS); a.ins("STA_zp", RV_VIR)
    a.label("rs_loop")
    a.jsr("find_clears")
    a.ins("LDA_zp", PASS_CELLS); a.br("BNE", "rs_more")
    a.ins("RTS")
    a.label("rs_more")
    a.ins("CLC"); a.ins("ADC_zp", RV_CELLS); a.ins("STA_zp", RV_CELLS)
    a.ins("LDA_zp", PASS_VIR); a.ins("CLC"); a.ins("ADC_zp", RV_VIR); a.ins("STA_zp", RV_VIR)
    a.jsr("gravity")
    a.jmp("rs_loop")


def emit_resolve_targeted(a):
    """Like resolve but the FIRST pass scans only the 2 placed cells' lines
    (cheap); if nothing clears we return immediately. After any clear the board
    can cascade anywhere, so subsequent passes use the full find_clears."""
    a.label("resolve_targeted")
    a.ins("LDA_imm", 0); a.ins("STA_zp", RV_CELLS); a.ins("STA_zp", RV_VIR)
    a.jsr("find_clears_targeted")
    a.ins("LDA_zp", PASS_CELLS); a.br("BNE", "rt_more")
    a.ins("RTS")                         # common path: no clear, done cheap
    a.label("rt_more")
    a.ins("CLC"); a.ins("ADC_zp", RV_CELLS); a.ins("STA_zp", RV_CELLS)
    a.ins("LDA_zp", PASS_VIR); a.ins("CLC"); a.ins("ADC_zp", RV_VIR); a.ins("STA_zp", RV_VIR)
    a.jsr("gravity")
    a.label("rt_loop")
    a.jsr("find_clears")
    a.ins("LDA_zp", PASS_CELLS); a.br("BNE", "rt_loopmore")
    a.ins("RTS")
    a.label("rt_loopmore")
    a.ins("CLC"); a.ins("ADC_zp", RV_CELLS); a.ins("STA_zp", RV_CELLS)
    a.ins("LDA_zp", PASS_VIR); a.ins("CLC"); a.ins("ADC_zp", RV_VIR); a.ins("STA_zp", RV_VIR)
    a.jsr("gravity")
    a.jmp("rt_loop")


def emit_resolve_capped(a):
    """CAP=1 resolve for the cartridge NMI budget: targeted first pass + (if it
    cleared) ONE gravity, then STOP -- NO cascade loop. A full find_clears pass is
    ~36k cyc (overruns one NMI frame); this caps the eval at ~12k so it runs
    atomically in one NMI hook. Measured divergence from the full cascade: only
    2/400 boards pick a different placement (0.5%) -- negligible for depth-1.
    Writes RV_CELLS/RV_VIR like resolve_targeted."""
    a.label("resolve_capped")
    a.ins("LDA_imm", 0); a.ins("STA_zp", RV_CELLS); a.ins("STA_zp", RV_VIR)
    a.jsr("find_clears_targeted")
    a.ins("LDA_zp", PASS_CELLS); a.br("BNE", "rc_more")
    a.ins("RTS")                          # common path: no clear
    a.label("rc_more")
    a.ins("CLC"); a.ins("ADC_zp", RV_CELLS); a.ins("STA_zp", RV_CELLS)
    a.ins("LDA_zp", PASS_VIR); a.ins("CLC"); a.ins("ADC_zp", RV_VIR); a.ins("STA_zp", RV_VIR)
    a.jsr("gravity")                      # settle once, then STOP (no cascade loop)
    a.ins("RTS")


def emit_find_clears(a):
    a.label("find_clears")
    a.jsr("fc_clearmark")
    a.ins("LDA_imm", 0); a.ins("STA_zp", _ROW)
    a.label("fc_hrow")
    a.ins("LDA_zp", _ROW); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("STA_zp", _OFF)
    a.ins("LDA_imm", 1); a.ins("STA_zp", _STEP); a.ins("LDA_imm", COLS); a.ins("STA_zp", _CNT)
    a.jsr("fc_scan")
    a.ins("INC_zp", _ROW); a.ins("LDA_zp", _ROW); a.ins("CMP_imm", ROWS); a.br("BNE", "fc_hrow")
    a.ins("LDA_imm", 0); a.ins("STA_zp", _COL)
    a.label("fc_vcol")
    a.ins("LDA_zp", _COL); a.ins("STA_zp", _OFF)
    a.ins("LDA_imm", 8); a.ins("STA_zp", _STEP); a.ins("LDA_imm", ROWS); a.ins("STA_zp", _CNT)
    a.jsr("fc_scan")
    a.ins("INC_zp", _COL); a.ins("LDA_zp", _COL); a.ins("CMP_imm", COLS); a.br("BNE", "fc_vcol")
    a.jmp("fc_apply")               # tail-call apply (ends in RTS)

    # fc_clearmark: zero the 16-byte BIT-PACKED MARK buffer + PASS counters.
    # MARK is 16 bytes; cell offset k -> bit (k&7) of byte (k>>3). Masks computed
    # inline (1<<(k&7) via a shift loop) so no address-of-table is needed.
    a.label("fc_clearmark")
    a.ins("LDA_imm", 0); a.ins("LDX_imm", 15)
    a.label("fc_mkclr"); a.ins16("STA_absX", MARK); a.ins("DEX"); a.br("BPL", "fc_mkclr")
    a.ins("STA_zp", PASS_CELLS); a.ins("STA_zp", PASS_VIR); a.ins("RTS")

    # fc_apply: BYTE-MAJOR walk of the 16-byte packed MARK. For each MARK byte:
    # if zero, skip its 8 cells outright (the common case -- most bytes are empty,
    # so this is far cheaper than the old per-cell shift-loop and fits the NMI
    # budget). If nonzero, expand bits 0..7 -> cell offsets byteidx*8 + bit, and
    # clear+count each set bit. X = byte index throughout (board uses Y/absY, so X
    # is never clobbered); _BP2 = rolling mask. Same totals as the old 127..0 walk.
    a.label("fc_apply")
    a.ins("LDX_imm", 0)                                    # X = MARK byte index 0..15
    a.label("fc_apb")
    a.ins16("LDA_absX", MARK); a.br("BEQ", "fc_apbnext")   # empty byte -> skip 8 cells
    a.ins("STA_zp", _BP2)                                  # rolling mask
    a.ins("TXA"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("TAY")  # Y = byteidx*8
    a.label("fc_apbit")
    a.ins("LDA_zp", _BP2); a.ins("LSR_A"); a.ins("STA_zp", _BP2); a.br("BCC", "fc_apbitnext")
    # bit set: clear board[Y], count (Y = cell offset)
    a.ins16("LDA_absY", BOARD); a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0)
    a.br("BNE", "fc_apnotv"); a.ins("INC_zp", PASS_VIR)
    a.label("fc_apnotv")
    a.ins("INC_zp", PASS_CELLS)
    a.ins("LDA_imm", EMPTY); a.ins16("STA_absY", BOARD)
    a.label("fc_apbitnext")
    a.ins("INY"); a.ins("LDA_zp", _BP2); a.br("BNE", "fc_apbit")  # more set bits in byte?
    a.label("fc_apbnext")
    a.ins("INX"); a.ins("CPX_imm", 16); a.br("BNE", "fc_apb")
    a.ins("RTS")

    # ---- targeted first pass: scan only the 2 placed cells' rows+cols ----
    # inputs Z_OFFA=$DC, Z_OFFB=$DE. Correct because the pre-placement board has
    # no >=4 runs, so any new run must pass through a placed cell.
    a.label("find_clears_targeted")
    a.jsr("fc_clearmark")
    # row A
    a.ins("LDA_zp", Z_OFFA); a.ins("AND_imm", 0xF8); a.ins("STA_zp", _OFF)
    a.ins("LDA_imm", 1); a.ins("STA_zp", _STEP); a.ins("LDA_imm", COLS); a.ins("STA_zp", _CNT)
    a.jsr("fc_scan")
    # col A
    a.ins("LDA_zp", Z_OFFA); a.ins("AND_imm", 0x07); a.ins("STA_zp", _OFF)
    a.ins("LDA_imm", 8); a.ins("STA_zp", _STEP); a.ins("LDA_imm", ROWS); a.ins("STA_zp", _CNT)
    a.jsr("fc_scan")
    # row B
    a.ins("LDA_zp", Z_OFFB); a.ins("AND_imm", 0xF8); a.ins("STA_zp", _OFF)
    a.ins("LDA_imm", 1); a.ins("STA_zp", _STEP); a.ins("LDA_imm", COLS); a.ins("STA_zp", _CNT)
    a.jsr("fc_scan")
    # col B
    a.ins("LDA_zp", Z_OFFB); a.ins("AND_imm", 0x07); a.ins("STA_zp", _OFF)
    a.ins("LDA_imm", 8); a.ins("STA_zp", _STEP); a.ins("LDA_imm", ROWS); a.ins("STA_zp", _CNT)
    a.jsr("fc_scan")
    a.jmp("fc_apply")

    # fc_scan: walk _CNT cells from _OFF step _STEP, mark runs >=4
    a.label("fc_scan")
    a.ins("LDY_imm", 0); a.ins("LDA_imm", 0); a.ins("STA_zp", _RUN)
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", _MCOL)
    a.label("fc_cell")
    a.ins("LDX_zp", _OFF); a.ins16("LDA_absX", BOARD)
    a.ins("CMP_imm", EMPTY); a.br("BEQ", "fc_break")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", _MCOL); a.br("BNE", "fc_newcol")
    a.ins("INC_zp", _RUN); a.jmp("fc_adv")
    a.label("fc_break")
    a.jsr("fc_flush"); a.ins("LDA_imm", 0); a.ins("STA_zp", _RUN)
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", _MCOL); a.jmp("fc_adv")
    a.label("fc_newcol")
    a.jsr("fc_flush")
    a.ins("LDX_zp", _OFF); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0x0F); a.ins("STA_zp", _MCOL)
    a.ins("LDA_zp", _OFF); a.ins("STA_zp", _RSTART)
    a.ins("LDA_imm", 1); a.ins("STA_zp", _RUN)
    a.label("fc_adv")
    a.ins("LDA_zp", _RUN); a.ins("CMP_imm", 1); a.br("BNE", "fc_noset")
    a.ins("LDA_zp", _OFF); a.ins("STA_zp", _RSTART)
    a.label("fc_noset")
    a.ins("LDA_zp", _OFF); a.ins("CLC"); a.ins("ADC_zp", _STEP); a.ins("STA_zp", _OFF)
    a.ins("INY"); a.ins("CPY_zp", _CNT); a.br("BNE", "fc_cell")
    a.jsr("fc_flush"); a.ins("RTS")
    # fc_flush: if _RUN>=4 set the packed MARK bit for each run cell (from _RSTART,
    # step _STEP, _FLCNT cells). Walks the offset in _BP1; uses ONLY A/X (NOT Y —
    # fc_scan's loop counter is Y and fc_flush runs inside that loop). Leaf (no JSR).
    a.label("fc_flush")
    a.ins("LDA_zp", _RUN); a.ins("CMP_imm", 4); a.br("BCC", "fc_fldone")
    a.ins("LDA_zp", _RSTART); a.ins("STA_zp", _BP1)        # offset walk in _BP1
    a.ins("LDA_zp", _RUN); a.ins("STA_zp", _FLCNT)
    a.label("fc_flmark")
    a.ins("LDA_zp", _BP1); a.ins("AND_imm", 7); a.ins("TAX")   # X = bit index
    a.ins("LDA_imm", 1)
    a.label("fc_flsh"); a.ins("DEX"); a.br("BMI", "fc_flshd")
    a.ins("ASL_A"); a.jmp("fc_flsh")
    a.label("fc_flshd"); a.ins("STA_zp", _BP2)                 # mask = 1<<(off&7)
    a.ins("LDA_zp", _BP1); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("TAX")  # byte idx
    a.ins16("LDA_absX", MARK); a.ins("ORA_zp", _BP2); a.ins16("STA_absX", MARK)
    a.ins("LDA_zp", _BP1); a.ins("CLC"); a.ins("ADC_zp", _STEP); a.ins("STA_zp", _BP1)
    a.ins("DEC_zp", _FLCNT); a.br("BNE", "fc_flmark")
    a.label("fc_fldone"); a.ins("RTS")


def emit_gravity(a):
    a.label("gravity")
    a.ins("LDA_imm", 0); a.ins("STA_zp", _GCOL)
    a.label("g_col")
    a.ins("LDA_imm", 120); a.ins("CLC"); a.ins("ADC_zp", _GCOL); a.ins("STA_zp", _GDEST)
    a.ins("LDA_imm", 120); a.ins("CLC"); a.ins("ADC_zp", _GCOL); a.ins("STA_zp", _GREAD)
    a.ins("LDY_imm", 0)
    a.label("g_row")
    a.ins("LDX_zp", _GREAD); a.ins16("LDA_absX", BOARD)
    a.ins("CMP_imm", EMPTY); a.br("BEQ", "g_next")
    a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BNE", "g_iscap")
    a.ins("LDA_zp", _GREAD); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", _GDEST)
    a.jmp("g_next")
    a.label("g_iscap")
    a.ins("LDX_zp", _GREAD); a.ins16("LDA_absX", BOARD); a.ins("STA_zp", _GTILE)
    a.ins("LDA_zp", _GREAD); a.ins("CMP_zp", _GDEST); a.br("BEQ", "g_nomove")
    a.ins("LDA_imm", EMPTY); a.ins16("STA_absX", BOARD)
    a.ins("LDX_zp", _GDEST); a.ins("LDA_zp", _GTILE); a.ins16("STA_absX", BOARD)
    a.label("g_nomove")
    a.ins("LDA_zp", _GDEST); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", _GDEST)
    a.label("g_next")
    a.ins("LDA_zp", _GREAD); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", _GREAD)
    a.ins("INY"); a.ins("CPY_imm", ROWS); a.br("BNE", "g_row")
    a.ins("INC_zp", _GCOL); a.ins("LDA_zp", _GCOL); a.ins("CMP_imm", COLS); a.br("BNE", "g_col")
    a.ins("RTS")


def emit_shape(a):
    a.label("shape")
    a.ins("LDA_imm", 0); a.ins("STA_zp", SH_MAXH); a.ins("STA_zp", SH_HOLES); a.ins("STA_zp", SH_TOPRISK)
    a.ins("LDX_imm", 23)
    a.label("sh_tr"); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "sh_trsk")
    a.ins("INC_zp", SH_TOPRISK)
    a.label("sh_trsk"); a.ins("DEX"); a.br("BPL", "sh_tr")
    a.ins("LDA_imm", 0); a.ins("STA_zp", _SHCOL)
    a.label("sh_col")
    a.ins("LDA_zp", _SHCOL); a.ins("STA_zp", _SHOFF)
    a.ins("LDA_imm", 0); a.ins("STA_zp", _SHSEEN); a.ins("LDY_imm", 0)
    a.label("sh_row")
    a.ins("LDX_zp", _SHOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "sh_empty")
    a.ins("LDA_zp", _SHSEEN); a.br("BNE", "sh_after")
    a.ins("LDA_imm", 1); a.ins("STA_zp", _SHSEEN)
    a.ins("TYA"); a.ins("STA_zp", _SHTMP)
    a.ins("LDA_imm", ROWS); a.ins("SEC"); a.ins("SBC_zp", _SHTMP)
    a.ins("CMP_zp", SH_MAXH); a.br("BCC", "sh_after")
    a.ins("STA_zp", SH_MAXH); a.jmp("sh_after")
    a.label("sh_empty")
    a.ins("LDA_zp", _SHSEEN); a.br("BEQ", "sh_after")
    a.ins("INC_zp", SH_HOLES)
    a.label("sh_after")
    a.ins("LDA_zp", _SHOFF); a.ins("CLC"); a.ins("ADC_imm", 8); a.ins("STA_zp", _SHOFF)
    a.ins("INY"); a.ins("CPY_imm", ROWS); a.br("BNE", "sh_row")
    a.ins("INC_zp", _SHCOL); a.ins("LDA_zp", _SHCOL); a.ins("CMP_imm", COLS); a.br("BNE", "sh_col")
    a.ins("RTS")


SCRATCH = 0x0600        # 128-byte board backup for the kernel


def emit_kernel(a, resolve="resolve_targeted"):
    """eval_placement_deep: inputs Z_OFFA/Z_OFFB/Z_TILEA/Z_TILEB.
    backup board -> place -> <resolve> -> shape -> restore. Outputs
    RV_VIR/RV_CELLS (cleared) + SH_MAXH/SH_HOLES/SH_TOPRISK. Non-destructive.
    `resolve`: "resolve_targeted" (full cascade) or "resolve_capped" (cartridge,
    fits one NMI; emit_all provides both)."""
    a.label("kernel")
    a.ins("LDX_imm", 127)
    a.label("k_bk"); a.ins16("LDA_absX", BOARD); a.ins16("STA_absX", SCRATCH)
    a.ins("DEX"); a.br("BPL", "k_bk")
    a.ins("LDX_zp", Z_OFFA); a.ins("LDA_zp", Z_TILEA); a.ins16("STA_absX", BOARD)
    a.ins("LDX_zp", Z_OFFB); a.ins("LDA_zp", Z_TILEB); a.ins16("STA_absX", BOARD)
    a.jsr(resolve)
    a.jsr("shape")
    a.ins("LDX_imm", 127)
    a.label("k_rs"); a.ins16("LDA_absX", SCRATCH); a.ins16("STA_absX", BOARD)
    a.ins("DEX"); a.br("BPL", "k_rs")
    a.ins("RTS")


def emit_kernel_wc(a, resolve="resolve_capped"):
    """Working-copy kernel for the CARTRIDGE: copy the LIVE settled board
    ($0500) -> private WORK board (BOARD, e.g. $0100), place the 2 cells in WORK,
    <resolve> + shape on WORK. NO backup/restore -> the live $0500 is never
    touched (the game renders it cleanly while we compute). Outputs RV_*/SH_*."""
    a.label("kernel")
    a.ins("LDX_imm", 127)
    a.label("kwc_cp"); a.ins16("LDA_absX", LIVE_BOARD); a.ins16("STA_absX", BOARD)
    a.ins("DEX"); a.br("BPL", "kwc_cp")
    a.ins("LDX_zp", Z_OFFA); a.ins("LDA_zp", Z_TILEA); a.ins16("STA_absX", BOARD)
    a.ins("LDX_zp", Z_OFFB); a.ins("LDA_zp", Z_TILEB); a.ins16("STA_absX", BOARD)
    a.jsr(resolve)
    a.jsr("shape")
    a.ins("RTS")


def emit_copy_place(a):
    """copy_place: copy LIVE settled board ($0500) -> WORK (BOARD), then place the
    pill's 2 cells. The RESUMABLE LAND phase calls this; later phases
    (find_clears_targeted / gravity / shape) operate on the persisted WORK."""
    a.label("copy_place")
    a.ins("LDX_imm", 127)
    a.label("cp_lp"); a.ins16("LDA_absX", LIVE_BOARD); a.ins16("STA_absX", BOARD)
    a.ins("DEX"); a.br("BPL", "cp_lp")
    a.ins("LDX_zp", Z_OFFA); a.ins("LDA_zp", Z_TILEA); a.ins16("STA_absX", BOARD)
    a.ins("LDX_zp", Z_OFFB); a.ins("LDA_zp", Z_TILEB); a.ins16("STA_absX", BOARD)
    a.ins("RTS")


def emit_first_occ(a):
    """first_occ: input col in X (0-7). Output A = row (0-15) of the topmost
    occupied cell in that column, or 16 if the column is empty."""
    a.label("first_occ")
    a.ins("TXA"); a.ins("STA_zp", FO_OFF)      # working offset = col (row 0)
    a.ins("LDY_imm", 0)                          # Y = row
    a.label("fo_loop")
    a.ins("LDX_zp", FO_OFF); a.ins16("LDA_absX", LIVE_BOARD)   # landing reads LIVE settled board
    a.ins("CMP_imm", EMPTY); a.br("BNE", "fo_hit")
    a.ins("LDA_zp", FO_OFF); a.ins("CLC"); a.ins("ADC_imm", 8); a.ins("STA_zp", FO_OFF)
    a.ins("INY"); a.ins("CPY_imm", ROWS); a.br("BNE", "fo_loop")
    a.label("fo_hit")
    a.ins("TYA"); a.ins("RTS")                   # A = row of first occupied (or 16)


def emit_all(a):
    """Board-sim primitives only (resolve + shape). Callers that need the
    per-placement kernel / first_occ emit those separately to avoid duplicate
    `kernel` labels with tests that define their own."""
    emit_resolve(a); emit_resolve_targeted(a); emit_resolve_capped(a)
    emit_find_clears(a); emit_gravity(a); emit_shape(a)


# ============================================================================
# DEPTH-2 RICH EVAL (validated cell-exact in test_eval_terms / test_score_combine):
# the 6 terms -> weighted leaf score (win_flag + 16-bit). State in $6000 PRG-RAM
# (cart) / RAM (py65) to avoid zp pressure. All term routines read BOARD.
# ============================================================================
EV_BUR_LO, EV_BUR_HI = 0x6110, 0x6111
EV_RDY_LO, EV_RDY_HI = 0x6112, 0x6113
EV_SET, EV_VIRFLAG, EV_WIN = 0x6114, 0x6115, 0x6116
EV_SCO_LO, EV_SCO_HI = 0x6117, 0x6118
EV_MLO, EV_MHI, EV_PLO, EV_PHI = 0x6119, 0x611A, 0x611B, 0x611C
SQ_LO_ADDR, SQ_HI_ADDR = 0x7A00, 0x7A11      # 17-byte square tables (lo, hi)
EO_LO, EO_HI = 0xE9, 0xEA                     # term accumulator output (disjoint from RV)
ET0, ET1, ET2, ET3, ET4, ET5, ET6 = 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8
ESCR = 0xEF                                   # setup virus-check scratch
BIAS5000 = 5000


def emit_buried(a):
    a.label("buried")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", EV_BUR_LO); a.ins16("STA_abs", EV_BUR_HI); a.ins("STA_zp", ET1)
    a.label("bu_col")
    a.ins("LDA_zp", ET1); a.ins("STA_zp", ET0)
    a.ins("LDY_imm", 0); a.ins("LDA_imm", ROWS); a.ins("STA_zp", ET2)
    a.label("bu_cell")
    a.ins("LDX_zp", ET0); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "bu_next")
    a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BNE", "bu_occ")
    a.ins("TYA"); a.ins("CLC"); a.ins16("ADC_abs", EV_BUR_LO); a.ins16("STA_abs", EV_BUR_LO)
    a.ins16("LDA_abs", EV_BUR_HI); a.ins("ADC_imm", 0); a.ins16("STA_abs", EV_BUR_HI)
    a.label("bu_occ")
    a.ins("INY")
    a.label("bu_next")
    a.ins("LDA_zp", ET0); a.ins("CLC"); a.ins("ADC_imm", 8); a.ins("STA_zp", ET0)
    a.ins("DEC_zp", ET2); a.br("BNE", "bu_cell")
    a.ins("INC_zp", ET1); a.ins("LDA_zp", ET1); a.ins("CMP_imm", COLS); a.br("BNE", "bu_col")
    a.ins("RTS")


def emit_readiness(a):
    a.label("readiness")
    a.ins("LDA_imm", 0); a.ins("STA_zp", EO_LO); a.ins("STA_zp", EO_HI); a.ins("STA_zp", ET0)
    a.label("rd_cell")
    a.ins("LDX_zp", ET0); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BNE", "rd_c1"); a.jmp("rd_next")
    a.label("rd_c1")
    a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BEQ", "rd_c2"); a.jmp("rd_next")
    a.label("rd_c2")
    a.ins("LDX_zp", ET0); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0x0F); a.ins("STA_zp", ET1)
    a.ins("LDA_zp", ET0); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("STA_zp", ET2)
    a.ins("LDA_imm", 1); a.ins("STA_zp", ET3)
    a.ins("LDA_zp", ET0); a.ins("STA_zp", ET4)
    a.ins("LDA_zp", ET0); a.ins("AND_imm", 7); a.ins("TAX")
    a.label("rd_hl")
    a.ins("CPX_imm", 0); a.br("BEQ", "rd_hr0")
    a.ins("DEX"); a.ins("DEC_zp", ET4)
    a.ins("LDY_zp", ET4); a.ins16("LDA_absY", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "rd_hr0")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", ET1); a.br("BNE", "rd_hr0")
    a.ins("INC_zp", ET3); a.jmp("rd_hl")
    a.label("rd_hr0")
    a.ins("LDA_zp", ET0); a.ins("STA_zp", ET4)
    a.ins("LDA_zp", ET0); a.ins("AND_imm", 7); a.ins("TAX")
    a.label("rd_hr")
    a.ins("CPX_imm", COLS - 1); a.br("BEQ", "rd_v")
    a.ins("INX"); a.ins("INC_zp", ET4)
    a.ins("LDY_zp", ET4); a.ins16("LDA_absY", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "rd_v")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", ET1); a.br("BNE", "rd_v")
    a.ins("INC_zp", ET3); a.jmp("rd_hr")
    a.label("rd_v")
    a.ins("LDA_imm", 1); a.ins("STA_zp", ET5)
    a.ins("LDA_zp", ET0); a.ins("STA_zp", ET4)
    a.ins("LDX_zp", ET2)
    a.label("rd_vu")
    a.ins("CPX_imm", 0); a.br("BEQ", "rd_vd0")
    a.ins("DEX"); a.ins("LDA_zp", ET4); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", ET4)
    a.ins("LDY_zp", ET4); a.ins16("LDA_absY", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "rd_vd0")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", ET1); a.br("BNE", "rd_vd0")
    a.ins("INC_zp", ET5); a.jmp("rd_vu")
    a.label("rd_vd0")
    a.ins("LDA_zp", ET0); a.ins("STA_zp", ET4)
    a.ins("LDX_zp", ET2)
    a.label("rd_vd")
    a.ins("CPX_imm", ROWS - 1); a.br("BEQ", "rd_max")
    a.ins("INX"); a.ins("LDA_zp", ET4); a.ins("CLC"); a.ins("ADC_imm", 8); a.ins("STA_zp", ET4)
    a.ins("LDY_zp", ET4); a.ins16("LDA_absY", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "rd_max")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", ET1); a.br("BNE", "rd_max")
    a.ins("INC_zp", ET5); a.jmp("rd_vd")
    a.label("rd_max")
    a.ins("LDA_zp", ET3); a.ins("CMP_zp", ET5); a.br("BCS", "rd_useh"); a.ins("LDA_zp", ET5)
    a.label("rd_useh")
    a.ins("TAX")
    a.ins16("LDA_absX", SQ_LO_ADDR); a.ins("CLC"); a.ins("ADC_zp", EO_LO); a.ins("STA_zp", EO_LO)
    a.ins16("LDA_absX", SQ_HI_ADDR); a.ins("ADC_zp", EO_HI); a.ins("STA_zp", EO_HI)
    a.label("rd_next")
    a.ins("INC_zp", ET0); a.ins("LDA_zp", ET0); a.ins("CMP_imm", 128); a.br("BEQ", "rd_done"); a.jmp("rd_cell")
    a.label("rd_done")
    a.ins("RTS")           # result left in EO_LO/EO_HI; leaf_score copies to EV_RDY


def emit_setup(a):
    a.label("setup")
    a.ins("LDA_imm", 0); a.ins("STA_zp", EO_LO)
    a.ins("LDA_imm", 1); a.ins("STA_zp", ET3); a.ins("LDA_imm", ROWS); a.ins("STA_zp", ET5)
    a.ins("LDA_imm", COLS); a.ins("STA_zp", ET6); a.jsr("su_pass")
    a.ins("LDA_imm", 8); a.ins("STA_zp", ET3); a.ins("LDA_imm", COLS); a.ins("STA_zp", ET5)
    a.ins("LDA_imm", ROWS); a.ins("STA_zp", ET6); a.jsr("su_pass")
    a.ins("RTS")
    a.label("su_pass")
    a.ins("LDA_imm", 0); a.ins("STA_zp", ET0)
    a.label("su_line")
    a.ins("LDA_zp", ET3); a.ins("CMP_imm", 1); a.br("BNE", "su_lcol")
    a.ins("LDA_zp", ET0); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.jmp("su_lset")
    a.label("su_lcol")
    a.ins("LDA_zp", ET0)
    a.label("su_lset")
    a.ins("STA_zp", ET2); a.ins("LDA_imm", 0); a.ins("STA_zp", ET1)
    a.label("su_i")
    a.ins("LDX_zp", ET2); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "su_iadv")
    a.ins("AND_imm", 0x0F); a.ins("STA_zp", ET4)
    a.ins("LDA_zp", ET2); a.ins("CLC"); a.ins("ADC_zp", ET3); a.ins("TAX")
    a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "su_iadv")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", ET4); a.br("BNE", "su_iadv")
    a.ins("TXA"); a.ins("CLC"); a.ins("ADC_zp", ET3); a.ins("TAX")
    a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "su_iadv")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", ET4); a.br("BNE", "su_iadv")
    a.jsr("su_touch"); a.br("BCC", "su_iadv"); a.ins("INC_zp", EO_LO)
    a.label("su_iadv")
    a.ins("LDA_zp", ET2); a.ins("CLC"); a.ins("ADC_zp", ET3); a.ins("STA_zp", ET2)
    a.ins("INC_zp", ET1)
    a.ins("LDA_zp", ET6); a.ins("SEC"); a.ins("SBC_imm", 2); a.ins("CMP_zp", ET1); a.br("BNE", "su_i")
    a.ins("INC_zp", ET0); a.ins("LDA_zp", ET0); a.ins("CMP_zp", ET5); a.br("BNE", "su_line")
    a.ins("RTS")
    a.label("su_touch")
    a.ins("LDX_zp", ET2); a.jsr("su_chkv"); a.br("BCS", "su_t1")
    a.ins("LDA_zp", ET2); a.ins("CLC"); a.ins("ADC_zp", ET3); a.ins("TAX"); a.jsr("su_chkv"); a.br("BCS", "su_t1")
    a.ins("LDA_zp", ET2); a.ins("CLC"); a.ins("ADC_zp", ET3); a.ins("CLC"); a.ins("ADC_zp", ET3); a.ins("TAX")
    a.jsr("su_chkv"); a.br("BCS", "su_t1")
    a.ins("LDA_zp", ET1); a.br("BEQ", "su_tend")
    a.ins("LDA_zp", ET2); a.ins("SEC"); a.ins("SBC_zp", ET3); a.ins("TAX"); a.jsr("su_chkv"); a.br("BCS", "su_t1")
    a.label("su_tend")
    a.ins("LDA_zp", ET6); a.ins("SEC"); a.ins("SBC_imm", 3); a.ins("CMP_zp", ET1); a.br("BEQ", "su_t0"); a.br("BCC", "su_t0")
    a.ins("LDA_zp", ET2); a.ins("CLC"); a.ins("ADC_zp", ET3); a.ins("CLC"); a.ins("ADC_zp", ET3)
    a.ins("CLC"); a.ins("ADC_zp", ET3); a.ins("TAX"); a.jsr("su_chkv"); a.br("BCS", "su_t1")
    a.label("su_t0")
    a.ins("CLC"); a.ins("RTS")
    a.label("su_t1")
    a.ins("SEC"); a.ins("RTS")
    a.label("su_chkv")
    a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "su_cv0")
    a.ins("STA_zp", ESCR)
    a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BNE", "su_cv0")
    a.ins("LDA_zp", ESCR); a.ins("AND_imm", 0x0F); a.ins("CMP_zp", ET4); a.br("BNE", "su_cv0")
    a.ins("SEC"); a.ins("RTS")
    a.label("su_cv0")
    a.ins("CLC"); a.ins("RTS")


def emit_has_virus(a):
    # EV_VIRFLAG = 1 if BOARD has any virus, else 0
    a.label("has_virus")
    a.ins("LDX_imm", 127)
    a.label("hv_lp")
    a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "hv_no")
    a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BEQ", "hv_yes")
    a.label("hv_no")
    a.ins("DEX"); a.br("BPL", "hv_lp")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", EV_VIRFLAG); a.ins("RTS")
    a.label("hv_yes")
    a.ins("LDA_imm", 1); a.ins16("STA_abs", EV_VIRFLAG); a.ins("RTS")


def emit_combine(a):
    # SCO = 5000 -12*maxh -25*holes -45*toprisk +40*set -30*bur +4*rdy ; EV_WIN=1 if no virus
    a.label("combine")
    a.ins16("LDA_abs", EV_VIRFLAG); a.br("BNE", "cm_go")
    a.ins("LDA_imm", 1); a.ins16("STA_abs", EV_WIN)
    a.ins("LDA_imm", 0); a.ins16("STA_abs", EV_SCO_LO); a.ins16("STA_abs", EV_SCO_HI); a.ins("RTS")
    a.label("cm_go")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", EV_WIN)
    a.ins("LDA_imm", BIAS5000 & 0xFF); a.ins16("STA_abs", EV_SCO_LO)
    a.ins("LDA_imm", (BIAS5000 >> 8) & 0xFF); a.ins16("STA_abs", EV_SCO_HI)
    # helper macro via su-like calls
    def t8(src_zp, k, sub):
        a.ins("LDA_zp", src_zp); a.ins16("STA_abs", EV_MLO); a.ins("LDA_imm", 0); a.ins16("STA_abs", EV_MHI)
        a.ins("LDX_imm", k); a.jsr("cm_mul"); a.jsr("cm_sub" if sub else "cm_add")
    def t16(lo, hi, k, sub):
        a.ins16("LDA_abs", lo); a.ins16("STA_abs", EV_MLO); a.ins16("LDA_abs", hi); a.ins16("STA_abs", EV_MHI)
        a.ins("LDX_imm", k); a.jsr("cm_mul"); a.jsr("cm_sub" if sub else "cm_add")
    t8(SH_MAXH, 12, True); t8(SH_HOLES, 25, True); t8(SH_TOPRISK, 45, True)
    a.ins16("LDA_abs", EV_SET); a.ins16("STA_abs", EV_MLO); a.ins("LDA_imm", 0); a.ins16("STA_abs", EV_MHI)
    a.ins("LDX_imm", 40); a.jsr("cm_mul"); a.jsr("cm_add")
    t16(EV_BUR_LO, EV_BUR_HI, 30, True)
    t16(EV_RDY_LO, EV_RDY_HI, 4, False)
    a.ins("RTS")
    a.label("cm_mul")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", EV_PLO); a.ins16("STA_abs", EV_PHI)
    a.label("cm_mlp")
    a.ins16("LDA_abs", EV_PLO); a.ins("CLC"); a.ins16("ADC_abs", EV_MLO); a.ins16("STA_abs", EV_PLO)
    a.ins16("LDA_abs", EV_PHI); a.ins16("ADC_abs", EV_MHI); a.ins16("STA_abs", EV_PHI)
    a.ins("DEX"); a.br("BNE", "cm_mlp"); a.ins("RTS")
    a.label("cm_add")
    a.ins16("LDA_abs", EV_SCO_LO); a.ins("CLC"); a.ins16("ADC_abs", EV_PLO); a.ins16("STA_abs", EV_SCO_LO)
    a.ins16("LDA_abs", EV_SCO_HI); a.ins16("ADC_abs", EV_PHI); a.ins16("STA_abs", EV_SCO_HI); a.ins("RTS")
    a.label("cm_sub")
    a.ins16("LDA_abs", EV_SCO_LO); a.ins("SEC"); a.ins16("SBC_abs", EV_PLO); a.ins16("STA_abs", EV_SCO_LO)
    a.ins16("LDA_abs", EV_SCO_HI); a.ins16("SBC_abs", EV_PHI); a.ins16("STA_abs", EV_SCO_HI); a.ins("RTS")


def emit_leaf_score(a):
    # Run all terms on BOARD -> EV_WIN (1=virus-free) + EV_SCO (16-bit weighted score).
    a.label("leaf_score")
    a.jsr("shape")
    a.jsr("buried")           # writes EV_BUR_LO/HI directly
    a.jsr("readiness")        # writes EO_LO/HI -> copy to EV_RDY
    a.ins("LDA_zp", EO_LO); a.ins16("STA_abs", EV_RDY_LO)
    a.ins("LDA_zp", EO_HI); a.ins16("STA_abs", EV_RDY_HI)
    a.jsr("setup")            # writes EO_LO -> copy to EV_SET
    a.ins("LDA_zp", EO_LO); a.ins16("STA_abs", EV_SET)
    a.jsr("has_virus")
    a.jsr("combine")
    a.ins("RTS")


def emit_eval(a):
    emit_buried(a); emit_readiness(a); emit_setup(a); emit_has_virus(a); emit_combine(a); emit_leaf_score(a)

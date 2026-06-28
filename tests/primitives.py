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
BOARD = 0x0500
MARK = 0x0300          # 16-byte BIT-PACKED mark buffer (cell k -> bit k&7 of byte k>>3)

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

    # fc_apply: walk cell offset 127..0; test its packed bit; clear+count if set.
    # _BP1 holds the cell offset (X is reused for byte index); _BP2 holds the mask.
    a.label("fc_apply")
    a.ins("LDX_imm", 127)
    a.label("fc_ap")
    a.ins("STX_zp", _BP1)                                  # save cell offset
    a.ins("TXA"); a.ins("AND_imm", 7); a.ins("TAY")        # Y = bit index
    a.ins("LDA_imm", 1)
    a.label("fc_apsh"); a.ins("DEY"); a.br("BMI", "fc_apshd")
    a.ins("ASL_A"); a.jmp("fc_apsh")
    a.label("fc_apshd"); a.ins("STA_zp", _BP2)             # mask = 1<<(off&7)
    a.ins("TXA"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("TAX")  # X = byte idx
    a.ins16("LDA_absX", MARK); a.ins("AND_zp", _BP2); a.br("BEQ", "fc_apnext")
    # marked: clear board[_BP1], count
    a.ins("LDX_zp", _BP1)
    a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0)
    a.br("BNE", "fc_apnotv"); a.ins("INC_zp", PASS_VIR)
    a.label("fc_apnotv")
    a.ins("INC_zp", PASS_CELLS)
    a.ins("LDA_imm", EMPTY); a.ins16("STA_absX", BOARD)
    a.label("fc_apnext")
    a.ins("LDX_zp", _BP1); a.ins("DEX"); a.br("BPL", "fc_ap")   # restore offset, next
    a.ins("RTS")

    # ---- targeted first pass: scan only the 2 placed cells' rows+cols ----
    # inputs Z_OFFA=$6D, Z_OFFB=$6E. Correct because the pre-placement board has
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


def emit_first_occ(a):
    """first_occ: input col in X (0-7). Output A = row (0-15) of the topmost
    occupied cell in that column, or 16 if the column is empty."""
    a.label("first_occ")
    a.ins("TXA"); a.ins("STA_zp", FO_OFF)      # working offset = col (row 0)
    a.ins("LDY_imm", 0)                          # Y = row
    a.label("fo_loop")
    a.ins("LDX_zp", FO_OFF); a.ins16("LDA_absX", BOARD)
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

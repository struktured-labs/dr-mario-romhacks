#!/usr/bin/env python3
"""Build drmario_copro.nes — the COPROCESSOR cartridge for the custom MiSTer NES core
(mapper 100 = MMC1 + Dr.Mario coprocessor at $5000-$51FF), with AUTO-NAV: the cart boots
itself into a VS-CPU L11 match and re-arms after every match. No controller needed (built
for a MiSTer whose physical controls are broken; also makes it a self-running demo).

How: the v28cs blob head at $FB00 (reached from the 0x37CF controller hook EVERY frame,
all modes) is repointed to the $FF54 trampoline, which bank-switches to unit-1 and runs
`main` each frame:
  menu modes  -> autonav state machine injecting P1 presses into $F5 (SELECT,SELECT,START,
                 LEFT x15, RIGHT x11, START) so the hack's own menu toggle sets VS-CPU
                 state properly; mirrors $F5->$F6 when $04=1 (P2 level cursor).
  intro (8)   -> hands off (no stray START).
  play (4)    -> the copro driver: on new pill upload board+colors to the FPGA window,
                 GO, hold pill while DONE=0, then publish best move to $DD/$DA and act.
The heavy depth-2 search runs on the SECOND 6502 inside the FPGA (~0.2-0.3s/pill vs 78s).
NOT Mesen-compatible (mapper 100) — MiSTer custom core only.
"""
import sys
sys.path.insert(0, "tests")
from patch_vs_cpu import Asm6502
import patch_vs_cpu as _pv
_pv.OPS.setdefault("ORA_abs", 0x0D)
from expand_prg import expand

V28CS = "drmario_v28cs.nes"
OUT = "drmario_copro.nes"
UNIT1_CPU = 0x8000
WRAP_CPU = 0xFF54
WRAP_FILE = 0x4010 + (WRAP_CPU - 0xC000)
BLOB_FILE = 0x7B10                       # CPU $FB00
PRG_REG = 0xFFF0
ARMED = 0x6143             # PRG-RAM: !=0 searching (hold), ==0 act
NAV_T, NAV_MAGIC = 0x6147, 0x6149   # autonav frame counter + PRG-RAM power-on magic
GRAV_P1, GRAV_P2 = 0x0312, 0x0392   # per-player gravity counters
# CPU-vs-CPU: FPGA coprocessor is time-shared between P1 and P2 (~0.3s per pill each);
# ARMED tracks in-flight search, WHICH is 1=serving P1, 2=serving P2, PEND_* records
# player i's pill has locked and needs a search, TGT_C/O_* are that player's target move.
WHICH  = 0x614D
PEND1  = 0x614E
PEND2  = 0x614F
TGT_C1 = 0x6150
TGT_O1 = 0x6151
TGT_C2 = 0x6152
TGT_O2 = 0x6153
LASTY1 = 0x6154
LASTY2 = 0x6155
STKX1, STKY1, STK1 = 0x6156, 0x6157, 0x6158   # P1 stagnation: last x/y + stuck-frame count
STKX2, STKY2, STK2 = 0x6159, 0x615A, 0x615B   # P2 stagnation
WDOG, WRETRY = 0x615C, 0x615D   # search watchdog: ticks-while-ARMED + one-retry latch
DELAY1, DELAY2 = 0x615E, 0x615F  # post-edge settle: preview/board can update a beat after spawn
TURN = 0x6160    # (unused in dual-copro) fair round-robin serving
# DUAL COPRO: each player has its OWN coprocessor + search state -> no time-sharing.
# copro1 window $5000-$51FF serves P1; copro2 window $5200-$53FF serves P2.
ARMED2, WDOG2, WRETRY2 = 0x6161, 0x6162, 0x6163   # P2's independent search state (ARMED/WDOG/WRETRY = P1's)
MATCH_ACTIVE = 0x6164   # set once play is dispatched; gates the full-clear STAGE-CLEAR auto-advance
WDOGH1, WDOGH2 = 0x6165, 0x6166   # watchdog HIGH bytes: depth-3 searches run seconds, not frames
WDOG_HI_LIM = 56                  # timeout = 56*256 = 14336 ticks ~= 4min (FULL-ply1 d3 first pill
                                  # ~95s measured-scaled on the dense 48-virus board; 2.5x margin)
# per-copro tie-break seeds (same eval, different near-tie resolution -> desyncs mirror play).
# Derived once per match from NAV_T; ride the color uploads' HIGH nibbles (firmware masks &$0F
# and extracts SEED=(CB&$F0)|(CA>>4); seed 0 = jitter off).
SEED1, SEED2, TMPSEED = 0x6167, 0x6168, 0x6169
VSEEN1, VSEEN2 = 0x616A, 0x616B   # count-was-nonzero-this-match latches (gate the auto-advance:
                                  # in 1P/demo contexts the unused P2 count reads 0 -> START-spam)
# ROT_DONE2 (DRROTFIX): P2 orient-commit latch, reset per pill. 0 = pre-phase (orient still
# tracks the search while the capsule is frozen HIGH); 1 = committed (orient LOCKED, only the
# column refines as it descends). Stops the mid-flight orient retarget that rotates a low/flush
# capsule and locks it BACKWARDS (field-seen on the Pocket combo brain 2026-07-19). $616C/$616D
# are the anytime torn-read scratch; $616E is the next free PRG-RAM byte.
ROT_DONE2 = 0x616E
import os as _os
USE_SEEDS = _os.environ.get("DRSEED", "1") != "0"   # DRSEED=0 -> seeds stay 0 = deterministic mirror
# WEAVE steering: when sliding to the target column is blocked at the pill's row (stuck
# >= WEAVE_LIM hook-cycles), release the gravity freeze for one drop so the pill descends
# a row and can slide past the obstruction (down-and-over), instead of hovering frozen and
# then force-dropping straight down. Measured: 8-17% of legal cols are slide-unreachable at
# half-to-3/4 fill -> misplacement -> burial (hardware walls at ~20 viruses). DRWEAVE=0 off.
USE_WEAVE = _os.environ.get("DRWEAVE", "1") != "0"
# DRHUMAN=1 -> HUMAN-CHALLENGE build: P1 = human passthrough (no copro search, no $F5/$F7
# injection, no P1 gravity pinning in act), P2 = the validated copro AI unchanged.
HUMAN_P1 = _os.environ.get("DRHUMAN", "0") == "1"
# DRNOFREEZE=1 -> ANYTIME steering: never pin P2 gravity while searching. The firmware
# live-publishes its running best into the result mailbox (orient=0xFF = "no result yet"
# sentinel); the driver refreshes TGT every hook and weave-steers while the search refines.
# Pill fall time becomes the AI's honest time budget (kills the visible mid-air pause).
NO_FREEZE = _os.environ.get("DRNOFREEZE", "0") == "1"
WEAVE_LIM = int(_os.environ.get("DRWEAVELIM", "40"))   # hook-cycles of no-move before a weave drop
                                                        # (> DAS repeat ~30 so normal slides don't trip it)
# DRROTFIX=1 (default): the P2 anytime driver gets driver-fidelity steering -- rotation
# PRE-PHASE (rotate to the target orient while frozen high, in open air), FEASIBILITY-GATED
# retarget (orient locks at commit so a late retarget can't rotate a low capsule backwards),
# and a MINIMUM-THINK gate (no lateral/orient commit until DONE or MIN_THINK hooks of search).
# DRROTFIX=0 reproduces the pre-fidelity byte-exact emission (A/B + regression parity).
ROTFIX = _os.environ.get("DRROTFIX", "1") != "0"
# minimum-think gate: hooks of search (WDOG2) the driver waits before committing laterally /
# locking orient. ~5 hooks/frame, so 90 ~= 18 frames ~= the spawn animation (controller input
# is ignored during it anyway). Below this the search's argmax is a shallow first guess; the
# field miss (dual-end at cols 6-7 lost to a left-wall half-credit) was a commit off that guess.
MIN_THINK = int(_os.environ.get("DRMINTHINK", "90"))
VCOUNT_P1, VCOUNT_P2 = 0x0324, 0x03A4   # remaining virus counts (0 => that player cleared -> STAGE CLEAR)
W2_BASE = 0x5200
# DRPOCKET=1: single-window build (Analogue Pocket core has only the $5000 window).
# P2's copro traffic rides the $5000 mailbox instead of $5200. Requires DRHUMAN=1
# (P1 must not be using the window; with both players active they'd collide).
if _os.environ.get("DRPOCKET", "0") == "1":
    assert _os.environ.get("DRHUMAN", "0") == "1", "DRPOCKET requires DRHUMAN=1 (single window)"
    W2_BASE = 0x5000
# if a pill sits still this many frames (while not search-frozen), force DOWN to unstick
STUCK_LIM = 60        # 1s -- continuous holds again; if truly stuck kick fast to unpark
# copro window (mapper 100)
W_BOARD, W_CA, W_GO, W_DONE, W_COL, W_OR = 0x5000, 0x5080, 0x5084, 0x5084, 0x5085, 0x5086
# NES pad bits on $F5 (pressed-this-frame): A=$80 B=$40 Sel=$20 Start=$10 U=$08 D=$04 L=$02 R=$01
B_SEL, B_START, B_LEFT, B_RIGHT = 0x20, 0x10, 0x02, 0x01

# DRSTUDY=1 -> "study pause": freeze game logic on pause but keep the last gameplay frame
# rendered instead of the vanilla blank+"PAUSE". Default ON for human carts (DRHUMAN=1) so a
# paused board can be studied. Mechanism (base pause routine at CPU $978E; verified on base
# drmario.nes in Mesen — see tmp/study_pause/): the routine blanks the background ($2001 bit3),
# fills OAM with $FF, draws "PAUSE", then spins on $B654 whose tail re-clears OAM every frame.
# We keep background rendering ON, and swap the two pause frame-waits $B654 -> $B670 (identical
# wait WITHOUT the OAM-clear tail) so the sprites in the buffer at pause entry stay put; the
# entry OAM-clear is NOP'd. The falling capsule + bottle + viruses are in the buffer at pause
# entry, so they persist. The pause loop's draw call ($97D3) is repointed to STUDY_BLOB at $D2CC
# (a 4-part trampoline routine in dead padding free in base AND v28cs) which (1) reconnects the
# "STUDY" text by setting $42=$80 then JSR $88F6 so the 5 letters land in OAM slots 32-36 (ABOVE
# every capsule/preview, so BOTH players' capsules in 2P/VS stay put), and (2) HAND-DRAWS the
# next-pill preview(s) — P1 (slots 37-38, colors $031A/$031B) always, and P2 (slots 39-40, colors
# $039A/$039B) in 2P/VS — each at its mode-correct position ($0727). See STUDY_BLOB below.
#   NOTE (validation basis): base-ROM change is Mesen-proven (paused frame shows bottle+viruses+
#   capsule+preview, frozen, clean resume). The copro carts are mapper 100 (not Mesen-emulable);
#   DRSTUDY applies the SAME asserted byte patches + blob to the v28cs image (which already
#   carries 2 of the 5 edits from a prior partial attempt — the patch is idempotent). Dr.Mario /
#   magnifier sprites are still not restored (decor built by the skipped main-loop phase). The
#   carts run in VS-CPU mode; pause-reachability and 2P preview correctness are NOT emulator-
#   verified. $D2CC-$D2FF must be confirmed dead in any deployed binary before surgical patching.
STUDY = _os.environ.get("DRSTUDY", "1" if HUMAN_P1 else "0") != "0"
# Anchor on the pause loop's START/$F7 check (LDA $F5;CMP #$10;BEQ;LDA $F7;CMP #$F0;BEQ) —
# these bytes are NEVER touched by the edits, so the locator stays valid + idempotent even
# after patching (all 5 edits sit just before/after this window, never inside it).
STUDY_ANCHOR = bytes.fromhex("a5f5c910f00ca5f7c9f0f0b7")
STUDY_EDITS = [   # (rel-to-anchor, [accepted originals], replacement, note)
    (-0x20, [bytes.fromhex("2054b6")], bytes.fromhex("2070b6"), "entry wait $B654->$B670 (no OAM clear)"),
    (-0x1D, [bytes.fromhex("a916"), bytes.fromhex("a91e")], bytes.fromhex("a91e"), "keep background rendering ON"),
    (-0x12, [bytes.fromhex("2094b8"), bytes.fromhex("eaeaea")], bytes.fromhex("eaeaea"), "drop entry OAM clear"),
    (-0x03, [bytes.fromhex("20f688"), bytes.fromhex("eaeaea")], bytes.fromhex("20ccd2"), "draw STUDY letters + preview (JSR $D2CC)"),
    (0x0C, [bytes.fromhex("2054b6")], bytes.fromhex("2070b6"), "loop wait $B654->$B670 (no OAM clear)"),
]
# STUDY-draw routine (v3.2) — reconnects "STUDY" text AND hand-draws BOTH players' next-pill previews
# during pause, WITHOUT disturbing any frozen capsule, in 1P / 2-player / VS layouts. STUDY -> OAM
# slots 32-36, P1 preview -> 37-38, P2 preview (2P/VS only) -> 39-40 — all ABOVE the slot-15 gameplay
# buffer max, so BOTH players' capsules (slots 0-3 in 2P/VS) are byte-untouched. Both players consume
# the shared pill sequence at different rates, so P2's next pill ($039A/$039B) differs from P1's
# ($031A/$031B) and must show separately (the game itself draws both, $87DA/$87FE).
# A mode-correct 2-preview draw doesn't fit one dead run, so it is a 4-part trampoline through dead
# padding free in base AND v28cs (part1 in the fixed bank; parts 2-4 in bank0, where the pause routine
# already runs so they are always mapped):
#   part1 @ $D2CC: $42=$80; JSR $88F6 (STUDY -> 32-36); write P1 tiles+attr (37-38) and the 1P-default
#     P1 position (Y=$45 X=$BE/$C6, the right box); JMP part2.
#   part2 @ $9FF8: LDY $0727; DEY; BEQ RTS  (1P -> keep part1's defaults, no P2). Else (2P/VS) set
#     Y=$33 for all four preview slots (37-40) and P1 X=$38/$40 (above P1's board); JMP part3a.
#   part3a @ $A371: P2 preview tiles ($60|$039A / $70|$039B) + attr into slots 39-40; JMP part3b.
#   part3b @ $BE56: P2 preview X=$B8/$C0 (above P2's board, mirroring the game's $87FE draw); RTS.
# Tiles = $60|colorA / $70|colorB (game's own preview $8772 uses template+color via ADC, never masks
# -> raw colors are 0-2 and $60|c == $60+c). STUDY_BLOB (part1) fills the whole 52-byte $D2CC run so
# it covers any prior v2/v3/v3.1 blob when upgrading an already-patched image in place.
#   NOTE (validation basis): base-ROM change is Mesen-proven in 1P, 2P and VS-CPU (paused frame keeps
#   both capsules + STUDY + BOTH mode-correct previews showing each player's actual next pill, frozen,
#   clean resume). The copro carts are mapper 100 (not Mesen-emulable); DRSTUDY applies the SAME
#   asserted byte patches + blobs, and the 2P base test reproduces the cart's both-capsules-in-buffer
#   layout. All four dead runs must be confirmed dead in any deployed binary before surgical patching.
STUDY_BLOB_CPU  = 0xD2CC   # part1  (fixed bank; duplicated by expand at file 0x52DC / 0xD2DC)
STUDY_BLOB2_CPU = 0x9FF8   # part2  (bank0; single copy, file 0x2008)
STUDY_BLOB3_CPU = 0xA371   # part3a (bank0; single copy, file 0x2381)
STUDY_BLOB4_CPU = 0xBE56   # part3b (bank0; single copy, file 0x3E66)
STUDY_BLOB = bytes.fromhex(                          # part1 — exactly 52 B (fills the $D2CC run)
    "A980" "8542" "20F688"            # LDA #$80; STA $42; JSR $88F6   (STUDY -> slots 32-36)
    "AD1A03" "0960" "8D9502"          # LDA $031A; ORA #$60; STA $0295 (P1 slot37 tile = left half)
    "AD1B03" "0970" "8D9902"          # LDA $031B; ORA #$70; STA $0299 (P1 slot38 tile = right half)
    "A902" "8D9602" "8D9A02"          # LDA #$02; STA $0296; STA $029A (P1 attr, both halves)
    "A945" "8D9402" "8D9802"          # LDA #$45; STA $0294; STA $0298 (P1 Y = 69, 1P default)
    "A9BE" "8D9702"                   # LDA #$BE; STA $0297            (P1 slot37 X = 190, 1P)
    "A9C6" "8D9B02"                   # LDA #$C6; STA $029B            (P1 slot38 X = 198, 1P)
    "4CF89F")                         # JMP $9FF8  -> part2
STUDY_BLOB2 = bytes.fromhex(                         # part2 @ $9FF8 (34 B)
    "AC2707" "88" "F01B"              # LDY $0727; DEY; BEQ +27 (1P -> RTS, keep part1 defaults)
    "A933" "8D9402" "8D9802" "8D9C02" "8DA002"   # LDA #$33; STA Y of slots 37,38,39,40 (all = 51)
    "A938" "8D9702"                   # LDA #$38; STA $0297 (P1 slot37 X = 56, 2P/VS)
    "A940" "8D9B02"                   # LDA #$40; STA $029B (P1 slot38 X = 64, 2P/VS)
    "4C71A3"                          # JMP $A371 -> part3a
    "60")                             # RTS (1P lands here)
STUDY_BLOB3 = bytes.fromhex(                         # part3a @ $A371 (27 B) — P2 tiles + attr
    "AD9A03" "0960" "8D9D02"          # LDA $039A; ORA #$60; STA $029D (P2 slot39 tile = left half)
    "AD9B03" "0970" "8DA102"          # LDA $039B; ORA #$70; STA $02A1 (P2 slot40 tile = right half)
    "A902" "8D9E02" "8DA202"          # LDA #$02; STA $029E; STA $02A2 (P2 attr, both halves)
    "4C56BE")                         # JMP $BE56 -> part3b
STUDY_BLOB4 = bytes.fromhex(                         # part3b @ $BE56 (11 B) — P2 X, then done
    "A9B8" "8D9F02"                   # LDA #$B8; STA $029F (P2 slot39 X = 184, above P2 board)
    "A9C0" "8DA302"                   # LDA #$C0; STA $02A3 (P2 slot40 X = 192)
    "60")                             # RTS
# Prior blobs at $D2CC accepted as overwritable so an already-patched image upgrades in place.
OLD_STUDY_BLOB_V2 = bytes.fromhex(   # v2: preview only, slots 2-3, no STUDY text (47 B)
    "AD1A03" "2903" "0960" "8D0902" "AD1B03" "2903" "0970" "8D0D02"
    "A945" "8D0802" "8D0C02" "A902" "8D0A02" "8D0E02" "A9BE" "8D0B02" "A9C6" "8D0F02" "60")
OLD_STUDY_BLOB_V3 = bytes.fromhex(   # v3.0: STUDY slots 2-6 + preview slots 7-8, fixed 1P pos (50 B)
    "A908" "8542" "20F688" "AD1A03" "0960" "8D1D02" "AD1B03" "0970" "8D2102"
    "A945" "8D1C02" "8D2002" "A902" "8D1E02" "8D2202" "A9BE" "8D1F02" "A9C6" "8D2302" "60")
OLD_STUDY_BLOB_V31 = bytes.fromhex(  # v3.1 part1 @ $D2CC (34 B code, was $00-padded to 50)
    "A980" "8542" "20F688" "AD1A03" "0960" "8D9502" "AD1B03" "0970" "8D9902"
    "A902" "8D9602" "8D9A02" "4CF89F")
OLD_STUDY_BLOB2_V31 = bytes.fromhex( # v3.1 part2 @ $9FF8 (31 B)
    "A945" "A2BE" "AC2707" "88" "F004" "A933" "A238"
    "8D9402" "8D9802" "8E9702" "8A" "18" "6908" "8D9B02" "60")


class StudyPatchError(Exception):
    pass


def apply_study_pause(rom):
    """Apply the DRSTUDY 'study pause' byte patches to a Dr. Mario PRG image in place.
    Idempotent + asserted: locate the pause routine by a stable anchor, verify each target holds
    an accepted original (base) OR the already-patched value (v28cs / re-run), place the preview
    blob in dead padding (asserting it is filler or already the blob), and fail loudly on
    anything else. Returns the count of edits actually written (edits + blob)."""
    if rom[4] != 2:
        raise StudyPatchError(f"DRSTUDY: expected a 32KB-PRG image (2 banks), got {rom[4]}")
    a = rom.find(STUDY_ANCHOR)
    if a < 0:
        raise StudyPatchError("DRSTUDY: pause-routine anchor not found (unexpected ROM)")
    if rom.find(STUDY_ANCHOR, a + 1) >= 0:
        raise StudyPatchError("DRSTUDY: pause-routine anchor is ambiguous (multiple matches)")
    for rel, accepted, after, note in STUDY_EDITS:          # verify all before writing any
        off = a + rel
        got = bytes(rom[off:off + len(after)])
        if got != after and got not in accepted:
            raise StudyPatchError(
                f"DRSTUDY: 0x{off:X} ({note}): got {got.hex()}, expected one of "
                + "/".join(b.hex() for b in accepted + [after]))
    # 4 blob targets, each in a confirmed dead run; every one must be free (or already ours, or a
    # prior blob we are upgrading in place). (cpu, blob, dead-run-size, [accepted prior prefixes])
    targets = [
        (STUDY_BLOB_CPU,  STUDY_BLOB,  52, [OLD_STUDY_BLOB_V2, OLD_STUDY_BLOB_V3, OLD_STUDY_BLOB_V31]),
        (STUDY_BLOB2_CPU, STUDY_BLOB2, 38, [OLD_STUDY_BLOB2_V31]),
        (STUDY_BLOB3_CPU, STUDY_BLOB3, 28, []),
        (STUDY_BLOB4_CPU, STUDY_BLOB4, 24, []),
    ]
    def _overwritable(reg, blob, olds):
        if reg[:len(blob)] == blob or set(reg) <= {0x00, 0xFF}:              # already ours / pristine
            return True
        return any(reg[:len(o)] == o and set(reg[len(o):]) <= {0x00, 0xFF} for o in olds)  # prior blob
    for cpu, blob, dead, olds in targets:                  # verify all before writing any
        off = 16 + (cpu - 0x8000)
        reg = bytes(rom[off:off + dead])
        if not _overwritable(reg, blob, olds):
            raise StudyPatchError(f"DRSTUDY: blob target 0x{off:X} (${cpu:04X}) not free: {reg[:8].hex()}...")
    written = 0
    for rel, accepted, after, note in STUDY_EDITS:
        off = a + rel
        if bytes(rom[off:off + len(after)]) != after:
            rom[off:off + len(after)] = after
            written += 1
    for cpu, blob, dead, olds in targets:                  # each blob fills from the run start; a
        off = 16 + (cpu - 0x8000)                          # longer blob fully covers any shorter prior
        if bytes(rom[off:off + len(blob)]) != blob:
            rom[off:off + len(blob)] = blob
            written += 1
    return written


def build_main(level=11, speed=1):
    a = Asm6502(UNIT1_CPU)

    # ================= per-frame entry =================
    a.label("main")
    # PRG-RAM power-on init (SDRAM boots as garbage): magic byte at NAV_MAGIC
    a.ins16("LDA_abs", NAV_MAGIC); a.ins("CMP_imm", 0xA5); a.br("BEQ", "inited")
    a.ins("LDA_imm", 0xA5); a.ins16("STA_abs", NAV_MAGIC)
    a.ins("LDA_imm", 0); a.ins16("STA_abs", ARMED); a.ins16("STA_abs", NAV_T)
    a.ins16("STA_abs", STK1); a.ins16("STA_abs", STK2); a.ins16("STA_abs", MATCH_ACTIVE)
    a.ins16("STA_abs", WDOG); a.ins16("STA_abs", WRETRY)
    a.ins16("STA_abs", ARMED2); a.ins16("STA_abs", WDOG2); a.ins16("STA_abs", WRETRY2)
    a.ins16("STA_abs", WDOGH1); a.ins16("STA_abs", WDOGH2)
    a.ins16("STA_abs", SEED1); a.ins16("STA_abs", SEED2)
    a.ins16("STA_abs", VSEEN1); a.ins16("STA_abs", VSEEN2)
    if ROTFIX:
        a.ins16("STA_abs", ROT_DONE2)                       # A==0 here: orient-commit latch clear
    a.ins("LDA_imm", 3)                                     # sane targets pre-first-publish
    a.ins16("STA_abs", TGT_C1); a.ins16("STA_abs", TGT_O1)
    a.ins16("STA_abs", TGT_C2); a.ins16("STA_abs", TGT_O2)
    a.ins("LDA_imm", 2); a.ins16("STA_abs", TURN)          # fair-serve round-robin seed
    a.label("inited")
    a.ins16("INC_abs", NAV_T)                               # tick every hook call (autonav only ticked in menus)
    # ---- full-clear auto-advance (mode-independent): a player's virus count ($0324/$03A4) hit 0
    # => STAGE CLEAR screen. Inject START (press window) to advance it so the demo LOOPS instead
    # of halting. Gated by MATCH_ACTIVE (set once play dispatched) so boot-init count==0 can't
    # false-trigger (which would wreck the boot state machine). ----
    a.ins16("LDA_abs", MATCH_ACTIVE); a.br("BEQ", "fc_no")
    a.ins16("LDA_abs", VCOUNT_P1); a.br("BNE", "fc_chk2")
    a.ins16("LDA_abs", VSEEN1); a.br("BNE", "fc_clear")     # P1==0 counts only if it was ever >0
    a.label("fc_chk2")
    a.ins16("LDA_abs", VCOUNT_P2); a.br("BNE", "fc_no")
    a.ins16("LDA_abs", VSEEN2); a.br("BEQ", "fc_no")
    a.label("fc_clear")                                     # full clear -> own the frame (skip normal dispatch)
    a.ins16("LDA_abs", NAV_T); a.ins("AND_imm", 0x1F); a.ins("CMP_imm", 4); a.br("BCS", "fc_ret")
    a.ins("LDA_imm", B_START); a.ins("STA_zp", 0xF5)        # inject START to dismiss STAGE CLEAR
    a.label("fc_ret"); a.ins("RTS")
    a.label("fc_no")
    a.ins16("LDA_abs", 0x0046); a.ins("CMP_imm", 0x04); a.br("BNE", "not_play")
    a.ins("LDA_zp", 0x04); a.br("BNE", "go_ai"); a.ins("RTS")
    a.label("go_ai")
    if USE_SEEDS:
        a.ins16("LDA_abs", MATCH_ACTIVE); a.br("BNE", "ga_on")  # first play frame of this match:
        a.ins16("LDA_abs", NAV_T); a.ins("ORA_imm", 0x01); a.ins16("STA_abs", SEED1)   # root seed
        a.ins("EOR_imm", 0xA4); a.ins16("STA_abs", SEED2)       # bit0 kept -> both odd, distinct
        a.label("ga_on")
    a.ins("LDA_imm", 1); a.ins16("STA_abs", MATCH_ACTIVE)   # play started -> arm full-clear detect
    a.ins16("LDA_abs", VCOUNT_P1); a.br("BEQ", "ga_v2"); a.ins("LDA_imm", 1); a.ins16("STA_abs", VSEEN1)
    a.label("ga_v2")
    a.ins16("LDA_abs", VCOUNT_P2); a.br("BEQ", "ga_vd"); a.ins("LDA_imm", 1); a.ins16("STA_abs", VSEEN2)
    a.label("ga_vd")
    a.jmp("dispatch")
    a.label("not_play")
    a.ins("CMP_imm", 0x08); a.br("BNE", "menus")
    # intro mode ONLY happens at power-on/reset: re-arm the autonav (PRG-RAM persists across
    # soft core relaunches, so the NAV_MAGIC one-time init does NOT re-run -> stale NAV_T killed
    # the nav and the title idled into attract mode). Zeroing here makes every boot nav cleanly.
    a.ins("LDA_imm", 0); a.ins16("STA_abs", NAV_T); a.ins16("STA_abs", MATCH_ACTIVE)
    a.ins16("STA_abs", VSEEN1); a.ins16("STA_abs", VSEEN2)
    a.ins("RTS")                                            # intro/init: hands off otherwise
    a.label("menus")
    a.jsr("autonav")
    a.ins("LDA_zp", 0x04); a.br("BEQ", "m_done")
    a.ins("LDA_zp", 0xF5); a.ins("STA_zp", 0xF6)            # VS: mirror P1->P2 (level cursor)
    a.label("m_done"); a.ins("RTS")

    # ============ autonav: direct state + $F5-only START injection (ZERO input) ============
    # SELECT-equivalent: JSR $FF30 (hack's own toggle; touches only $0727/$04/$06F1) until
    # $04==1. Levels: force $0316/$0396/$96=11 in mode 1. STARTs: inject $F5=$10 in a press
    # window. KEY: inject $F5 ONLY -- the read routine ANDs two raw passes (hook fires in
    # both, value survives) then computes newly-pressed = raw & ~held($F7); writing $F7 too
    # marks the button already-held and zeroes the edge (the original injection bug).
    # Window (NAV_T & $1F) < 4: pressed ~1 frame in ~6 (hook ~5 calls/frame), then released.
    def inject(bits):
        a.ins("LDA_imm", bits); a.ins("STA_zp", 0xF5)
        a.ins16("STA_abs", 0x6148)                          # DBG: last injected
        a.ins16("INC_abs", 0x614B)                          # DBG: inject count
    a.label("autonav")
    a.ins16("LDA_abs", 0x0046)
    a.ins("CMP_imm", 0x00); a.br("BEQ", "an_title")
    a.ins("CMP_imm", 0x01); a.br("BEQ", "an_lvl")
    a.ins("CMP_imm", 0x07); a.br("BEQ", "an_start")         # post-match: START -> rematch
    a.ins("RTS")
    a.label("an_title")
    # VS-CPU landing gate. $FF30 cycles three states: 1P ($0727=1,$04=0) -> 2P-human
    # ($0727=2,$04=0) -> VS-CPU ($0727=2,$04=1). $04 is the ONLY discriminator that
    # isolates VS-CPU; $0727==2 is ALSO true at 2P-human. Gating START on $0727==2 (the
    # 992682f "deterministic-nav" experiment) fires START one toggle early, INTO 2P-human,
    # where $04==0 leaves the play-dispatch AI dormant (see "LDA $04; BNE go_ai" above) ->
    # neither board is ever uploaded, DONE never fires, both capsules stagnate. That is the
    # v4 AB-cart regression. Gate on $04 (BEQ->toggle past 2P-human, land on VS-CPU): this
    # is the emission that ALL shipped/validated carts use (Pocket + AB); $0727==2 never
    # shipped. NOTE: keep this a byte-exact "LDA $04; BEQ; JMP" 7-byte block -- any change
    # here shifts the whole downstream driver and reopens the byte-divergence from the
    # deployed reference carts.
    a.ins("LDA_zp", 0x04); a.br("BEQ", "an_tog")
    a.jmp("an_start")
    a.label("an_tog")
    a.ins16("LDA_abs", NAV_T); a.ins("AND_imm", 0x1F); a.ins("CMP_imm", 1); a.br("BEQ", "an_tog_go")
    a.ins("RTS")
    a.label("an_tog_go")
    a.jsr(0xFF30)                                           # ONE toggle per window (game needs a
    a.ins("RTS")                                            #  frame between mode inits; the $04
                                                            #  gate above lands VS-CPU deterministically)
    a.label("an_lvl")
    a.ins("LDA_imm", level)
    a.ins16("STA_abs", 0x0316)                              # P1 level
    a.ins16("STA_abs", 0x0396)                              # P2 level (+$80 struct offset)
    a.ins("STA_zp", 0x96)                                   # live cursor (cosmetic)
    a.ins("LDA_imm", speed); a.ins("STA_zp", 0x45)         # force game speed (0=LOW,1=MED,2=HI)
    a.label("an_start")
    a.ins16("LDA_abs", NAV_T); a.ins("AND_imm", 0x1F); a.ins("CMP_imm", 4); a.br("BCC", "an_st_go")
    a.ins("RTS")
    a.label("an_st_go")
    inject(B_START)
    a.ins("RTS")

    # ================= play-mode CPU-vs-CPU driver (time-shared FPGA) =================
    a.label("dispatch")
    # ---- pill-lock edge detect (both players) ----
    a.ins16("LDA_abs", 0x0306); a.ins16("CMP_abs", LASTY1)
    a.br("BCC", "no_p1_new"); a.br("BEQ", "no_p1_new")
    a.ins("LDA_imm", 1); a.ins16("STA_abs", PEND1)
    a.ins("LDA_imm", 15); a.ins16("STA_abs", DELAY1)        # ~3 frames settle before upload
    a.ins("LDA_imm", 0); a.ins16("STA_abs", WRETRY)
    a.label("no_p1_new")
    a.ins16("LDA_abs", 0x0306); a.ins16("STA_abs", LASTY1)
    a.ins16("LDA_abs", 0x0386); a.ins16("CMP_abs", LASTY2)
    a.br("BCC", "no_p2_new"); a.br("BEQ", "no_p2_new")
    a.ins("LDA_imm", 1); a.ins16("STA_abs", PEND2)
    a.ins("LDA_imm", 15); a.ins16("STA_abs", DELAY2)        # ~3 frames settle before upload
    a.ins("LDA_imm", 0); a.ins16("STA_abs", WRETRY)
    if ROTFIX:
        a.ins16("STA_abs", ROT_DONE2)                       # A==0 here: new P2 pill -> re-enter pre-phase
    a.label("no_p2_new")
    a.ins16("LDA_abs", 0x0386); a.ins16("STA_abs", LASTY2)

    # ---- stagnation detect: pill not moving while not search-frozen -> count up ----
    def stagnate(px, py, sx, sy, cnt, armed, pend, tag):
        a.ins16("LDA_abs", px); a.ins16("CMP_abs", sx); a.br("BNE", f"mvd_{tag}")
        a.ins16("LDA_abs", py); a.ins16("CMP_abs", sy); a.br("BNE", f"mvd_{tag}")
        # Skip while PENDING (waiting for its search -> would force-drop in the spawn center)
        # or while being SEARCHED (frozen). Only a genuinely wedged pill should force-drop.
        a.ins16("LDA_abs", pend); a.br("BNE", f"sk_{tag}")
        a.ins16("LDA_abs", armed); a.br("BNE", f"sk_{tag}")
        a.label(f"cnt_{tag}")
        a.ins16("INC_abs", cnt)
        a.jmp(f"sk_{tag}")
        a.label(f"mvd_{tag}")
        a.ins("LDA_imm", 0); a.ins16("STA_abs", cnt)
        a.ins16("LDA_abs", px); a.ins16("STA_abs", sx)
        a.ins16("LDA_abs", py); a.ins16("STA_abs", sy)
        a.label(f"sk_{tag}")
    stagnate(0x0305, 0x0306, STKX1, STKY1, STK1, ARMED, PEND1, "s1")
    stagnate(0x0385, 0x0386, STKX2, STKY2, STK2, ARMED2, PEND2, "s2")

    # ---- DUAL-COPRO search: each player drives its OWN coprocessor; both run in parallel.
    # No time-sharing => no WHICH / fair-serving / pending-wait. handle() emitted per player.
    def handle(idx, wbase, board_src, colsrcs, armed, wdog, wretry, pend, delay, tgt_c, tgt_o, wdogh, seedsrc):
        wgo, wdone, wcol, wor = wbase + 0x84, wbase + 0x84, wbase + 0x85, wbase + 0x86
        L = f"h{idx}"
        a.ins16("LDA_abs", delay); a.br("BEQ", f"{L}_dz"); a.ins16("DEC_abs", delay)   # settle timer
        a.label(f"{L}_dz")
        a.ins16("LDA_abs", armed); a.br("BEQ", f"{L}_start")     # not searching -> maybe start
        a.ins16("LDA_abs", wdone); a.br("BEQ", f"{L}_search")    # DONE==0 -> still searching
        # publish result: best_col + orient4 -> game orient map {0xFF/0:3, 1:1, 2:0, 3:2}
        a.ins16("LDA_abs", wcol); a.ins16("STA_abs", tgt_c)
        a.ins16("LDA_abs", wor); a.ins("CMP_imm", 0xFF); a.br("BNE", f"{L}_map")
        a.ins("LDA_imm", 3); a.jmp(f"{L}_pst")
        a.label(f"{L}_map")
        a.ins("CMP_imm", 0); a.br("BNE", f"{L}_m1"); a.ins("LDA_imm", 3); a.jmp(f"{L}_pst")
        a.label(f"{L}_m1"); a.ins("CMP_imm", 1); a.br("BNE", f"{L}_m2"); a.ins("LDA_imm", 1); a.jmp(f"{L}_pst")
        a.label(f"{L}_m2"); a.ins("CMP_imm", 2); a.br("BNE", f"{L}_m3"); a.ins("LDA_imm", 0); a.jmp(f"{L}_pst")
        a.label(f"{L}_m3"); a.ins("LDA_imm", 2)
        a.label(f"{L}_pst"); a.ins16("STA_abs", tgt_o)
        a.ins("LDA_imm", 0); a.ins16("STA_abs", armed); a.ins16("STA_abs", wdog); a.ins16("STA_abs", wdogh)
        a.jmp(f"{L}_done")
        a.label(f"{L}_search")           # 16-bit watchdog: d3 searches take seconds; abandon ~30s, re-queue once
        a.ins16("INC_abs", wdog); a.br("BNE", f"{L}_wl"); a.ins16("INC_abs", wdogh)
        a.label(f"{L}_wl")
        a.ins16("LDA_abs", wdogh); a.ins("CMP_imm", WDOG_HI_LIM); a.br("BCS", f"{L}_wto"); a.jmp(f"{L}_done"); a.label(f"{L}_wto")
        a.ins("LDA_imm", 0); a.ins16("STA_abs", armed); a.ins16("STA_abs", wdog); a.ins16("STA_abs", wdogh)
        a.ins16("LDA_abs", wretry); a.br("BEQ", f"{L}_rt"); a.jmp(f"{L}_done"); a.label(f"{L}_rt")
        a.ins("LDA_imm", 1); a.ins16("STA_abs", wretry); a.ins16("STA_abs", pend)
        a.jmp(f"{L}_done")
        a.label(f"{L}_start")            # start a search: upload board+colors to THIS copro, GO
        a.ins16("LDA_abs", pend); a.br("BNE", f"{L}_st1"); a.jmp(f"{L}_done"); a.label(f"{L}_st1")
        a.ins16("LDA_abs", delay); a.br("BEQ", f"{L}_st2"); a.jmp(f"{L}_done"); a.label(f"{L}_st2")
        a.ins("LDX_imm", 0)
        # NES playfield empties are 0xFF *or* 0x00 (per tile-encoding); the copro parser only
        # treats 0xFF as empty, so a 0x00 cell reads as a PHANTOM yellow pill -> the color-heavy
        # depth-3 endgame eval corrupts once mid-game clears create 0x00 cells (walls at ~20;
        # sim never sees it -- faithful_to_nes always emits 0xFF). Normalize 0x00 -> 0xFF here.
        a.label(f"{L}_cp")
        a.ins16("LDA_absX", board_src); a.br("BNE", f"{L}_cpnz")   # non-zero -> store as-is
        a.ins("LDA_imm", 0xFF)                                      # 0x00 -> empty
        a.label(f"{L}_cpnz")
        a.ins16("STA_absX", wbase)
        a.ins("INX"); a.ins("CPX_imm", 128); a.br("BNE", f"{L}_cp")
        for k, src in enumerate(colsrcs):
            if k == 0:      # cA carries seed low nibble (<<4)
                a.ins16("LDA_abs", seedsrc)
                a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A")
                a.ins16("STA_abs", TMPSEED)
                a.ins16("LDA_abs", src); a.ins("AND_imm", 0x0F); a.ins16("ORA_abs", TMPSEED)
            elif k == 1:    # cB carries seed high nibble
                a.ins16("LDA_abs", seedsrc); a.ins("AND_imm", 0xF0); a.ins16("STA_abs", TMPSEED)
                a.ins16("LDA_abs", src); a.ins("AND_imm", 0x0F); a.ins16("ORA_abs", TMPSEED)
            else:
                a.ins16("LDA_abs", src); a.ins("AND_imm", 0x0F)
            a.ins16("STA_abs", wbase + 0x80 + k)
        a.ins16("STA_abs", wgo)          # GO: write to +$84 pulses copro reset, clears DONE
        a.ins("LDA_imm", 1); a.ins16("STA_abs", armed)
        a.ins("LDA_imm", 0); a.ins16("STA_abs", pend); a.ins16("STA_abs", wretry)
        a.ins16("STA_abs", wdog); a.ins16("STA_abs", wdogh)
        a.label(f"{L}_done")
    if not HUMAN_P1:
        handle(1, 0x5000, 0x0400, [0x0301, 0x0302, 0x031A, 0x031B], ARMED, WDOG, WRETRY, PEND1, DELAY1, TGT_C1, TGT_O1, WDOGH1, SEED1)
    handle(2, W2_BASE, 0x0500, [0x0381, 0x0382, 0x039A, 0x039B], ARMED2, WDOG2, WRETRY2, PEND2, DELAY2, TGT_C2, TGT_O2, WDOGH2, SEED2)
    a.jmp("act")

    # freeze QUEUED players too: a pill whose search hasn't run yet must not fall unguided
    # (time-sharing wait was letting pills drop 2-4 rows before their target arrived ->
    # unreachable columns -> bad placements). Called from act below.
    a.label("freeze_pending")
    if not HUMAN_P1:
        # (DRHUMAN builds MUST skip this: handle(1) never runs, so PEND1 is uninitialized
        #  boot garbage — nonzero garbage pinned P1's gravity forever = capsule stuck at top,
        #  observed on Pocket hardware 2026-07-18.)
        a.ins16("LDA_abs", PEND1); a.br("BEQ", "fp_p2")
        a.ins("LDA_imm", 0); a.ins16("STA_abs", GRAV_P1)
    a.label("fp_p2")
    a.ins16("LDA_abs", PEND2); a.br("BEQ", "fp_done")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", GRAV_P2)
    a.label("fp_done")
    a.ins("RTS")

    # (time-shared d_start / start_p1 / start_p2 removed: handle() above starts each player's
    #  search on its own copro.)

    # ---- act: steer BOTH players toward their published targets ----
    a.label("act")
    a.jsr("freeze_pending")
    # P2 first (only if we're not currently freezing it)
    a.ins16("LDA_abs", ARMED2); a.br("BEQ", "act_p2")      # not searching P2 -> steer it
    if NO_FREEZE:
        # ANYTIME: refresh TGT from the LIVE mailbox and keep steering during the search.
        # Scratch = $616C/$616D free driver RAM (NOT zp $DB/$DC = v28cs eval scratch).
        a.ins16("LDA_abs", W2_BASE + 0x86); a.ins("CMP_imm", 0xFF); a.br("BEQ", "nf2_hold")
        a.ins16("STA_abs", 0x616C)
        a.ins16("LDA_abs", W2_BASE + 0x85); a.ins16("STA_abs", 0x616D)
        a.ins16("LDA_abs", W2_BASE + 0x86); a.ins16("CMP_abs", 0x616C)         # re-read: detect torn read
        if ROTFIX:
            a.br("BEQ", "nf2_untorn"); a.jmp("act_p1"); a.label("nf2_untorn")  # torn: keep old TGT (rel too far)
        else:
            a.br("BNE", "act_p1")                                              # torn read: keep old TGT
        a.ins16("LDA_abs", 0x616D); a.ins16("STA_abs", TGT_C2)   # column: always refine (anytime)
        if ROTFIX:
            # FEASIBILITY-GATED retarget: refine the ORIENT only while pre-phase (orient not yet
            # committed). Once ROT_DONE2 latches, keep the committed orient so a late candidate
            # cannot rotate a low/flush capsule and lock it backwards.
            a.ins16("LDA_abs", ROT_DONE2); a.br("BNE", "nf2_col_only")
            a.ins16("LDA_abs", 0x616C); a.ins16("STA_abs", TGT_O2)
            a.label("nf2_col_only")
        else:
            a.ins16("LDA_abs", 0x616C); a.ins16("STA_abs", TGT_O2)
        a.jmp("act_p2")                                     # weave-steer toward the live target
        a.label("nf2_hold")
        # no candidate published yet. FAIRNESS: under ROTFIX the capsule keeps FALLING under
        # live gravity (no pin) -- we only WITHHOLD steering until there is a move to make.
        # DRROTFIX=0 keeps the legacy brief freeze (byte-identical to the deployed carts).
        a.ins("LDA_imm", 0)
        if not ROTFIX:
            a.ins16("STA_abs", GRAV_P2)
        a.ins("STA_zp", 0xF6); a.ins("STA_zp", 0xF8); a.jmp("act_p1")
    else:
        a.ins("LDA_imm", 0); a.ins16("STA_abs", GRAV_P2)       # searching P2 -> freeze + skip steer
        a.ins("STA_zp", 0xF6); a.ins("STA_zp", 0xF8); a.jmp("act_p1")
    a.label("act_p2")
    if ROTFIX:
        # SETTLE GUARD: while a new pill is PENDING (search not started, TGT still stale from the
        # previous pill) WITHHOLD steering so no stale target/orient is adopted. Gravity during
        # PEND2 is handled by freeze_pending (deployed; the ~3-frame settle sits inside the spawn
        # no-fall window) -- we do NOT pin GRAV_P2 here (fairness: no extra world-stop).
        a.ins16("LDA_abs", PEND2); a.br("BEQ", "act_p2_go")
        a.ins("LDA_imm", 0); a.ins("STA_zp", 0xF6); a.ins("STA_zp", 0xF8); a.jmp("act_p1")
        a.label("act_p2_go")
    a.ins16("LDA_abs", STK2); a.ins("CMP_imm", STUCK_LIM); a.br("BCC", "act_p2_n")
    a.ins("LDY_imm", 0x04); a.ins("STY_zp", 0xF6); a.jmp("act_p1")   # stuck: force drop
    a.label("act_p2_n")
    # steer-then-drop, CONTINUOUS holds (v28cs DAS handles repeat). Pulsed windows parked
    # pills near the top on hardware because (with NAV_T=5*/frame) 32-hook cycles = 6.4
    # frames per edge -> 25s to move 4 cols -> pill hovered forever.
    if ROTFIX:
        # ROTATION PRE-PHASE + MINIMUM-THINK gate (orient not yet committed) -- all under LIVE
        # gravity (FAIRNESS north star: the AI never pins gravity to buy time; it plays under the
        # same fall a human does):
        #  - orient != target -> press A to rotate toward TGT_O2 (no pin). Rotations land in the
        #    first natural fall-steps -- the honest budget. If a late-game fall is too fast to
        #    finish, that is the same constraint a human faces (we do NOT stop the world for it).
        #  - orient reached -> WITHHOLD lateral + orient-lock until the think gate opens: DONE
        #    (ARMED2==0) or WDOG2 >= MIN_THINK hooks (below that the argmax is a shallow guess).
        #    During the gate the capsule keeps FALLING (no pin); we simply do not ACT yet.
        #  - at the gate: LATCH ROT_DONE2 (orient locked) and fall through to the column phase.
        # (ROT_DONE2 set => this whole block is skipped: orient stays put, only the column moves.
        #  That is the feasibility lock -- a late candidate can't re-rotate a low/flush capsule.)
        a.ins16("LDA_abs", ROT_DONE2); a.br("BNE", "mv_p2")           # committed -> column only
        a.ins16("LDA_abs", 0x03A5); a.ins16("CMP_abs", TGT_O2); a.br("BEQ", "p2_orient_ok")
        a.ins("LDA_imm", 0x00); a.ins("STA_zp", 0xF8)                # edge (held=0) so A rotates,
        a.ins("LDA_imm", 0x80); a.ins("STA_zp", 0xF6); a.jmp("act_p1")   # under live gravity, no pin
        a.label("p2_orient_ok")                                       # orient reached; think gate:
        a.ins16("LDA_abs", ARMED2); a.br("BEQ", "p2_commit")         # DONE -> commit
        a.ins16("LDA_abs", WDOGH2); a.br("BNE", "p2_commit")         # >256 hooks searched -> commit
        a.ins16("LDA_abs", WDOG2); a.ins("CMP_imm", MIN_THINK); a.br("BCS", "p2_commit")
        a.ins("LDA_imm", 0); a.ins("STA_zp", 0xF6); a.ins("STA_zp", 0xF8)   # gate closed: no ACT,
        a.jmp("act_p1")                                              # but NO pin -- capsule falls
        a.label("p2_commit")
        a.ins("LDA_imm", 1); a.ins16("STA_abs", ROT_DONE2)           # orient LOCKED -> begin descent
    else:
        a.ins16("LDA_abs", 0x03A5); a.ins16("CMP_abs", TGT_O2); a.br("BEQ", "mv_p2")
        a.ins("LDA_imm", 0); a.ins16("STA_abs", GRAV_P2)
        a.ins("LDA_imm", 0x00); a.ins("STA_zp", 0xF8)
        a.ins("LDA_imm", 0x80); a.ins("STA_zp", 0xF6); a.jmp("act_p1")
    a.label("mv_p2")
    a.ins16("LDA_abs", 0x0385); a.ins16("CMP_abs", TGT_C2); a.br("BEQ", "dn_p2")
    if not USE_WEAVE:
        a.ins("LDA_imm", 0); a.ins16("STA_abs", GRAV_P2)  # baseline: freeze at spawn row (slide-only)
    # WEAVE: skip the freeze -> the pill falls at natural gravity WHILE sliding toward the
    # target, weaving down-and-over past columns blocked at the spawn row. DAS shift-rate
    # (~1 col/6f) >> drop-rate (~1 row/16f), so it reaches the target column well before landing.
    a.ins("LDY_imm", 0x01); a.ins16("LDA_abs", 0x0385); a.ins16("CMP_abs", TGT_C2); a.br("BCC", "st_p2")
    a.ins("LDY_imm", 0x02); a.jmp("st_p2")
    a.label("dn_p2")
    if NO_FREEZE:
        # ANYTIME: never fast-drop while the search is still ARMED — gravity is the time
        # budget. Aligned + still thinking = hold position (no input) and keep falling.
        a.ins16("LDA_abs", ARMED2); a.br("BEQ", "dn_p2_go")
        a.ins("LDY_imm", 0x00); a.jmp("st_p2")
        a.label("dn_p2_go")
    a.ins("LDY_imm", 0x04)
    a.label("st_p2"); a.ins("STY_zp", 0xF6)
    a.label("act_p1")
    if HUMAN_P1:
        a.jmp("act_done")                                   # human P1: never touch $F5/$F7/GRAV_P1
    # skip P1 acting if we're currently searching for P1
    a.ins16("LDA_abs", ARMED); a.br("BEQ", "act_p1_go")    # not searching P1 -> steer it
    a.ins("LDA_imm", 0); a.ins16("STA_abs", GRAV_P1)       # searching P1 -> freeze + skip steer
    a.ins("STA_zp", 0xF5); a.ins("STA_zp", 0xF7); a.jmp("act_done")
    a.label("act_p1_go")
    a.ins16("LDA_abs", STK1); a.ins("CMP_imm", STUCK_LIM); a.br("BCC", "act_p1_n")
    a.ins("LDY_imm", 0x04); a.ins("STY_zp", 0xF5); a.jmp("act_done")  # stuck: force drop
    a.label("act_p1_n")
    a.ins16("LDA_abs", 0x0325); a.ins16("CMP_abs", TGT_O1); a.br("BEQ", "mv_p1")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", GRAV_P1)
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", 0xF7)
    a.ins("LDA_imm", 0x80); a.ins("STA_zp", 0xF5); a.jmp("act_done")
    a.label("mv_p1")
    a.ins16("LDA_abs", 0x0305); a.ins16("CMP_abs", TGT_C1); a.br("BEQ", "dn_p1")
    if not USE_WEAVE:
        a.ins("LDA_imm", 0); a.ins16("STA_abs", GRAV_P1)  # baseline: freeze at spawn row (slide-only)
    # WEAVE: skip the freeze -> pill falls while sliding, weaving down-and-over (see mv_p2).
    a.ins("LDY_imm", 0x01); a.ins16("LDA_abs", 0x0305); a.ins16("CMP_abs", TGT_C1); a.br("BCC", "st_p1")
    a.ins("LDY_imm", 0x02); a.jmp("st_p1")
    a.label("dn_p1"); a.ins("LDY_imm", 0x04)
    a.label("st_p1"); a.ins("STY_zp", 0xF5)
    a.label("act_done")
    a.ins("RTS")
    return a.assemble(), a.labels


def _sel(w, value):
    w.ins("LDA_imm", value)
    for i in range(5):
        w.ins("STA_abs", PRG_REG & 0xFF, (PRG_REG >> 8) & 0xFF)
        if i < 4:
            w.ins("LSR_A")


def build_wrapper(main_cpu):
    """Trampoline (every frame, all modes): bank2 -> JSR main -> bank0 -> RTS."""
    w = Asm6502(WRAP_CPU)
    _sel(w, 2)
    w.jsr(main_cpu)
    _sel(w, 0)
    w.ins("RTS")
    return w.assemble()


def main():
    import os
    global OUT
    level = int(os.environ.get("DRLEVEL", "11"))
    speed = int(os.environ.get("DRSPEED", "1"))
    if level != 11 or speed != 1:
        OUT = f"drmario_copro_L{level}s{speed}.nes"
    unit1, labels = build_main(level, speed)
    print(f"LEVEL={level} SPEED={speed} -> {OUT}")
    main_cpu = UNIT1_CPU + labels["main"]
    print(f"unit-1 main: {len(unit1)} B at ${UNIT1_CPU:04X}; main=${main_cpu:04X}")
    bank = bytearray(b"\x00" * 0x4000)
    bank[0:len(unit1)] = unit1

    wrap = build_wrapper(main_cpu)
    print(f"trampoline: {len(wrap)} B at ${WRAP_CPU:04X}")
    assert WRAP_CPU + len(wrap) <= 0xFFD2, "wrapper overflows the dead-v17 window"

    rom = bytearray(open(V28CS, "rb").read())
    assert rom[4] == 2
    rom[WRAP_FILE:WRAP_FILE + len(wrap)] = wrap
    HOOK_FILE = 0x37CF
    assert rom[HOOK_FILE] == 0x4C and rom[HOOK_FILE + 1] == 0x00 and rom[HOOK_FILE + 2] == 0xFB, \
        "expected v28cs hook JMP $FB00 at 0x37CF"
    # blob head: STA $F6; LDA $04; BNE... -> STA $F6; JMP $FF54  (trampoline runs every frame)
    assert rom[BLOB_FILE:BLOB_FILE + 6] == bytes.fromhex("85f6a504d003"), \
        "unexpected v28cs blob head"
    rom[BLOB_FILE:BLOB_FILE + 5] = bytes([0x85, 0xF6, 0x4C, 0x54, 0xFF])
    print("blob head repointed: STA $F6; JMP $FF54 (every frame, all modes)")

    if STUDY:
        n = apply_study_pause(rom)      # asserted + idempotent; touches only the pause routine
        print(f"DRSTUDY: study-pause patched ($978E; {n} new edit(s)) — bg stays on, "
              f"sprites frozen, no blank/PAUSE")

    tmp = OUT + ".2bank"
    open(tmp, "wb").write(rom)
    expand(tmp, OUT, new_bank_bytes=bytes(bank))
    import os
    os.remove(tmp)
    out = bytearray(open(OUT, "rb").read())
    out[6] = (out[6] & 0x0F) | 0x40      # mapper 100 = 0x64
    out[7] = (out[7] & 0x0F) | 0x60
    open(OUT, "wb").write(out)
    print(f"wrote {OUT} (mapper 100, AUTO-NAV VS-CPU L11, FPGA coprocessor)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate the v28 cartridge AI on L11 VS-CPU by letting P2 (AI) play a full
board while keeping idle-P1 alive (blank P1's top rows so it can't top out, but
leave P1's viruses so P1 can't win either). Tracks P2's real virus count
(tiles with high nibble $D in $0500-$057F) until win / topout / timeout.
"""
import sys, os, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from mesen_interface_file import MesenInterface

WORK = Path(__file__).resolve().parents[1].parent / "mesen2/bin/linux-x64/Release"
P1_BOARD = 0x0400
P2_BOARD = 0x0500


def main():
    max_frames = int(sys.argv[1]) if len(sys.argv) > 1 else 9000
    it = MesenInterface(work_dir=WORK)
    it.connect(timeout=8)

    def r(a): return it.read_memory(a, 1)[0]
    def rd(a, n): return it.read_memory(a, n)
    def w(a, vals): it.write_memory(a, vals)
    def tap(btn, hold=6, rest=16):
        it.set_input(0, [btn] if btn else []); it.step_frame(hold)
        it.set_input(0, []); it.step_frame(rest)

    def viruses(base):
        return sum(1 for x in rd(base, 0x80) if (x & 0xF0) == 0xD0)

    # --- nav: title -> VS-CPU -> L11 -> play ---
    it.set_step_mode(True); it.step_frame(150)
    tap("select"); tap("select"); tap("start", 8, 60)
    for _ in range(25): tap("left", 4, 6)
    for _ in range(11): tap("right", 5, 9)
    seed = int(os.environ.get("DRM_SEED", "0"))   # vary virus layout: write BEFORE the start
    if seed:
        w(0x0017, [seed & 0xFF]); w(0x0018, [(seed >> 8) & 0xFF])
    tap("start", 8, 120)
    for _ in range(200):
        if r(0x46) == 4: break
        it.step_frame(8)
    def keep_p1_alive():
        # Clear ALL capsule tiles ($40-$7F) across P1's whole board so stacked
        # pieces can never top P1 out; preserve viruses ($Dx) so P1 can't win.
        b = rd(P1_BOARD, 0x80)
        out = [0xFF if 0x40 <= x <= 0x7F else x for x in b]
        if out != list(b):
            w(P1_BOARD, out)

    def fill_map(base):
        b = rd(base, 0x80)
        rows = []
        for r_ in range(8):  # show top 8 rows (16 cols/row -> 8 cells visible/row width 8)
            row = b[r_ * 8:(r_ + 1) * 8]
            rows.append("".join("." if x == 0xFF else
                                ("V" if (x & 0xF0) == 0xD0 else "o") for x in row))
        return rows

    # wait for the virus intro to finish — keep P1 alive throughout so the match
    # can't end before the measurement loop starts.
    for _ in range(60):
        keep_p1_alive()
        it.step_frame(16)
        if viruses(P1_BOARD) >= 40 and viruses(P2_BOARD) >= 40:
            break

    p2v0 = viruses(P2_BOARD)
    print(f"level={r(0x0316)} P1v={viruses(P1_BOARD)} P2v={p2v0}  (expect 48 each at L11)")
    print("running... (clearing only P1 stacked capsules, viruses preserved)")

    orient = collections.Counter()
    minv = p2v0
    frames = 0
    last_report = 0
    result = "timeout"
    while frames < max_frames:
        keep_p1_alive()
        it.step_frame(16)
        frames += 16
        m = r(0x46)
        if m != 4:
            result = (f"match ended (mode={m}) P1v={viruses(P1_BOARD)} "
                      f"P2v={viruses(P2_BOARD)}")
            print(" -- P1 board top8 --   -- P2 board top8 --")
            p1m, p2m = fill_map(P1_BOARD), fill_map(P2_BOARD)
            for a, bb in zip(p1m, p2m):
                print(f"   {a}        {bb}")
            break
        v = viruses(P2_BOARD)
        minv = min(minv, v)
        orient[r(0x03A5) & 1] += 1
        if v == 0:
            result = "P2 WIN (all viruses cleared)"
            break
        if frames - last_report >= 200:
            last_report = frames
            # P2 board fill (topout risk = top 2 rows occupied)
            toprow = sum(1 for x in rd(P2_BOARD, 16) if x != 0xFF)
            print(f"  ~{frames:5d}f: P2 vir={v} (min {minv}) toprow={toprow} "
                  f"P2x={r(0x0385)} P2y={r(0x0386)} o3A5={r(0x03A5)} "
                  f"Zbor={r(0xDA)} tgt={r(0xDE)} raw00={r(0x00)}")

    print(f"=== RESULT: {result} | P2 viruses {p2v0} -> {viruses(P2_BOARD)} "
          f"(min {minv}, cleared {p2v0 - minv}) | vert-frames={orient[1]} horiz={orient[0]} ===")


if __name__ == "__main__":
    main()

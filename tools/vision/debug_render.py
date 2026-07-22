#!/usr/bin/env python3
"""Render a classification-annotated overlay: each cell tagged with colour
letter (r/y/b lower=pill, R/Y/B upper=virus) for visual QA."""
from __future__ import annotations
import numpy as np
import cv2

TAGCOL = {"R": (60, 60, 230), "Y": (40, 220, 230), "B": (230, 200, 90), ".": (120, 120, 120)}


def render(im_bgr, pf, board, title=None):
    import classify as C
    out = im_bgr.copy()
    for c in range(9):
        x = int(round(pf.x0 + c * pf.cw)); cv2.line(out, (x, int(pf.y0)), (x, int(pf.y1)), (0, 180, 0), 1)
    for r in range(17):
        y = int(round(pf.y0 + r * pf.ch)); cv2.line(out, (int(pf.x0), y), (int(pf.x1), y), (0, 180, 0), 1)
    for r in range(16):
        for c in range(8):
            color, isv = board[r][c]
            letter = C.COLOR_NAME[color]
            if color != C.EMPTY and not isv:
                letter = letter.lower()
            if color == C.EMPTY:
                continue
            x0, y0, x1, y1 = pf.cell_box(r, c)
            cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
            cv2.putText(out, letter, (cx - 12, cy + 8), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 0), 4, cv2.LINE_AA)
            cv2.putText(out, letter, (cx - 12, cy + 8), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, TAGCOL[C.COLOR_NAME[color]], 2, cv2.LINE_AA)
    if title:
        cv2.putText(out, title, (int(pf.x0), int(pf.y0) - 8), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255, 255, 255), 2, cv2.LINE_AA)
    return out


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "/home/struktured/projects/dr-mario-mods/tools/vision")
    import localize as L, classify as C
    im = cv2.imread(sys.argv[1])
    p1, p2 = L.playfields()
    b1 = C.read_board(im, p1); b2 = C.read_board(im, p2)
    out = render(im, p1, b1, f"P1 vir={C.virus_count(b1)}")
    out = render(out, p2, b2, f"P2 vir={C.virus_count(b2)}")
    outp = sys.argv[2] if len(sys.argv) > 2 else "/tmp/dbg.png"
    cv2.imwrite(outp, out)
    print("wrote", outp)

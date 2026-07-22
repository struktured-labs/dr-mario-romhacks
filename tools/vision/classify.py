#!/usr/bin/env python3
"""Per-cell classifier for a located DRMC playfield.

Each 8x16 cell is classified as EMPTY or one of {R,Y,B} x {pill, virus}:
  * empty vs filled  -- fraction of bright pixels in the cell.
  * colour           -- median HSV hue among bright pixels (OpenCV hue 0-179):
                          yellow ~32, blue ~101, red/magenta ~160.
  * virus vs pill    -- viruses carry a face (eyes/mouth) giving high pixel-value
                        texture (std) and dark interior pixels; pill halves are
                        smooth. Threshold on brightness-std separates them cleanly
                        (pills <~25, viruses >~65 on 2024 broadcast).

Colour codes match the NES convention used elsewhere in this repo
(NES_C: Yellow=0, Red=1, Blue=2; tile $D0=yellow virus).
"""
from __future__ import annotations
import numpy as np
import cv2

EMPTY, R, Y, B = 0, 1, 2, 3
COLOR_NAME = {EMPTY: ".", R: "R", Y: "Y", B: "B"}
NES_C = {Y: 0, R: 1, B: 2}

# thresholds (2024 broadcast, calibrated in tmp/vision_m1/probe/colordump.py)
BRIGHT_SUM = 150       # BGR-sum for a "bright" (lit) pixel
FILL_FRAC = 0.30       # >= this fraction bright -> cell is filled
HUE_YELLOW = (18, 48)
HUE_BLUE = (85, 118)
HUE_RED = (140, 179)   # magenta-red; also catch wrap-around below
HUE_RED_LO = (0, 10)
VIRUS_TEX = 42.0       # brightness-std above this -> virus


def classify_cell(cell_bgr, cell_hsv):
    """cell_bgr/cell_hsv: HxWx3 crops of ONE cell. -> (color, is_virus)."""
    bsum = cell_bgr.astype(np.int32).sum(axis=2)
    bright = bsum > BRIGHT_SUM
    bf = float(bright.mean())
    if bf < FILL_FRAC:
        return EMPTY, False
    hue = cell_hsv[:, :, 0]
    hb = hue[bright]
    if hb.size < 4:
        return EMPTY, False
    h = float(np.median(hb))

    def inr(rng):
        return rng[0] <= h <= rng[1]

    if inr(HUE_YELLOW):
        color = Y
    elif inr(HUE_BLUE):
        color = B
    elif inr(HUE_RED) or inr(HUE_RED_LO):
        color = R
    else:
        # nearest cluster fallback
        color = min((Y, 32), (B, 101), (R, 160), key=lambda kv: abs(h - kv[1]))[0]

    tex = float(cell_hsv[:, :, 2].std())
    is_virus = tex > VIRUS_TEX
    return color, is_virus


def read_board(im_bgr, pf, hsv=None):
    """-> 16x8 list of (color, is_virus). Row 0 = top."""
    if hsv is None:
        hsv = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2HSV)
    board = []
    for r in range(16):
        row = []
        for c in range(8):
            x0, y0, x1, y1 = pf.cell_box(r, c)
            row.append(classify_cell(im_bgr[y0:y1, x0:x1], hsv[y0:y1, x0:x1]))
        board.append(row)
    return board


def virus_count(board):
    return sum(1 for row in board for col, isv in row if col != EMPTY and isv)


def fill_count(board):
    return sum(1 for row in board for col, _ in row if col != EMPTY)


def to_nes(board):
    """-> 128-byte NES encoding, row-major (0xFF empty, 0xD0|c virus, 0x40|c pill)."""
    out = []
    for row in board:
        for color, isv in row:
            if color == EMPTY:
                out.append(0xFF)
            else:
                out.append((0xD0 if isv else 0x40) | NES_C[color])
    return out


def board_str(board):
    """ASCII board: '.'=empty, lowercase=pill (r/y/b), UPPERCASE=virus (R/Y/B)."""
    lines = []
    for row in board:
        s = ""
        for color, isv in row:
            ch = COLOR_NAME[color]
            s += ch if (isv or color == EMPTY) else ch.lower()
        lines.append(s)
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "/home/struktured/projects/dr-mario-mods/tools/vision")
    import localize as L
    im = cv2.imread(sys.argv[1])
    p1, p2 = L.playfields()
    for name, pf in (("P1", p1), ("P2", p2)):
        b = read_board(im, pf)
        print(f"=== {name}  viruses={virus_count(b)} filled={fill_count(b)} ===")
        print(board_str(b))

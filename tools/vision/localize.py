#!/usr/bin/env python3
"""Layout localization for DRMC broadcast frames (2024-era, 1920x1080).

Two NES Dr. Mario feeds are composited side by side, each an 8-col x 16-row
playfield inside a bright bottle frame on a black interior. The broadcast
layout is constant for a given era, so we calibrate the grid geometry ONCE
(origin + per-cell pitch, per player) and reuse it, re-verifying per frame with
a cheap anchor check (the two interiors stay mostly black, the frame between
them stays bright).

Calibration method (see tmp/vision_m1/probe/grid_optimize.py): fit the 9x17
gridlines to sit in the black gaps between cells while cell centers land on
pieces -- content-independent and subpixel. The values below were fit on the
2024 FINALS video and are stable to <1px across frames/games.
"""
from __future__ import annotations
import numpy as np
import cv2

ROWS, COLS = 16, 8

# Fixed grid geometry per player: (x0, y0, cw, ch) top-left origin + cell pitch.
ERA_2024 = {
    "frame_wh": (1920, 1080),
    "p1": (548.0, 178.5, 48.45, 49.50),
    "p2": (969.5, 179.5, 48.88, 49.72),
    # anchor-check windows (upper third of each interior, empty in ~all states)
    "p1_window": (548, 178, 936, 430),
    "p2_window": (969, 179, 1360, 430),
    "black_sum": 95,
}


class Playfield:
    """A located playfield: grid origin + 8x16 cell pitch."""
    __slots__ = ("x0", "y0", "cw", "ch", "x1", "y1")

    def __init__(self, x0, y0, cw, ch):
        self.x0, self.y0, self.cw, self.ch = float(x0), float(y0), float(cw), float(ch)
        self.x1 = self.x0 + COLS * self.cw
        self.y1 = self.y0 + ROWS * self.ch

    def cell_box(self, r, c, inset=0.20):
        """Interior pixel box (x0,y0,x1,y1) of cell (row r, col c), inset to
        avoid grid-line/border bleed from neighbouring cells."""
        ix, iy = self.cw * inset, self.ch * inset
        cx0 = self.x0 + c * self.cw + ix
        cy0 = self.y0 + r * self.ch + iy
        cx1 = self.x0 + (c + 1) * self.cw - ix
        cy1 = self.y0 + (r + 1) * self.ch - iy
        return (int(round(cx0)), int(round(cy0)), int(round(cx1)), int(round(cy1)))

    def as_dict(self):
        return {"x0": round(self.x0, 2), "y0": round(self.y0, 2),
                "cw": round(self.cw, 3), "ch": round(self.ch, 3),
                "x1": round(self.x1, 2), "y1": round(self.y1, 2)}

    def __repr__(self):
        return (f"Playfield(x[{self.x0:.0f},{self.x1:.0f}] y[{self.y0:.0f},{self.y1:.0f}] "
                f"cw={self.cw:.2f} ch={self.ch:.2f})")


def playfields(era=ERA_2024):
    """Return (p1, p2) fixed-calibrated Playfields for the era."""
    return Playfield(*era["p1"]), Playfield(*era["p2"])


def is_gameplay(frame_bgr, era=ERA_2024):
    """Cheap anchor check that the frame shows two live playfields:
    both interiors' upper thirds are largely black. Returns (bool, (f1, f2))."""
    bright = frame_bgr.astype(np.int32).sum(axis=2)
    bs = era["black_sum"]

    def black_frac(win):
        x0, y0, x1, y1 = win
        return float((bright[y0:y1, x0:x1] < bs).mean())

    f1 = black_frac(era["p1_window"])
    f2 = black_frac(era["p2_window"])
    return (f1 > 0.55 and f2 > 0.55), (round(f1, 3), round(f2, 3))


# --- re-calibration helper (used to derive ERA_* for a new broadcast era) ----

def _fit_axis(proj_black, lo_o, hi_o, lo_p, hi_p, n_lines):
    best = None
    for pitch in np.arange(lo_p, hi_p, 0.05):
        for o in np.arange(lo_o, hi_o, 0.5):
            lines = o + np.arange(n_lines + 1) * pitch
            centers = o + (np.arange(n_lines) + 0.5) * pitch
            li = np.clip(np.round(lines).astype(int), 0, len(proj_black) - 1)
            ci = np.clip(np.round(centers).astype(int), 0, len(proj_black) - 1)
            score = proj_black[li].mean() - proj_black[ci].mean()
            if best is None or score > best[0]:
                best = (score, o, pitch)
    return best


def calibrate(frame_bgr, x_window, y_window, black_sum=95):
    """Fit (x0,y0,cw,ch) for one bottle from a filled frame. For re-calibration
    of a new era; the fitted values then get hardcoded into an ERA_* dict."""
    bright = frame_bgr.astype(np.int32).sum(axis=2)
    black = (bright < black_sum).astype(np.float32)
    x_lo, x_hi = x_window
    y_lo, y_hi = y_window
    sub = black[y_lo:y_hi, x_lo:x_hi]
    sy = _fit_axis(sub.mean(axis=1), 0, 30, 47.0, 52.0, ROWS)
    sx = _fit_axis(sub.mean(axis=0), 0, 30, 46.0, 52.0, COLS)
    return (x_lo + sx[1], y_lo + sy[1], sx[2], sy[2])


def draw_overlay(frame_bgr, pf, color=(0, 255, 0)):
    """Draw the 8x16 grid + per-cell sample boxes for visual verification."""
    out = frame_bgr.copy()
    for c in range(COLS + 1):
        x = int(round(pf.x0 + c * pf.cw))
        cv2.line(out, (x, int(pf.y0)), (x, int(pf.y1)), color, 1)
    for r in range(ROWS + 1):
        y = int(round(pf.y0 + r * pf.ch))
        cv2.line(out, (int(pf.x0), y), (int(pf.x1), y), color, 1)
    for r in range(ROWS):
        for c in range(COLS):
            bx0, by0, bx1, by1 = pf.cell_box(r, c)
            cv2.rectangle(out, (bx0, by0), (bx1, by1), (255, 0, 255), 1)
    return out


if __name__ == "__main__":
    import sys
    frame = cv2.imread(sys.argv[1])
    p1, p2 = playfields()
    ok, fr = is_gameplay(frame)
    print("p1", p1)
    print("p2", p2)
    print("is_gameplay", ok, "black_frac", fr)
    ov = draw_overlay(draw_overlay(frame, p1), p2)
    outp = sys.argv[2] if len(sys.argv) > 2 else "/tmp/overlay.png"
    cv2.imwrite(outp, ov)
    print("wrote", outp)

#!/usr/bin/env python3
"""Streaming frame extraction + per-frame board classification for DRMC
broadcast video.

Frames are streamed from ffmpeg as raw BGR (one at a time -- never the whole
video in RAM) at a chosen sample rate. Each frame is gated by the cheap
`is_gameplay` anchor check and, when live, classified into (p1_board, p2_board).

CLI:
  extract.py scan  VIDEO [fps]              -> map gameplay segments (stdout)
  extract.py dump  VIDEO OUT.jsonl START DUR [fps]
                                            -> per-frame boards for a segment
"""
from __future__ import annotations
import sys, json, subprocess, shutil
import numpy as np
sys.path.insert(0, "/home/struktured/projects/dr-mario-mods/tools/vision")
import localize as L
import classify as C

W, H = 1920, 1080
FRAME_BYTES = W * H * 3


def stream_frames(video, fps=10.0, start=None, duration=None):
    """Yield (sample_index, timestamp_sec, bgr_ndarray) at `fps`.
    Uses ffmpeg rawvideo pipe; one frame resident at a time."""
    cmd = ["ffmpeg", "-v", "error"]
    if start is not None:
        cmd += ["-ss", str(start)]
    cmd += ["-i", video]
    if duration is not None:
        cmd += ["-t", str(duration)]
    cmd += ["-vf", f"fps={fps}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=FRAME_BYTES)
    idx = 0
    try:
        while True:
            buf = proc.stdout.read(FRAME_BYTES)
            if len(buf) < FRAME_BYTES:
                break
            frame = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
            ts = (start or 0.0) + idx / fps
            yield idx, ts, frame
            idx += 1
    finally:
        proc.stdout.close()
        proc.wait()


def classify_frame(frame, p1, p2):
    """-> dict with per-player boards (or None if not gameplay)."""
    ok, fr = L.is_gameplay(frame)
    if not ok:
        return {"live": False, "black": fr}
    import cv2
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    b1 = C.read_board(frame, p1, hsv)
    b2 = C.read_board(frame, p2, hsv)
    return {"live": True, "black": fr,
            "p1": b1, "p2": b2,
            "p1_vir": C.virus_count(b1), "p1_fill": C.fill_count(b1),
            "p2_vir": C.virus_count(b2), "p2_fill": C.fill_count(b2)}


def board_to_compact(board):
    """16x8 (color,isv) -> list of 16 strings (fast to store/read)."""
    out = []
    for row in board:
        s = ""
        for color, isv in row:
            ch = C.COLOR_NAME[color]
            s += ch if (color == C.EMPTY or isv) else ch.lower()
        out.append(s)
    return out


def compact_to_board(rows):
    inv = {"R": (C.R, True), "Y": (C.Y, True), "B": (C.B, True),
           "r": (C.R, False), "y": (C.Y, False), "b": (C.B, False),
           ".": (C.EMPTY, False)}
    return [[inv[ch] for ch in row] for row in rows]


def _scan(video, fps=1.0):
    """Map contiguous gameplay segments; print start/end + virus range."""
    p1, p2 = L.playfields()
    seg_start = None
    last_live = None
    for idx, ts, frame in stream_frames(video, fps=fps):
        ok, fr = L.is_gameplay(frame)
        if ok and seg_start is None:
            seg_start = ts
        if not ok and seg_start is not None:
            print(f"GAME  {seg_start:7.1f} -> {last_live:7.1f}  ({last_live-seg_start:5.1f}s)")
            seg_start = None
        if ok:
            last_live = ts
    if seg_start is not None:
        print(f"GAME  {seg_start:7.1f} -> {last_live:7.1f}  ({last_live-seg_start:5.1f}s)")


def _dump(video, out, start, dur, fps=10.0):
    p1, p2 = L.playfields()
    n = 0
    with open(out, "w") as fh:
        for idx, ts, frame in stream_frames(video, fps=fps, start=start, duration=dur):
            r = classify_frame(frame, p1, p2)
            rec = {"i": idx, "t": round(ts, 3), "live": r["live"]}
            if r["live"]:
                rec["p1"] = board_to_compact(r["p1"])
                rec["p2"] = board_to_compact(r["p2"])
                rec["p1_vir"] = r["p1_vir"]; rec["p2_vir"] = r["p2_vir"]
                rec["p1_fill"] = r["p1_fill"]; rec["p2_fill"] = r["p2_fill"]
            fh.write(json.dumps(rec) + "\n")
            n += 1
    print(f"wrote {n} frames -> {out}")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "scan":
        _scan(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1.0)
    elif mode == "dump":
        video, out, start, dur = sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
        fps = float(sys.argv[6]) if len(sys.argv) > 6 else 10.0
        _dump(video, out, start, dur, fps)

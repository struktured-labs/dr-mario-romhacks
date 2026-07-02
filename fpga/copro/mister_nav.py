#!/usr/bin/env python3
"""Robust VS-CPU navigation for drmario_copro on MiSTer with lossy virtual input:
every press is screenshot-verified; unverifiable steps (SELECT #2) are trusted but the
final gameplay screenshot reveals mode (P2 AI moves = VS-CPU; static P2 = plain 2P).
Usage: mister_nav.py [level=11]
"""
import subprocess, sys, time, os

M = os.environ.get("MISTER_HOST", "10.42.0.225")
TMP = os.path.expanduser("~/projects/dr-mario-mods/tmp")
LVL = int(sys.argv[1]) if len(sys.argv) > 1 else 11


def mc(*args, retries=3):
    for i in range(retries):
        r = subprocess.run(["misterclaw-send", "--host", M, *args],
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            return r.stdout.strip()
        time.sleep(2)
    return None


def shot(name):
    p = os.path.join(TMP, name)
    for i in range(3):
        if mc("screenshot", "--output", p) is not None and os.path.exists(p):
            return p
        time.sleep(2)
    raise RuntimeError("screenshot failed " + name)


def diff(p1, p2):
    from PIL import Image
    a = Image.open(p1).convert("RGB"); b = Image.open(p2).convert("RGB")
    if a.size != b.size:
        return 10**9
    return sum(1 for pa, pb in zip(a.getdata(), b.getdata()) if pa != pb)


def press_until_change(button, before, name, max_tries=5, settle=1.5, min_diff=500):
    """Press `button` until the screen visibly changes vs `before`. Returns new screenshot."""
    for t in range(max_tries):
        mc("input", "button", button)
        time.sleep(settle)
        after = shot(name)
        d = diff(before, after)
        if d >= min_diff:
            print(f"  {button}: changed ({d}px) after {t+1} press(es)")
            return after
        print(f"  {button}: no change (try {t+1}, {d}px)")
    raise RuntimeError(f"{button} never registered")


def press_n(button, n, settle=0.6):
    for i in range(n):
        mc("input", "button", button)
        time.sleep(settle)


def main():
    print("== relaunch ROM (clean title state) ==")
    mc("launch", "drmario_copro", "--system", "NES")
    time.sleep(7)
    title = shot("nav_0_title.png")

    print("== SELECT x2: 1P -> 2P (visible) -> VS-CPU (invisible) ==")
    after_sel1 = press_until_change("select", title, "nav_1_sel1.png", min_diff=50)
    mc("input", "button", "select")          # 2P -> VS-CPU: no visual change, trust one press
    time.sleep(1.5)

    print("== START -> level select ==")
    lvlsel = press_until_change("start", after_sel1, "nav_2_lvlsel.png")

    print(f"== level: LEFT x25 then RIGHT x{LVL} ==")
    press_n("left", 25, settle=0.45)
    press_n("right", LVL, settle=0.5)
    shot("nav_3_level.png")

    print("== START -> match ==")
    press_until_change("start", os.path.join(TMP, "nav_3_level.png"), "nav_4_game.png")

    print("== gameplay: shots at t+5/15/30/45/60s (P2 motion = VS-CPU AI live) ==")
    for t in (5, 15, 30, 45, 60):
        time.sleep(t - (0 if t == 5 else [5, 15, 30, 45][[15, 30, 45, 60].index(t)]))
        shot(f"nav_5_t{t:02d}.png")
        print(f"  t={t}s captured")
    print("done — read nav_*.png")


if __name__ == "__main__":
    main()

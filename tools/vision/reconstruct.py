#!/usr/bin/env python3
"""Reconstruct a settled-board timeline and (board, move) events from a
sequence of per-frame classified boards, self-validated by Dr. Mario's
legal-transition rules.

Pipeline
--------
1. CONFIRMED STACK: the moving capsule and the clear "flash" animation are
   transient; a cell is admitted to the settled stack only once it holds one
   value for K consecutive samples AND is supported (resting on floor / a
   filled cell below), viruses excepted. This filters the active pill.
2. SETTLED TIMELINE: emit the stack whenever it goes quiescent (unchanged for
   Q samples) and differs from the last emitted settled board.
3. MOVE EVENTS: between consecutive settled boards S -> S', diff the cells.
   The active capsule observed just before the change gives the placement.
4. LEGALITY ORACLE: a transition is legal if it is a pure capsule lock (two
   adjacent pill-halves added, nothing else changed) OR resolve(S + capsule)
   == S' under Dr. Mario clear+gravity rules. Illegal transitions are OCR
   errors; we retry after single-cell corrections.

Colour/kind cells are (color, is_virus) with color in {0 empty,1 R,2 Y,3 B}.
"""
from __future__ import annotations
import sys, json
from copy import deepcopy
sys.path.insert(0, "/home/struktured/projects/dr-mario-mods/tools/vision")
import classify as C

EMPTY = C.EMPTY
ROWS, COLS = 16, 8


# ------------------------------- board utils --------------------------------

def empty_board():
    return [[(EMPTY, False)] * COLS for _ in range(ROWS)]


def filled(board, r, c):
    return board[r][c][0] != EMPTY


def board_eq(a, b):
    return all(a[r][c] == b[r][c] for r in range(ROWS) for c in range(COLS))


def to_ascii(board):
    out = []
    for row in board:
        s = ""
        for color, isv in row:
            ch = C.COLOR_NAME[color]
            s += ch if (color == EMPTY or isv) else ch.lower()
        out.append(s)
    return out


def virus_count(board):
    return sum(1 for row in board for col, isv in row if col != EMPTY and isv)


# ---------------------------- Dr. Mario resolver ----------------------------

def _clear_mask(board):
    """Cells belonging to any horizontal/vertical run of >=4 same colour."""
    mark = [[False] * COLS for _ in range(ROWS)]
    for r in range(ROWS):
        c = 0
        while c < COLS:
            if not filled(board, r, c):
                c += 1; continue
            col = board[r][c][0]; c2 = c
            while c2 < COLS and filled(board, r, c2) and board[r][c2][0] == col:
                c2 += 1
            if c2 - c >= 4:
                for cc in range(c, c2):
                    mark[r][cc] = True
            c = c2
    for c in range(COLS):
        r = 0
        while r < ROWS:
            if not filled(board, r, c):
                r += 1; continue
            col = board[r][c][0]; r2 = r
            while r2 < ROWS and filled(board, r2, c) and board[r2][c][0] == col:
                r2 += 1
            if r2 - r >= 4:
                for rr in range(r, r2):
                    mark[rr][c] = True
            r = r2
    return mark


def _apply_gravity(board):
    """Independent-half gravity: every pill-half falls straight down until it
    rests; viruses never move. (Approximation -- capsule-link pairing is not
    recoverable from colour-only vision; adequate for single clears, may
    mis-order rare multi-piece cascades.)"""
    moved = False
    for c in range(COLS):
        # collect movable (pills) keeping viruses pinned
        write_r = ROWS - 1
        # walk from bottom; place pills as low as possible, keep viruses fixed
        stack = []
        for r in range(ROWS - 1, -1, -1):
            cell = board[r][c]
            if cell[0] == EMPTY:
                continue
            stack.append((r, cell))
        # rebuild column: viruses stay at their row, pills settle onto floor/others
        newcol = [(EMPTY, False)] * ROWS
        for r in range(ROWS):
            if board[r][c][0] != EMPTY and board[r][c][1]:  # virus pinned
                newcol[r] = board[r][c]
        # drop pills into remaining gaps from the bottom
        pills = [board[r][c] for r in range(ROWS) if board[r][c][0] != EMPTY and not board[r][c][1]]
        rr = ROWS - 1
        for cell in reversed(pills):  # bottom-most pill first
            while rr >= 0 and newcol[rr][0] != EMPTY:
                rr -= 1
            if rr < 0:
                break
            newcol[rr] = cell
            rr -= 1
        for r in range(ROWS):
            if board[r][c] != newcol[r]:
                moved = True
            board[r][c] = newcol[r]
    return moved


def resolve(board):
    """Clear >=4 lines, apply gravity, cascade until stable.
    -> (resolved_board, cleared_cells, cleared_virus_positions:set)."""
    board = deepcopy(board)
    total_cells = 0; cleared_vir = set()
    for _ in range(64):
        mark = _clear_mask(board)
        ncleared = sum(mark[r][c] for r in range(ROWS) for c in range(COLS))
        if ncleared == 0:
            break
        for r in range(ROWS):
            for c in range(COLS):
                if mark[r][c]:
                    if board[r][c][1]:
                        cleared_vir.add((r, c))
                    board[r][c] = (EMPTY, False)
                    total_cells += 1
        _apply_gravity(board)
    return board, total_cells, cleared_vir


def place_capsule(board, cells):
    """Return board with capsule cells [(r,c,color)] added as pill-halves."""
    b = deepcopy(board)
    for r, c, color in cells:
        b[r][c] = (color, False)
    return b


# --------------------------- confirmed-stack tracker ------------------------

class StackTracker:
    def __init__(self, K=4, Q=2, support=False):
        self.K = K; self.Q = Q; self.support = support
        self.hist = []                 # last K frame boards
        self.stack = empty_board()
        self.quiet = 0                 # frames since stack last changed
        self.settled = []             # list of (approx_index, stack_snapshot)
        self.last_emitted = None
        self.active_hist = []          # active capsule per frame (for placement)

    def _supported(self, r, c, cur):
        if r == ROWS - 1:
            return True
        # supported by confirmed stack or the current frame below
        return (self.stack[r + 1][c][0] != EMPTY) or (cur[r + 1][c][0] != EMPTY)

    def push(self, idx, board):
        self.hist.append(board)
        if len(self.hist) > self.K:
            self.hist.pop(0)
        changed = False
        if len(self.hist) == self.K:
            for r in range(ROWS):
                for c in range(COLS):
                    vals = [h[r][c] for h in self.hist]
                    if all(v == vals[0] for v in vals):
                        v = vals[0]
                        if v[0] != EMPTY and not v[1] and self.support and not self._supported(r, c, board):
                            continue  # floating held capsule -> not settled
                        if self.stack[r][c] != v:
                            self.stack[r][c] = v
                            changed = True
        # active capsule = filled cells in current frame not in confirmed stack
        active = [(r, c, board[r][c][0]) for r in range(ROWS) for c in range(COLS)
                  if board[r][c][0] != EMPTY and self.stack[r][c][0] == EMPTY]
        self.active_hist.append((idx, active))
        if changed:
            self.quiet = 0
        else:
            self.quiet += 1
        # emit quiescent stack
        if self.quiet == self.Q:
            snap = deepcopy(self.stack)
            if self.last_emitted is None or not board_eq(snap, self.last_emitted):
                self.settled.append((idx, snap))
                self.last_emitted = snap

    def recent_capsule(self, before_idx):
        """The last well-formed 2-cell capsule seen before `before_idx`."""
        for idx, active in reversed(self.active_hist):
            if idx >= before_idx:
                continue
            if len(active) == 2 and _is_domino([(r, c) for r, c, _ in active]):
                return active
        return None


def _is_domino(cells):
    (r0, c0), (r1, c1) = sorted(cells)
    return (r0 == r1 and c1 == c0 + 1) or (c0 == c1 and r1 == r0 + 1)


# ------------------------------ move extraction -----------------------------

def diff_cells(S, Sp):
    added, removed, changed = [], [], []
    for r in range(ROWS):
        for c in range(COLS):
            a, b = S[r][c], Sp[r][c]
            if a[0] == EMPTY and b[0] != EMPTY:
                added.append((r, c, b))
            elif a[0] != EMPTY and b[0] == EMPTY:
                removed.append((r, c, a))
            elif a != b:
                changed.append((r, c, a, b))
    return added, removed, changed


def _pure_lock(S, Sp):
    """If S' is S plus exactly one capsule (2 adjacent pill-halves, nothing
    removed/changed) -> move dict, else None."""
    added, removed, changed = diff_cells(S, Sp)
    if len(added) == 2 and not removed and not changed:
        cells = [(r, c) for r, c, _ in added]
        if _is_domino(cells) and all(not v[1] for _, _, v in added):
            (r0, c0, v0), (r1, c1, v1) = sorted(added)
            return {"orient": "H" if r0 == r1 else "V",
                    "cells": [[r0, c0], [r1, c1]],
                    "colors": [C.COLOR_NAME[v0[0]], C.COLOR_NAME[v1[0]]],
                    "cleared": 0, "cleared_viruses": 0}
    return None


def _candidate_anchor_cells(S, Sp):
    """Empty cells in S near the changed region -- where a locking capsule
    could have rested to produce the clear that yields S'."""
    _, removed, changed = diff_cells(S, Sp)
    hot = set((r, c) for r, c, _ in removed) | set((r, c) for r, c, _, _ in changed)
    # include empty cells above the removed region (the capsule sits on top)
    cand = set()
    for (r, c) in hot:
        for dr in range(-2, 2):
            for dc in (-1, 0, 1):
                rr, cc = r + dr, c + dc
                if 0 <= rr < ROWS and 0 <= cc < COLS and S[rr][cc][0] == EMPTY:
                    cand.add((rr, cc))
    return cand


def hamming(a, b):
    return sum(1 for r in range(ROWS) for c in range(COLS) if a[r][c] != b[r][c])


def _search_capsule(S, Sp):
    """Search capsule placements P (bounded to the changed region) minimizing
    hamming(resolve(S+P), Sp). Returns (move_dict, best_hamming) or (None, BIG).
    Tolerance absorbs single-cell OCR noise and gravity-link approximation."""
    colors = [C.R, C.Y, C.B]
    # viruses present in S that are gone/changed in Sp = viruses that cleared
    removed_vir = set((r, c) for r in range(ROWS) for c in range(COLS)
                      if S[r][c][0] != EMPTY and S[r][c][1] and Sp[r][c] != S[r][c])
    anchors = _candidate_anchor_cells(S, Sp)
    best = None    # (sort_key, move, ham, virus_ok)
    seen = set()
    for (r, c) in anchors:
        placements = []
        if c + 1 < COLS and S[r][c + 1][0] == EMPTY:
            placements.append(("H", (r, c), (r, c + 1)))
        if c - 1 >= 0 and S[r][c - 1][0] == EMPTY:
            placements.append(("H", (r, c - 1), (r, c)))
        if r + 1 < ROWS and S[r + 1][c][0] == EMPTY:
            placements.append(("V", (r, c), (r + 1, c)))
        if r - 1 >= 0 and S[r - 1][c][0] == EMPTY:
            placements.append(("V", (r - 1, c), (r, c)))
        for orient, p0, p1 in placements:
            key = (p0, p1)
            if key in seen:
                continue
            seen.add(key)
            for a in colors:
                for b in colors:
                    cap = [(p0[0], p0[1], a), (p1[0], p1[1], b)]
                    res, ncell, cvir = resolve(place_capsule(S, cap))
                    if ncell == 0:
                        continue
                    h = hamming(res, Sp)
                    virus_ok = (cvir == removed_vir)
                    key_sort = (0 if virus_ok else 1, h)
                    mv = {"orient": orient, "cells": [list(p0), list(p1)],
                          "colors": [C.COLOR_NAME[a], C.COLOR_NAME[b]],
                          "cleared": ncell, "cleared_viruses": len(cvir)}
                    if best is None or key_sort < best[0]:
                        best = (key_sort, mv, h, virus_ok)
                        if virus_ok and h == 0:
                            return best
    return best


def classify_transition(S, Sp, tol=1):
    """-> (kind, move_dict|None, hamming, verified). kind in {noop, pure_lock,
    clear, illegal}. `verified` True when the transition is provably Dr.Mario-
    legal (exact reproduction, or a clear whose cascade removes exactly the
    viruses that vanished)."""
    if board_eq(S, Sp):
        return "noop", None, 0, True
    mv = _pure_lock(S, Sp)
    if mv is not None:
        return "pure_lock", mv, 0, True
    _, removed, changed = diff_cells(S, Sp)
    if removed or changed:            # something disappeared -> a clear
        best = _search_capsule(S, Sp)
        if best is not None:
            _key, mv, h, virus_ok = best
            n_removed_vir = sum(1 for r in range(ROWS) for c in range(COLS)
                                if S[r][c][0] != EMPTY and S[r][c][1] and Sp[r][c] != S[r][c])
            # virus clear proven by exact virus-set match; pill-only clear needs
            # the reconstructed aftermath to essentially agree (ham small).
            if virus_ok and (n_removed_vir > 0 or h <= 2):
                return "clear", mv, h, True
            if h <= tol:
                return "clear", mv, h, False
    return "illegal", None, 999, False


def try_single_cell_fix(S, Sp):
    """Make an illegal S->S' legal by toggling ONE cell of S' (single-cell OCR
    error). Returns (fixed_Sp, move) or (None, None)."""
    cands = [(EMPTY, False)] + [(col, k) for col in (C.R, C.Y, C.B) for k in (False, True)]
    for r in range(ROWS):
        for c in range(COLS):
            orig = Sp[r][c]
            for cand in cands:
                if cand == orig:
                    continue
                Sp[r][c] = cand
                mv = _pure_lock(S, Sp)
                if mv is not None:
                    fixed = deepcopy(Sp); Sp[r][c] = orig
                    return fixed, mv
                Sp[r][c] = orig
    return None, None


# ------------------------------- driver -------------------------------------

def _skip_initial_fill(settled):
    """Drop leading entries up to and including the board-population burst
    (game start): the last big virus jump. Return start index into settled."""
    start = 0
    for k in range(1, len(settled)):
        added, _, _ = diff_cells(settled[k - 1][1], settled[k][1])
        if len(added) > 20:
            start = k
    return start


def reconstruct(frames, player, K=4, Q=2, coalesce=2, tol=1):
    """frames: per-frame records (compact board under `player`, None if not
    live). Returns (settled, moves, stats).

    Consecutive settled stacks are coalesced (look-ahead `coalesce`) to merge
    split-capsule artifacts, then validated by Dr. Mario legality. A transition
    is legal-exact if it resolves to the observed next stack with hamming 0,
    legal-after-correction if hamming <= `tol` (single-cell OCR noise), else
    illegal (residual OCR/tracking failure)."""
    import extract as E
    tr = StackTracker(K=K, Q=Q)
    for rec in frames:
        if rec.get("live"):
            tr.push(rec["i"], E.compact_to_board(rec[player]))
    settled = tr.settled
    s0 = _skip_initial_fill(settled)

    moves = []
    stats = {"settled_states": len(settled), "transitions": 0,
             "pure_lock": 0, "clear_exact": 0, "clear_virus_verified": 0,
             "corrected": 0, "illegal": 0, "ham_hist": {}}
    k = s0
    while k + 1 < len(settled):
        i_a, A = settled[k]
        # choose the look-ahead target giving the best-verified, lowest-hamming
        # legal fit (merges split-capsule artifacts across up to `coalesce`).
        best = None  # (sort_key, j, kind, move, ham, verified, target)
        for j in range(1, coalesce + 1):
            if k + j >= len(settled):
                break
            B = settled[k + j][1]
            kind, mv, h, verified = classify_transition(A, B, tol=tol)
            if kind in ("pure_lock", "clear"):
                sort_key = (0 if verified else 1, h)
                if best is None or sort_key < best[0]:
                    best = (sort_key, j, kind, mv, h, verified, B)
            if best is not None and best[0] == (0, 0):
                break

        if best is None:
            stats["transitions"] += 1
            stats["illegal"] += 1
            a, r, c = diff_cells(A, settled[k + 1][1])
            shape = ("split_add" if (len(a) >= 1 and not r and not c and
                                     not _pure_lock(A, settled[k + 1][1]))
                     else "clear_unmatched" if (r or c) else "other")
            stats.setdefault("illegal_shapes", {})
            stats["illegal_shapes"][shape] = stats["illegal_shapes"].get(shape, 0) + 1
            k += 1
            continue

        _key, j, kind, mv, h, verified, target = best
        stats["transitions"] += 1
        stats["ham_hist"][h] = stats["ham_hist"].get(h, 0) + 1
        is_clear = kind == "clear" and mv.get("cleared", 0) > 0
        if h == 0:
            stats["clear_exact" if is_clear else "pure_lock"] += 1
            legality = "clear" if is_clear else "pure_lock"
        elif verified:                       # clear proven via virus-set match
            stats["clear_virus_verified"] += 1
            legality = "clear_virus_verified"
        else:                                # single-cell OCR correction
            stats["corrected"] += 1
            legality = "corrected"
        moves.append({
            "sample_i": settled[k + j][0], "player": player,
            "legality": legality, "residual_cells": h,
            "board_before": to_ascii(A),
            "board_before_nes": C.to_nes(A),
            "placement": mv,
            "board_after": to_ascii(target),
            "virus_before": virus_count(A),
            "virus_after": virus_count(target),
        })
        k += j
    stats["moves"] = len(moves)
    tr_ = stats["transitions"] or 1
    # "before correction" = exactly reproduced transitions (hamming 0).
    stats["legal_before_correction"] = stats["pure_lock"] + stats["clear_exact"]
    # "after correction" adds virus-provable clears + single-cell OCR fixes.
    stats["legal_after_correction"] = (stats["legal_before_correction"]
                                       + stats["clear_virus_verified"] + stats["corrected"])
    stats["pct_legal_before"] = round(100 * stats["legal_before_correction"] / tr_, 1)
    stats["pct_legal_after"] = round(100 * stats["legal_after_correction"] / tr_, 1)
    return settled, moves, stats


if __name__ == "__main__":
    path = sys.argv[1]; player = sys.argv[2] if len(sys.argv) > 2 else "p2"
    frames = [json.loads(l) for l in open(path)]
    settled, moves, stats = reconstruct(frames, player)
    print(json.dumps(stats, indent=2))

#!/usr/bin/env python3
"""Produce the Milestone-1 deliverable for one game: (board, move) events for
both players + a stats summary. Reads a per-frame board dump (extract.py dump)
and writes moves JSONL."""
import sys, json
sys.path.insert(0, "/home/struktured/projects/dr-mario-mods/tools/vision")
import reconstruct as RC

CFG = dict(K=4, Q=2, coalesce=4, tol=1)


def main(dump_path, out_path, players=("p1", "p2")):
    frames = [json.loads(l) for l in open(dump_path)]
    all_moves = []
    summary = {}
    for p in players:
        _, moves, stats = RC.reconstruct(frames, p, **CFG)
        all_moves.extend(moves)
        summary[p] = stats
    all_moves.sort(key=lambda m: (m["sample_i"], m["player"]))
    with open(out_path, "w") as fh:
        for m in all_moves:
            fh.write(json.dumps(m) + "\n")
    summary["config"] = CFG
    summary["total_moves"] = len(all_moves)
    summary["dump"] = dump_path
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

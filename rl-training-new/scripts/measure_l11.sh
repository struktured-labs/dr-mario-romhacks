#!/bin/bash
# Measure a ROM's L11 play quality over N independent games (RNG-varied seeds).
# Usage: measure_l11.sh <rom.nes> [N] [frames]
set -u
ROM="${1:?need rom path}"
N="${2:-4}"
FRAMES="${3:-9000}"
ROOT=/home/struktured/projects/dr-mario-mods
LUA="$ROOT/rl-training-new/lua/mesen_bridge_file.lua"
REL="$ROOT/mesen2/bin/linux-x64/Release"
SEEDS=(4919 27644 9001 51234 17 60123 333 41999)
total=0; best=0; results=()
for i in $(seq 1 "$N"); do
  seed=${SEEDS[$(( (i-1) % ${#SEEDS[@]} ))]}
  pkill -9 -f Mesen 2>/dev/null; sleep 2
  rm -f "$REL/mesen_ready.txt" "$REL/mesen_cmd.txt" "$REL/mesen_response.txt"
  nohup "$ROOT/run_mesen.sh" "$ROOT/$(basename "$ROM")" "$LUA" --donotsavesettings \
        > "$ROOT/mesen_measure.log" 2>&1 &
  for t in $(seq 1 10); do sleep 1; [ -f "$REL/mesen_ready.txt" ] && break; done
  cleared=$(cd "$ROOT" && DRM_SEED=$seed PYTHONPATH=rl-training-new/src \
        timeout 200 python3 -u rl-training-new/scripts/validate_l11.py "$FRAMES" 2>&1 \
        | grep -oE "cleared [0-9]+" | grep -oE "[0-9]+")
  cleared=${cleared:-0}
  results+=("seed=$seed:$cleared")
  total=$((total + cleared))
  [ "$cleared" -gt "$best" ] && best=$cleared
  echo "  game $i (seed $seed): cleared $cleared"
done
echo "=== $(basename "$ROM"): games=$N  total_cleared=$total  avg=$(awk "BEGIN{printf \"%.1f\", $total/$N}")  best=$best  [${results[*]}] ==="

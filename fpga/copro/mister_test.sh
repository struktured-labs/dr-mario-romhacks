#!/bin/bash
# Hardware test: drmario_copro.nes on the coprocessor NES core (mapper 100).
# Drives the VS-CPU menu with misterclaw virtual buttons (physical controllers not needed)
# and screenshots P2's AI progress. Usage: ./mister_test.sh [level, default 11]
set -e
M=${MISTER_HOST:-10.42.0.225}
LVL=${1:-11}
SHOTS=~/projects/dr-mario-mods/tmp
mkdir -p "$SHOTS"

snd() { misterclaw-send --host "$M" "$@"; }
btn() { snd input button "$1" >/dev/null; sleep "${2:-0.8}"; }
dpd() { snd input dpad "$1" >/dev/null; sleep "${2:-0.35}"; }

echo "== launch =="
snd launch "drmario_copro" --system NES
sleep 6
snd screenshot --output "$SHOTS/copro_00_title.png" >/dev/null
echo "title screenshot: $SHOTS/copro_00_title.png"

echo "== nav: SELECT x2 (1P -> 2P -> VS-CPU), START =="
btn select 1.0
btn select 1.0
btn start 2.0
snd screenshot --output "$SHOTS/copro_01_levelsel.png" >/dev/null

echo "== level: LEFT x25 (clamp 0) then RIGHT x$LVL =="
for i in $(seq 25); do dpd left 0.25; done
for i in $(seq "$LVL"); do dpd right 0.3; done
snd screenshot --output "$SHOTS/copro_02_level.png" >/dev/null

echo "== start match =="
btn start 3.0
snd screenshot --output "$SHOTS/copro_03_start.png" >/dev/null

echo "== watch P2 AI (screenshot every 10s x 9) =="
for i in $(seq 9); do
  sleep 10
  snd screenshot --output "$SHOTS/copro_1${i}_t$((i*10))s.png" >/dev/null
  echo "  t=$((i*10))s -> copro_1${i}_t$((i*10))s.png"
done
echo "done — inspect $SHOTS/copro_*.png"

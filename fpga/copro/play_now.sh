#!/bin/bash
# Manual-drive to VS-CPU L11 on the coprocessor cart using ONLY inputs misterclaw supports
# (dpad + start; NOT select — misterclaw's virtual pad doesn't declare SELECT).
# Note: without SELECT you cannot reach VS-CPU mode from the title. This script advances
# through 1-PLAYER mode (which the FPGA coprocessor can still play via P1) and lets you
# watch the second 6502 think in real time.
# Usage: ./play_now.sh [level=11]
M=${MISTER_HOST:-10.42.0.225}
LVL=${1:-11}
snd() { misterclaw-send --host "$M" "$@"; }
snd launch "drmario_copro" --system NES; sleep 6
snd input button start >/dev/null; sleep 2      # title -> level select
for i in $(seq 25); do snd input dpad left >/dev/null; sleep 0.25; done
for i in $(seq "$LVL"); do snd input dpad right >/dev/null; sleep 0.3; done
snd input button start >/dev/null; sleep 2      # level -> match
echo "match started; watch screen"

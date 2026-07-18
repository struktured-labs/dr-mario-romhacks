#!/usr/bin/env bash
# build_firmware.sh — (re)generate copro_rom.hex, the CoproDrMario firmware ROM ($8000-$BFFF window
# that its `initial $readmemh("copro_rom.hex", rom)` loads).
#
# The firmware is assembled by the repo's Python 6502 assembler (NOT an external toolchain), so this
# must run inside the dr-mario-mods checkout with its Python env available. build_interface.py drives
# build_resumable_incr() -> a 64KB image, and writes img[$8000:$C000] to copro_rom.hex (16384 bytes).
#
# NOTE: for milestone 3 you normally do NOT need to rebuild -- the committed copro_rom.hex is already
# validated (6/6 vs the py65 oracle) and sync_to_pocket.sh vendors it as-is. Rebuild only when the
# search firmware itself changes, and confirm the drop_setup below matches the deployed build.
#
# Usage:  ./build_firmware.sh [drop_setup] [ncases]
#   drop_setup: 0 = exact-oracle search ; 1 = shipping ~66%-clear variant   (default 1)
#   ncases    : number of host test problems written to hostdata.txt        (default 6)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DROP="${1:-1}"
NCASES="${2:-6}"

cd "$HERE"
echo ">> build_interface.py drop_setup=${DROP} ncases=${NCASES}"
python3 build_interface.py "$DROP" "$NCASES"

if [ ! -s copro_rom.hex ]; then
  echo "ERROR: copro_rom.hex was not produced" >&2; exit 1
fi
echo "OK: $(pwd)/copro_rom.hex  ($(wc -l < copro_rom.hex) lines / bytes, drop_setup=${DROP})"
echo "    next: ./sync_to_pocket.sh   to vendor it into the Pocket tree."

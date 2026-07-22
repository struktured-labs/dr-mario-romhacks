import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from title_screen import (
    CHR_PAGE_SIZE,
    CHR_START,
    FOOTER_CHR_PAGE,
    FOOTER_DATA_OFFSET,
    FOOTER_HOOK_OFFSET,
    FOOTER_HOOK_PATCHED,
    FOOTER_METASPRITE,
    FOOTER_ROUTINE,
    FOOTER_ROUTINE_OFFSET,
    FOOTER_TILE_IDS,
    TITLE_BOTTOM_BASE_TILE_IDS,
    TITLE_CHR_PAGES,
    TITLE_TILEMAP_OFFSET,
    TITLE_TOP_TILE_IDS,
    _decode_strip,
    apply_training_edition_title,
)


def _allowed_offsets():
    allowed = set(range(TITLE_TILEMAP_OFFSET, TITLE_TILEMAP_OFFSET + 10))
    allowed.update(range(FOOTER_HOOK_OFFSET, FOOTER_HOOK_OFFSET + 3))
    allowed.update(range(FOOTER_ROUTINE_OFFSET, FOOTER_ROUTINE_OFFSET + len(FOOTER_ROUTINE)))
    allowed.update(range(FOOTER_DATA_OFFSET, FOOTER_DATA_OFFSET + len(FOOTER_METASPRITE)))
    for page in TITLE_CHR_PAGES:
        for tile_id in TITLE_TOP_TILE_IDS:
            off = CHR_START + page * CHR_PAGE_SIZE + tile_id * 16
            allowed.update(range(off, off + 16))
    for tile_id in FOOTER_TILE_IDS:
        off = CHR_START + FOOTER_CHR_PAGE * CHR_PAGE_SIZE + tile_id * 16
        allowed.update(range(off, off + 16))
    return allowed


def test_training_edition_title_is_a_scoped_patch():
    original = Path("drmario.nes").read_bytes()
    patched = bytearray(original)

    assert bytes(
        patched[TITLE_TILEMAP_OFFSET:TITLE_TILEMAP_OFFSET + 10]
    ) == bytes(TITLE_BOTTOM_BASE_TILE_IDS)
    assert apply_training_edition_title(patched) == 28

    changed = {i for i, (before, after) in enumerate(zip(original, patched)) if before != after}
    assert changed
    assert changed <= _allowed_offsets()
    assert bytes(
        patched[TITLE_TILEMAP_OFFSET:TITLE_TILEMAP_OFFSET + 10]
    ) == bytes(TITLE_BOTTOM_BASE_TILE_IDS)
    assert bytes(patched[FOOTER_HOOK_OFFSET:FOOTER_HOOK_OFFSET + 3]) == FOOTER_HOOK_PATCHED


def test_training_edition_art_matches_in_both_title_chr_pages():
    patched = bytearray(Path("drmario.nes").read_bytes())
    apply_training_edition_title(patched)

    canvases = []
    for page in TITLE_CHR_PAGES:
        top = _decode_strip(patched, page, TITLE_TOP_TILE_IDS)
        bottom = _decode_strip(patched, page, TITLE_BOTTOM_BASE_TILE_IDS)
        canvases.append(top + bottom)

    assert canvases[0] == canvases[1]
    colors = [pixel for row in canvases[0] for pixel in row]
    assert colors.count(2) > 200  # yellow letter faces
    assert colors.count(1) > 80  # white bevel
    assert set(colors) == {0, 1, 2, 3}


def test_title_patch_is_idempotent():
    patched = bytearray(Path("drmario.nes").read_bytes())
    apply_training_edition_title(patched)
    once = bytes(patched)
    assert apply_training_edition_title(patched) == 28
    assert bytes(patched) == once

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
    footer_hook_patched,
    footer_routine,
)

# TE v8 relocates the footer routine/data off DRSTUDY's part3b ($BE56) / part2 ($9FF8) runs.
V8_ROUTINE_OFF, V8_DATA_OFF, V8_TEXT = 0x40B9, 0x4F10, "V8.00 STRUK LABS"


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


def _allowed_offsets_at(routine_off, data_off):
    allowed = set(range(TITLE_TILEMAP_OFFSET, TITLE_TILEMAP_OFFSET + 10))
    allowed.update(range(FOOTER_HOOK_OFFSET, FOOTER_HOOK_OFFSET + 3))
    allowed.update(range(routine_off, routine_off + len(footer_routine(data_off))))
    allowed.update(range(data_off, data_off + len(FOOTER_METASPRITE)))
    for page in TITLE_CHR_PAGES:
        for tile_id in TITLE_TOP_TILE_IDS:
            off = CHR_START + page * CHR_PAGE_SIZE + tile_id * 16
            allowed.update(range(off, off + 16))
    for tile_id in FOOTER_TILE_IDS:
        off = CHR_START + FOOTER_CHR_PAGE * CHR_PAGE_SIZE + tile_id * 16
        allowed.update(range(off, off + 16))
    return allowed


def test_footer_helpers_reproduce_v7_defaults():
    # The parameterized helpers must reconstruct the exact committed v7 bytes.
    assert footer_routine(FOOTER_DATA_OFFSET) == FOOTER_ROUTINE
    assert footer_hook_patched(FOOTER_ROUTINE_OFFSET) == FOOTER_HOOK_PATCHED


def test_relocated_v8_footer_is_a_scoped_patch():
    original = Path("drmario.nes").read_bytes()
    patched = bytearray(original)
    assert apply_training_edition_title(
        patched, routine_off=V8_ROUTINE_OFF, data_off=V8_DATA_OFF, footer_text=V8_TEXT) == 28

    changed = {i for i, (a, b) in enumerate(zip(original, patched)) if a != b}
    assert changed
    assert changed <= _allowed_offsets_at(V8_ROUTINE_OFF, V8_DATA_OFF)
    # hook -> JSR $C0A9; routine carries the $CF00 data pointer; metasprite at $CF00
    assert bytes(patched[FOOTER_HOOK_OFFSET:FOOTER_HOOK_OFFSET + 3]) == footer_hook_patched(V8_ROUTINE_OFF)
    routine = footer_routine(V8_DATA_OFF)
    assert bytes(patched[V8_ROUTINE_OFF:V8_ROUTINE_OFF + len(routine)]) == routine
    assert bytes(patched[V8_DATA_OFF:V8_DATA_OFF + len(FOOTER_METASPRITE)]) == FOOTER_METASPRITE


def test_relocated_v8_footer_is_idempotent():
    patched = bytearray(Path("drmario.nes").read_bytes())
    kw = dict(routine_off=V8_ROUTINE_OFF, data_off=V8_DATA_OFF, footer_text=V8_TEXT)
    apply_training_edition_title(patched, **kw)
    once = bytes(patched)
    assert apply_training_edition_title(patched, **kw) == 28
    assert bytes(patched) == once


def test_v8_footer_leaves_drstudy_runs_intact():
    # The whole point of the relocation: applied on top of the v6 study ROM, the branding
    # must not touch DRSTUDY's part2 ($9FF8) / part3b ($BE56) dead runs.
    import os
    import tempfile

    import patch_vs_cpu
    from patch_cartridge_copro import (
        apply_study_pause, STUDY_BLOB2, STUDY_BLOB2_CPU, STUDY_BLOB4, STUDY_BLOB4_CPU)

    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "v6.nes")
        patch_vs_cpu.apply_patches("drmario.nes", out)
        rom = bytearray(Path(out).read_bytes())
    apply_study_pause(rom)

    p2 = 16 + (STUDY_BLOB2_CPU - 0x8000)
    p4 = 16 + (STUDY_BLOB4_CPU - 0x8000)
    assert bytes(rom[p2:p2 + len(STUDY_BLOB2)]) == STUDY_BLOB2  # study present pre-branding
    assert bytes(rom[p4:p4 + len(STUDY_BLOB4)]) == STUDY_BLOB4

    apply_training_edition_title(rom, routine_off=V8_ROUTINE_OFF, data_off=V8_DATA_OFF, footer_text=V8_TEXT)

    assert bytes(rom[p2:p2 + len(STUDY_BLOB2)]) == STUDY_BLOB2  # study still present post-branding
    assert bytes(rom[p4:p4 + len(STUDY_BLOB4)]) == STUDY_BLOB4

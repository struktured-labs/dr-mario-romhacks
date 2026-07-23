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
    TM_TILE_ID,
    TM_M_HALF,
    TE_E_HALF,
    _decode_strip,
    _tile_offset,
    apply_training_edition_title,
    footer_hook_patched,
    footer_layout,
    footer_metasprite,
    footer_routine,
)

# TE v8 relocates the footer routine/data off DRSTUDY's part3b ($BE56) / part2 ($9FF8) runs and
# into two 24-byte runs free in base v6 AND the v28cs/copro carts (so the v8 BPS is the cart
# byte-basis).  The credit is shortened to "V8.00 SL" -> a 4-tile, 17-byte metasprite.
V8_ROUTINE_OFF, V8_DATA_OFF, V8_TEXT = 0x40B9, 0x40FF, "V8.00 SL"


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


def _allowed_offsets_at(routine_off, data_off, footer_text, mark_te=True):
    n_tiles, base_x = footer_layout(footer_text)
    allowed = set(range(TITLE_TILEMAP_OFFSET, TITLE_TILEMAP_OFFSET + 10))
    allowed.update(range(FOOTER_HOOK_OFFSET, FOOTER_HOOK_OFFSET + 3))
    allowed.update(range(routine_off, routine_off + len(footer_routine(data_off, base_x))))
    allowed.update(range(data_off, data_off + len(footer_metasprite(n_tiles))))
    for page in TITLE_CHR_PAGES:
        for tile_id in TITLE_TOP_TILE_IDS:
            off = CHR_START + page * CHR_PAGE_SIZE + tile_id * 16
            allowed.update(range(off, off + 16))
    for i in range(n_tiles):
        off = CHR_START + FOOTER_CHR_PAGE * CHR_PAGE_SIZE + (FOOTER_TILE_IDS[0] + i) * 16
        allowed.update(range(off, off + 16))
    if mark_te:
        for page in TITLE_CHR_PAGES:
            off = CHR_START + page * CHR_PAGE_SIZE + TM_TILE_ID * 16
            allowed.update(range(off, off + 16))
    return allowed


def test_footer_helpers_reproduce_v7_defaults():
    # The parameterized helpers must reconstruct the exact committed v7 bytes.
    assert footer_routine(FOOTER_DATA_OFFSET) == FOOTER_ROUTINE
    assert footer_hook_patched(FOOTER_ROUTINE_OFFSET) == FOOTER_HOOK_PATCHED


def test_relocated_v8_footer_is_a_scoped_patch():
    original = Path("drmario.nes").read_bytes()
    patched = bytearray(original)
    # subtitle (10x2) + footer (4 for "V8.00 SL") + TM->TE mark (1 tile x 2 pages) = 26 CHR tiles
    assert apply_training_edition_title(
        patched, routine_off=V8_ROUTINE_OFF, data_off=V8_DATA_OFF, footer_text=V8_TEXT, mark_te=True) == 26

    changed = {i for i, (a, b) in enumerate(zip(original, patched)) if a != b}
    assert changed
    assert changed <= _allowed_offsets_at(V8_ROUTINE_OFF, V8_DATA_OFF, V8_TEXT, mark_te=True)
    # hook -> JSR $C0A9; routine carries the $C0EF data pointer; metasprite (<=24 B) at $C0EF
    n_tiles, base_x = footer_layout(V8_TEXT)
    assert bytes(patched[FOOTER_HOOK_OFFSET:FOOTER_HOOK_OFFSET + 3]) == footer_hook_patched(V8_ROUTINE_OFF)
    routine = footer_routine(V8_DATA_OFF, base_x)
    assert bytes(patched[V8_ROUTINE_OFF:V8_ROUTINE_OFF + len(routine)]) == routine
    meta = footer_metasprite(n_tiles)
    assert len(meta) <= 24
    assert bytes(patched[V8_DATA_OFF:V8_DATA_OFF + len(meta)]) == meta


def test_relocated_v8_footer_is_idempotent():
    patched = bytearray(Path("drmario.nes").read_bytes())
    kw = dict(routine_off=V8_ROUTINE_OFF, data_off=V8_DATA_OFF, footer_text=V8_TEXT, mark_te=True)
    apply_training_edition_title(patched, **kw)
    once = bytes(patched)
    assert apply_training_edition_title(patched, **kw) == 26
    assert bytes(patched) == once


def test_tm_to_te_repaints_only_tile_0F_and_default_keeps_tm():
    original = Path("drmario.nes").read_bytes()

    # default (v7): the "™" M-half is untouched
    plain = bytearray(original)
    apply_training_edition_title(plain)
    for page in TITLE_CHR_PAGES:
        off = _tile_offset(page, TM_TILE_ID)
        assert bytes(plain[off:off + 16]) == TM_M_HALF
        assert bytes(original[off:off + 16]) == TM_M_HALF     # base ROM really has the "™" there

    # mark_te: tile $0F on both title CHR pages becomes the "E"; the T-half ($0E) is untouched
    marked = bytearray(original)
    apply_training_edition_title(marked, routine_off=V8_ROUTINE_OFF, data_off=V8_DATA_OFF,
                                 footer_text=V8_TEXT, mark_te=True)
    for page in TITLE_CHR_PAGES:
        assert bytes(marked[_tile_offset(page, TM_TILE_ID):_tile_offset(page, TM_TILE_ID) + 16]) == TE_E_HALF
        t_off = _tile_offset(page, 0x0E)
        assert bytes(marked[t_off:t_off + 16]) == bytes(original[t_off:t_off + 16])   # T-half kept


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

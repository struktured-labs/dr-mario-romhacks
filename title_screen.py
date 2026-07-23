"""Title-screen branding for Dr. Mario Training Edition.

The original title art leaves an 80x16-pixel pocket beneath ``MARIO``.  Dr.
Mario Turbo uses the same pocket for its subtitle.  This patch keeps the
capsule artwork intact and renders ``TRAINING EDITION`` into that space.
"""

CHR_START = 16 + 32768
CHR_PAGE_SIZE = 0x1000

TITLE_TILEMAP_OFFSET = 0x3B06
TITLE_TOP_TILE_IDS = (0xAC, 0xAD, 0xAE, 0xAF, 0xED,
                      0xEE, 0xEF, 0xDC, 0xDD, 0xDE)
TITLE_BOTTOM_BASE_TILE_IDS = (0x42,) + (0xFC,) * 9
TITLE_CHR_PAGES = (3, 4)

FOOTER_TEXT = "V7.00 STRUK LABS"
FOOTER_TILE_IDS = tuple(range(0xE8, 0xF0))
FOOTER_CHR_PAGE = 2
FOOTER_HOOK_OFFSET = 0x0C34
FOOTER_HOOK_ORIGINAL = bytes((0x20, 0xF6, 0x88))  # JSR $88F6

# The 23-byte footer routine and its 33-byte metasprite table live in dead PRG
# runs.  v7 put them at $BE56 / $9FF8, but those are DRSTUDY v3.3's part3b /
# part2 runs, so a build that also carries the study (TE v8) must relocate them
# via the routine_off / data_off parameters of apply_training_edition_title.
# The routine is position-independent apart from the two-byte pointer to its
# metasprite table, and the title hook is a JSR to the routine; both the hook
# target and that pointer are derived from the chosen offsets below.
FOOTER_ROUTINE_OFFSET = 0x3E66   # v7 default ($BE56); TE v8 overrides to a free run
FOOTER_DATA_OFFSET = 0x2008      # v7 default ($9FF8); TE v8 overrides to a free run


def _prg_cpu_addr(file_off):
    """CPU address of a byte in the linear 32 KiB Dr. Mario PRG image."""
    return file_off - 0x10 + 0x8000


def footer_hook_patched(routine_off):
    """`JSR <routine>` opcode bytes for the title hook at FOOTER_HOOK_OFFSET."""
    cpu = _prg_cpu_addr(routine_off)
    return bytes((0x20, cpu & 0xFF, (cpu >> 8) & 0xFF))


def footer_routine(data_off, base_x=0x60):
    """The footer routine: metasprite pointer -> ``data_off``, drawn from screen
    X = ``base_x`` (chosen to center the tile strip on X=128)."""
    cpu = _prg_cpu_addr(data_off)
    return bytes((
        0x20, 0xF6, 0x88,               # JSR $88F6: draw final original title metasprite
        0xA9, cpu & 0xFF, 0x85, 0x47,   # footer data pointer lo
        0xA9, (cpu >> 8) & 0xFF, 0x85, 0x48,  # footer data pointer hi
        0xA9, base_x, 0x85, 0x44,       # base X
        0xA9, 0xD7, 0x85, 0x45,         # base Y = 215 (visible row 216)
        0x20, 0x06, 0x89,               # JSR $8906: native metasprite renderer
        0x60,                           # RTS
    ))


def footer_metasprite(n_tiles, first_tile=0xE8):
    """``n_tiles`` one-tile sprites (tiles first_tile..) at X=index*8, + $80 terminator.
    N sprites = 4*N+1 bytes, so a short credit shrinks the table to fit a small dead run
    (TE v8 keeps this ≤24 B so the footer lands in a run free in the copro carts too)."""
    return bytes(v for i in range(n_tiles)
                 for v in (0x00, first_tile + i, 0x00, i * 8)) + bytes((0x80,))


def footer_layout(text):
    """(n_tiles, base_x) for ``text``: the fewest 8-pixel tiles that cover the rendered
    width, centered on screen X=128.  v7 'V7.00 STRUK LABS' -> (8, 96); a short v8 credit
    -> fewer tiles / a smaller metasprite."""
    width = sum(len(FOOTER_FONT[c][0]) for c in text) + len(text) - 1
    n_tiles = (width + 7) // 8
    return n_tiles, 128 - n_tiles * 4


FOOTER_HOOK_PATCHED = footer_hook_patched(FOOTER_ROUTINE_OFFSET)  # v7: JSR $BE56
FOOTER_ROUTINE = footer_routine(FOOTER_DATA_OFFSET)               # v7: data ptr $9FF8
FOOTER_METASPRITE = footer_metasprite(len(FOOTER_TILE_IDS))       # v7: 8 tiles, 33 bytes

# Trademark mark -> "TE".  The title's "™" is two background tiles on the title CHR pages: $0E
# (the T-half) + $0F (the M-half).  For Training Edition we repaint the M-half into an E so it
# reads "TE".  The T-half's right column already draws the E's left stem, so ONLY tile $0F
# changes; the crash-sensitive title nametable keeps $0E/$0F in place (opt-in via mark_te=).
TM_TILE_ID = 0x0F
TM_M_HALF = bytes.fromhex("fffff76797f7f7f7" * 2)   # original ™ M-half (drmario.nes, pages 3 & 4)
TE_E_HALF = bytes.fromhex("ffff0fff1fffff0f" * 2)   # repainted E (pairs with the T-half's stem)

SUBTITLE_TEXT = "TRAINING EDITION"
TRAINING_TEXT = "TRAINING"
EDITION_TEXT = "EDITION"
# A compact, heavy 4x7 face lets the complete name use the full height of the
# safe title row.  The I is deliberately three pixels wide for legibility.
FONT = {
    " ": (
        "000",
    ) * 7,
    "A": (
        "0110",
        "1001",
        "1001",
        "1111",
        "1001",
        "1001",
        "1001",
    ),
    "D": (
        "1110",
        "1001",
        "1001",
        "1001",
        "1001",
        "1001",
        "1110",
    ),
    "E": (
        "1111",
        "1000",
        "1000",
        "1110",
        "1000",
        "1000",
        "1111",
    ),
    "G": (
        "0110",
        "1001",
        "1000",
        "1011",
        "1001",
        "1001",
        "0110",
    ),
    "I": (
        "111",
        "010",
        "010",
        "010",
        "010",
        "010",
        "111",
    ),
    "N": (
        "1001",
        "1101",
        "1101",
        "1011",
        "1011",
        "1011",
        "1001",
    ),
    "O": (
        "0110",
        "1001",
        "1001",
        "1001",
        "1001",
        "1001",
        "0110",
    ),
    "R": (
        "1110",
        "1001",
        "1001",
        "1110",
        "1010",
        "1001",
        "1001",
    ),
    "T": (
        "1111",
        "0110",
        "0110",
        "0110",
        "0110",
        "0110",
        "0110",
    ),
}

FOOTER_FONT = {
    " ": ("00",) * 5,
    ".": ("0", "0", "0", "0", "1"),
    "0": ("111", "101", "101", "101", "111"),
    "7": ("111", "001", "010", "010", "010"),
    "8": ("111", "101", "111", "101", "111"),
    "A": ("010", "101", "111", "101", "101"),
    "B": ("110", "101", "110", "101", "110"),
    "K": ("101", "101", "110", "101", "101"),
    "L": ("100", "100", "100", "100", "111"),
    "R": ("110", "101", "110", "101", "101"),
    "S": ("111", "100", "111", "001", "111"),
    "T": ("111", "010", "010", "010", "010"),
    "U": ("101", "101", "101", "101", "111"),
    "V": ("101", "101", "101", "101", "010"),
}


def _tile_offset(page, tile_id):
    return CHR_START + page * CHR_PAGE_SIZE + tile_id * 16


def _decode_strip(rom, page, tile_ids):
    pixels = [[0] * (len(tile_ids) * 8) for _ in range(8)]
    for tile_x, tile_id in enumerate(tile_ids):
        off = _tile_offset(page, tile_id)
        for y in range(8):
            plane0 = rom[off + y]
            plane1 = rom[off + 8 + y]
            for x in range(8):
                bit = 7 - x
                pixels[y][tile_x * 8 + x] = (
                    ((plane1 >> bit) & 1) << 1
                ) | ((plane0 >> bit) & 1)
    return pixels


def _encode_tile(pixels):
    encoded = bytearray(16)
    for y, row in enumerate(pixels):
        for x, color in enumerate(row):
            bit = 7 - x
            encoded[y] |= (color & 1) << bit
            encoded[8 + y] |= ((color >> 1) & 1) << bit
    return bytes(encoded)


def _text_pixels():
    """Return yellow body and left-side white bevel pixels."""
    body = set()

    def draw_line(text, font, y, row_indexes, x_scale):
        width = sum(len(font[ch][0]) * x_scale for ch in text)
        width += len(text) - 1
        cursor_x = (80 - width) // 2
        for char in text:
            glyph = font[char]
            for output_y, source_y in enumerate(row_indexes):
                row = glyph[source_y]
                for glyph_x, bit in enumerate(row):
                    if bit == "1":
                        for scale_x in range(x_scale):
                            x = cursor_x + glyph_x * x_scale + scale_x
                            body.add((x, y + output_y))
            cursor_x += len(glyph[0]) * x_scale + 1
        return width

    subtitle_width = draw_line(
        SUBTITLE_TEXT, FONT, 0, range(7), 1
    )
    assert subtitle_width == 74

    bevel = {(x - 1, y) for x, y in body if x > 0}
    return body, bevel


def _footer_pixels(text=FOOTER_TEXT, n_tiles=8):
    """Return the centered 3x5 footer pixels within an ``n_tiles``-wide sprite strip."""
    width = sum(len(FOOTER_FONT[ch][0]) for ch in text) + len(text) - 1
    canvas_w = n_tiles * 8
    assert width <= canvas_w

    body = set()
    cursor_x = (canvas_w - width) // 2
    for char in text:
        glyph = FOOTER_FONT[char]
        for y, row in enumerate(glyph):
            for x, bit in enumerate(row):
                if bit == "1":
                    body.add((cursor_x + x, y + 1))
        cursor_x += len(glyph[0]) + 1
    return body


def apply_training_edition_title(rom, routine_off=FOOTER_ROUTINE_OFFSET,
                                 data_off=FOOTER_DATA_OFFSET, footer_text=FOOTER_TEXT,
                                 mark_te=False):
    """Patch a standard 64 KiB Dr. Mario ROM image in place.

    Returns the number of CHR tiles written.  The crash-sensitive title
    nametable remains original; the footer is a title-only metasprite.

    ``routine_off`` / ``data_off`` are the PRG file offsets of the footer
    routine and its metasprite table.  They default to the v7 runs ($BE56 /
    $9FF8); TE v8 relocates them off DRSTUDY's part3b / part2 runs.  The hook
    JSR target and the routine's data pointer are derived from these offsets.
    ``mark_te`` repaints the title "™" M-half tile into an E so the mark reads
    "TE" (Training Edition); off by default so v7 keeps its "™".
    """
    if len(rom) < CHR_START + 5 * CHR_PAGE_SIZE:
        raise ValueError("ROM is too small for the standard Dr. Mario CHR layout")

    current = bytes(rom[TITLE_TILEMAP_OFFSET:TITLE_TILEMAP_OFFSET + 10])
    if current != bytes(TITLE_BOTTOM_BASE_TILE_IDS):
        raise ValueError(
            f"unexpected title tilemap at 0x{TITLE_TILEMAP_OFFSET:04X}: "
            f"{current.hex()}"
        )

    body, bevel = _text_pixels()
    tiles_written = 0
    for page in TITLE_CHR_PAGES:
        top = _decode_strip(rom, page, TITLE_TOP_TILE_IDS)
        canvas = top

        # Match Turbo's palette treatment: white upper-left bevel, yellow face,
        # while retaining the pink capsule and black exterior underneath.
        for x, y in bevel:
            canvas[y][x] = 1
        for x, y in body:
            canvas[y][x] = 2

        for tile_x, tile_id in enumerate(TITLE_TOP_TILE_IDS):
            tile = [row[tile_x * 8:(tile_x + 1) * 8] for row in canvas]
            off = _tile_offset(page, tile_id)
            rom[off:off + 16] = _encode_tile(tile)
            tiles_written += 1

    n_tiles, base_x = footer_layout(footer_text)
    footer_tiles = tuple(FOOTER_TILE_IDS[0] + i for i in range(n_tiles))
    metasprite = footer_metasprite(n_tiles)

    footer = [[0] * (n_tiles * 8) for _ in range(8)]
    for x, y in _footer_pixels(footer_text, n_tiles):
        footer[y][x] = 2

    for tile_x, tile_id in enumerate(footer_tiles):
        tile = [row[tile_x * 8:(tile_x + 1) * 8] for row in footer]
        encoded = _encode_tile(tile)
        off = _tile_offset(FOOTER_CHR_PAGE, tile_id)
        existing = bytes(rom[off:off + 16])
        if existing not in (bytes(16), encoded):
            raise ValueError(f"footer CHR tile 0x{tile_id:02X} is not unused")
        rom[off:off + 16] = encoded
        tiles_written += 1

    if mark_te:
        for page in TITLE_CHR_PAGES:
            off = _tile_offset(page, TM_TILE_ID)
            existing = bytes(rom[off:off + 16])
            if existing not in (TM_M_HALF, TE_E_HALF):
                raise ValueError(
                    f"trademark M-half tile 0x{TM_TILE_ID:02X} on CHR page {page} "
                    f"is not the expected mark: {existing.hex()}")
            rom[off:off + 16] = TE_E_HALF
            tiles_written += 1

    routine_bytes = footer_routine(data_off, base_x)
    hook_patched = footer_hook_patched(routine_off)

    hook = bytes(rom[FOOTER_HOOK_OFFSET:FOOTER_HOOK_OFFSET + 3])
    if hook not in (FOOTER_HOOK_ORIGINAL, hook_patched):
        raise ValueError(f"unexpected title hook at 0x{FOOTER_HOOK_OFFSET:04X}")

    # A dead run is filler (any mix of 0x00/0xFF) or our own bytes from a re-run.
    existing_routine = bytes(rom[routine_off:routine_off + len(routine_bytes)])
    if existing_routine != routine_bytes and set(existing_routine) - {0x00, 0xFF}:
        raise ValueError(f"title footer routine space at 0x{routine_off:04X} is not unused")

    existing_data = bytes(rom[data_off:data_off + len(metasprite)])
    if existing_data != metasprite and set(existing_data) - {0x00, 0xFF}:
        raise ValueError(f"title footer metasprite space at 0x{data_off:04X} is not unused")

    rom[FOOTER_HOOK_OFFSET:FOOTER_HOOK_OFFSET + 3] = hook_patched
    rom[routine_off:routine_off + len(routine_bytes)] = routine_bytes
    rom[data_off:data_off + len(metasprite)] = metasprite
    return tiles_written

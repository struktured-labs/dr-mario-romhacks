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


def apply_training_edition_title(rom):
    """Patch a standard 64 KiB Dr. Mario ROM image in place.

    Returns the number of CHR tiles written.  The routine verifies but does not
    change the original title-screen tilemap, keeping the attract demo safe.
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
    return tiles_written

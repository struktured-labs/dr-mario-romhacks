#!/usr/bin/env python3
"""
MINIMAL Dr. Mario VS CPU patch - toggle only.
Used to debug P2 level select issue.
"""

INPUT_ROM = "drmario.nes"
OUTPUT_ROM = "drmario_minimal.nes"

def apply_patches(input_path, output_path):
    with open(input_path, 'rb') as f:
        rom_data = bytearray(f.read())

    # Toggle routine: Cycles 1P -> 2P -> VS CPU -> 1P
    toggle_routine = bytes([
        0xAD, 0x27, 0x07,     # 00: LDA $0727
        0xC9, 0x01,           # 03: CMP #$01
        0xF0, 0x0E,           # 05: BEQ was_1p
        0xA5, 0x05,           # 07: LDA $05
        0xD0, 0x03,           # 09: BNE was_vs_cpu
        0xE6, 0x05,           # 0B: INC $05
        0x60,                 # 0D: RTS
        0xA9, 0x01,           # 0E: was_vs_cpu: LDA #$01
        0x8D, 0x27, 0x07,     # 10: STA $0727
        0xD0, 0x03,           # 13: BNE clear_flag
        0xEE, 0x27, 0x07,     # 15: was_1p: INC $0727
        0xA9, 0x00,           # 18: clear_flag: LDA #$00
        0x85, 0x05,           # 1A: STA $05
        0x60,                 # 1C: RTS
    ])

    # Install at 0x7F50 -> CPU $FF40 (before the JMPs at 0x7FE0)
    toggle_offset = 0x7F50
    toggle_cpu = 0x8000 + (toggle_offset - 0x10)
    rom_data[toggle_offset:toggle_offset + len(toggle_routine)] = toggle_routine
    print(f"Toggle routine at 0x{toggle_offset:04X} -> CPU ${toggle_cpu:04X}")

    # Hook at 0x18E5: JSR $FFC5
    rom_data[0x18E5] = 0x20  # JSR
    rom_data[0x18E6] = toggle_cpu & 0xFF
    rom_data[0x18E7] = (toggle_cpu >> 8) & 0xFF
    rom_data[0x18E8:0x18ED] = bytes([0xEA] * 5)  # NOPs
    print(f"Hook installed at 0x18E5: JSR ${toggle_cpu:04X}")

    with open(output_path, 'wb') as f:
        f.write(rom_data)
    print(f"Written: {output_path}")

if __name__ == "__main__":
    apply_patches(INPUT_ROM, OUTPUT_ROM)

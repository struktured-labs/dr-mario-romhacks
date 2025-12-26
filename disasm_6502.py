#!/usr/bin/env python3
"""6502 disassembler for NES ROM analysis"""

# 6502 instruction set
OPCODES = {
    0x00: ("BRK", 1, "impl"),
    0x01: ("ORA", 2, "indx"),
    0x05: ("ORA", 2, "zp"),
    0x06: ("ASL", 2, "zp"),
    0x08: ("PHP", 1, "impl"),
    0x09: ("ORA", 2, "imm"),
    0x0A: ("ASL", 1, "acc"),
    0x0D: ("ORA", 3, "abs"),
    0x0E: ("ASL", 3, "abs"),
    0x10: ("BPL", 2, "rel"),
    0x11: ("ORA", 2, "indy"),
    0x15: ("ORA", 2, "zpx"),
    0x16: ("ASL", 2, "zpx"),
    0x18: ("CLC", 1, "impl"),
    0x19: ("ORA", 3, "absy"),
    0x1D: ("ORA", 3, "absx"),
    0x1E: ("ASL", 3, "absx"),
    0x20: ("JSR", 3, "abs"),
    0x21: ("AND", 2, "indx"),
    0x24: ("BIT", 2, "zp"),
    0x25: ("AND", 2, "zp"),
    0x26: ("ROL", 2, "zp"),
    0x28: ("PLP", 1, "impl"),
    0x29: ("AND", 2, "imm"),
    0x2A: ("ROL", 1, "acc"),
    0x2C: ("BIT", 3, "abs"),
    0x2D: ("AND", 3, "abs"),
    0x2E: ("ROL", 3, "abs"),
    0x30: ("BMI", 2, "rel"),
    0x31: ("AND", 2, "indy"),
    0x35: ("AND", 2, "zpx"),
    0x36: ("ROL", 2, "zpx"),
    0x38: ("SEC", 1, "impl"),
    0x39: ("AND", 3, "absy"),
    0x3D: ("AND", 3, "absx"),
    0x3E: ("ROL", 3, "absx"),
    0x40: ("RTI", 1, "impl"),
    0x41: ("EOR", 2, "indx"),
    0x45: ("EOR", 2, "zp"),
    0x46: ("LSR", 2, "zp"),
    0x48: ("PHA", 1, "impl"),
    0x49: ("EOR", 2, "imm"),
    0x4A: ("LSR", 1, "acc"),
    0x4C: ("JMP", 3, "abs"),
    0x4D: ("EOR", 3, "abs"),
    0x4E: ("LSR", 3, "abs"),
    0x50: ("BVC", 2, "rel"),
    0x51: ("EOR", 2, "indy"),
    0x55: ("EOR", 2, "zpx"),
    0x56: ("LSR", 2, "zpx"),
    0x58: ("CLI", 1, "impl"),
    0x59: ("EOR", 3, "absy"),
    0x5D: ("EOR", 3, "absx"),
    0x5E: ("LSR", 3, "absx"),
    0x60: ("RTS", 1, "impl"),
    0x61: ("ADC", 2, "indx"),
    0x65: ("ADC", 2, "zp"),
    0x66: ("ROR", 2, "zp"),
    0x68: ("PLA", 1, "impl"),
    0x69: ("ADC", 2, "imm"),
    0x6A: ("ROR", 1, "acc"),
    0x6C: ("JMP", 3, "ind"),
    0x6D: ("ADC", 3, "abs"),
    0x6E: ("ROR", 3, "abs"),
    0x70: ("BVS", 2, "rel"),
    0x71: ("ADC", 2, "indy"),
    0x75: ("ADC", 2, "zpx"),
    0x76: ("ROR", 2, "zpx"),
    0x78: ("SEI", 1, "impl"),
    0x79: ("ADC", 3, "absy"),
    0x7D: ("ADC", 3, "absx"),
    0x7E: ("ROR", 3, "absx"),
    0x81: ("STA", 2, "indx"),
    0x84: ("STY", 2, "zp"),
    0x85: ("STA", 2, "zp"),
    0x86: ("STX", 2, "zp"),
    0x88: ("DEY", 1, "impl"),
    0x8A: ("TXA", 1, "impl"),
    0x8C: ("STY", 3, "abs"),
    0x8D: ("STA", 3, "abs"),
    0x8E: ("STX", 3, "abs"),
    0x90: ("BCC", 2, "rel"),
    0x91: ("STA", 2, "indy"),
    0x94: ("STY", 2, "zpx"),
    0x95: ("STA", 2, "zpx"),
    0x96: ("STX", 2, "zpy"),
    0x98: ("TYA", 1, "impl"),
    0x99: ("STA", 3, "absy"),
    0x9A: ("TXS", 1, "impl"),
    0x9D: ("STA", 3, "absx"),
    0xA0: ("LDY", 2, "imm"),
    0xA1: ("LDA", 2, "indx"),
    0xA2: ("LDX", 2, "imm"),
    0xA4: ("LDY", 2, "zp"),
    0xA5: ("LDA", 2, "zp"),
    0xA6: ("LDX", 2, "zp"),
    0xA8: ("TAY", 1, "impl"),
    0xA9: ("LDA", 2, "imm"),
    0xAA: ("TAX", 1, "impl"),
    0xAC: ("LDY", 3, "abs"),
    0xAD: ("LDA", 3, "abs"),
    0xAE: ("LDX", 3, "abs"),
    0xB0: ("BCS", 2, "rel"),
    0xB1: ("LDA", 2, "indy"),
    0xB4: ("LDY", 2, "zpx"),
    0xB5: ("LDA", 2, "zpx"),
    0xB6: ("LDX", 2, "zpy"),
    0xB8: ("CLV", 1, "impl"),
    0xB9: ("LDA", 3, "absy"),
    0xBA: ("TSX", 1, "impl"),
    0xBC: ("LDY", 3, "absx"),
    0xBD: ("LDA", 3, "absx"),
    0xBE: ("LDX", 3, "absy"),
    0xC0: ("CPY", 2, "imm"),
    0xC1: ("CMP", 2, "indx"),
    0xC4: ("CPY", 2, "zp"),
    0xC5: ("CMP", 2, "zp"),
    0xC6: ("DEC", 2, "zp"),
    0xC8: ("INY", 1, "impl"),
    0xC9: ("CMP", 2, "imm"),
    0xCA: ("DEX", 1, "impl"),
    0xCC: ("CPY", 3, "abs"),
    0xCD: ("CMP", 3, "abs"),
    0xCE: ("DEC", 3, "abs"),
    0xD0: ("BNE", 2, "rel"),
    0xD1: ("CMP", 2, "indy"),
    0xD5: ("CMP", 2, "zpx"),
    0xD6: ("DEC", 2, "zpx"),
    0xD8: ("CLD", 1, "impl"),
    0xD9: ("CMP", 3, "absy"),
    0xDD: ("CMP", 3, "absx"),
    0xDE: ("DEC", 3, "absx"),
    0xE0: ("CPX", 2, "imm"),
    0xE1: ("SBC", 2, "indx"),
    0xE4: ("CPX", 2, "zp"),
    0xE5: ("SBC", 2, "zp"),
    0xE6: ("INC", 2, "zp"),
    0xE8: ("INX", 1, "impl"),
    0xE9: ("SBC", 2, "imm"),
    0xEA: ("NOP", 1, "impl"),
    0xEC: ("CPX", 3, "abs"),
    0xED: ("SBC", 3, "abs"),
    0xEE: ("INC", 3, "abs"),
    0xF0: ("BEQ", 2, "rel"),
    0xF1: ("SBC", 2, "indy"),
    0xF5: ("SBC", 2, "zpx"),
    0xF6: ("INC", 2, "zpx"),
    0xF8: ("SED", 1, "impl"),
    0xF9: ("SBC", 3, "absy"),
    0xFD: ("SBC", 3, "absx"),
    0xFE: ("INC", 3, "absx"),
}

def disasm(data, start_addr, base_offset=0):
    """Disassemble 6502 code"""
    i = 0
    lines = []
    while i < len(data):
        opcode = data[i]
        if opcode not in OPCODES:
            lines.append(f"${start_addr + i:04X}: .byte ${opcode:02X}")
            i += 1
            continue

        mnemonic, size, mode = OPCODES[opcode]
        addr = start_addr + i
        rom_offset = base_offset + i

        if size == 1:
            operand = ""
            raw = f"{opcode:02X}"
        elif size == 2:
            if i + 1 >= len(data):
                break
            op1 = data[i + 1]
            raw = f"{opcode:02X} {op1:02X}"
            if mode == "imm":
                operand = f"#${op1:02X}"
            elif mode == "zp":
                operand = f"${op1:02X}"
            elif mode == "zpx":
                operand = f"${op1:02X},X"
            elif mode == "zpy":
                operand = f"${op1:02X},Y"
            elif mode == "indx":
                operand = f"(${op1:02X},X)"
            elif mode == "indy":
                operand = f"(${op1:02X}),Y"
            elif mode == "rel":
                # Relative branch
                offset = op1 if op1 < 128 else op1 - 256
                target = addr + 2 + offset
                operand = f"${target:04X}"
            else:
                operand = f"${op1:02X}"
        elif size == 3:
            if i + 2 >= len(data):
                break
            op1, op2 = data[i + 1], data[i + 2]
            raw = f"{opcode:02X} {op1:02X} {op2:02X}"
            full_addr = op1 | (op2 << 8)
            if mode == "abs":
                operand = f"${full_addr:04X}"
            elif mode == "absx":
                operand = f"${full_addr:04X},X"
            elif mode == "absy":
                operand = f"${full_addr:04X},Y"
            elif mode == "ind":
                operand = f"(${full_addr:04X})"
            else:
                operand = f"${full_addr:04X}"

        # Add annotation for known addresses
        annotation = ""
        if "2001" in operand:
            annotation = " ; PPU_MASK"
        elif "2000" in operand:
            annotation = " ; PPU_CTRL"
        elif "2002" in operand:
            annotation = " ; PPU_STATUS"
        elif "2006" in operand:
            annotation = " ; PPU_ADDR"
        elif "2007" in operand:
            annotation = " ; PPU_DATA"
        elif "4016" in operand:
            annotation = " ; JOY1"

        lines.append(f"${addr:04X} [{rom_offset:04X}]: {raw:12s} {mnemonic:4s} {operand}{annotation}")
        i += size

    return lines

# Load ROM
with open('drmario.nes', 'rb') as f:
    rom_data = bytearray(f.read())

prg_start = 16
prg_data = rom_data[prg_start:prg_start + 32768]

# Disassemble the pause-related area (around 0x17A0)
# ROM offset 0x17B9 = PRG offset 0x17A9 (subtract header)
# CPU address would be around $97A9 (second bank maps to $8000-$BFFF)

print("=== Disassembly around Start button check (ROM 0x17B0-0x1850) ===")
print("=== This area has PPU_MASK writes at 0x17CB and 0x17FE ===\n")

# PRG offset = ROM offset - 16 (header)
prg_offset = 0x17B0 - 16
cpu_addr = 0x8000 + prg_offset  # Assuming it maps to $8000

chunk = prg_data[prg_offset:prg_offset+0xA0]
lines = disasm(chunk, cpu_addr, 0x17B0)
for line in lines:
    print(line)

print("\n\n=== Disassembly around first Start check (ROM 0x1620-0x16A0) ===\n")
prg_offset = 0x1620 - 16
cpu_addr = 0x8000 + prg_offset
chunk = prg_data[prg_offset:prg_offset+0x80]
lines = disasm(chunk, cpu_addr, 0x1620)
for line in lines:
    print(line)

print("\n\n=== Initial PPU setup area (ROM 0x0100-0x0150) ===\n")
prg_offset = 0x0100 - 16
cpu_addr = 0x8000 + prg_offset
chunk = prg_data[prg_offset:prg_offset+0x50]
lines = disasm(chunk, cpu_addr, 0x0100)
for line in lines:
    print(line)

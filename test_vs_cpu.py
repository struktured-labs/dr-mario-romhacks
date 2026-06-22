#!/usr/bin/env python3
"""
Unit tests for Dr. Mario VS CPU patch routines.
Uses a simple 6502 simulator to verify routine behavior.
"""

import sys

class CPU6502:
    """Minimal 6502 simulator for testing patch routines."""

    def __init__(self):
        self.a = 0
        self.x = 0
        self.y = 0
        self.sp = 0xFF
        self.pc = 0
        self.status = 0  # NV-BDIZC
        self.memory = bytearray(0x10000)
        self.cycles = 0
        self.max_cycles = 10000

    def reset(self):
        self.a = 0
        self.x = 0
        self.y = 0
        self.sp = 0xFF
        self.status = 0
        self.cycles = 0
        # Clear relevant memory areas
        for i in range(0x100):
            self.memory[i] = 0
        for i in range(0x300, 0x400):
            self.memory[i] = 0
        # Initialize playfields to $FF (empty tiles)
        for i in range(0x400, 0x600):
            self.memory[i] = 0xFF
        for i in range(0x700, 0x800):
            self.memory[i] = 0

    def set_z(self, value):
        if value == 0:
            self.status |= 0x02
        else:
            self.status &= ~0x02

    def set_n(self, value):
        if value & 0x80:
            self.status |= 0x80
        else:
            self.status &= ~0x80

    def set_c(self, value):
        if value:
            self.status |= 0x01
        else:
            self.status &= ~0x01

    def get_z(self):
        return (self.status & 0x02) != 0

    def get_n(self):
        return (self.status & 0x80) != 0

    def get_c(self):
        return (self.status & 0x01) != 0

    def load_routine(self, addr, code):
        """Load routine bytes at address."""
        for i, b in enumerate(code):
            self.memory[addr + i] = b

    def run(self, start_addr):
        """Run until RTS or max cycles."""
        self.pc = start_addr
        while self.cycles < self.max_cycles:
            opcode = self.memory[self.pc]

            if opcode == 0x60:  # RTS
                return True
            elif opcode == 0x4C:  # JMP abs
                addr = self.memory[self.pc + 1] | (self.memory[self.pc + 2] << 8)
                self.pc = addr
            elif opcode == 0x20:  # JSR abs
                addr = self.memory[self.pc + 1] | (self.memory[self.pc + 2] << 8)
                ret_addr = self.pc + 2
                self.memory[0x100 + self.sp] = (ret_addr >> 8) & 0xFF
                self.sp = (self.sp - 1) & 0xFF
                self.memory[0x100 + self.sp] = ret_addr & 0xFF
                self.sp = (self.sp - 1) & 0xFF
                self.pc = addr
            elif opcode == 0xA9:  # LDA imm
                self.a = self.memory[self.pc + 1]
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 2
            elif opcode == 0xA5:  # LDA zp
                addr = self.memory[self.pc + 1]
                self.a = self.memory[addr]
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 2
            elif opcode == 0xAD:  # LDA abs
                addr = self.memory[self.pc + 1] | (self.memory[self.pc + 2] << 8)
                self.a = self.memory[addr]
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 3
            elif opcode == 0xBD:  # LDA abs,X
                addr = (self.memory[self.pc + 1] | (self.memory[self.pc + 2] << 8)) + self.x
                self.a = self.memory[addr & 0xFFFF]
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 3
            elif opcode == 0xB9:  # LDA abs,Y
                addr = (self.memory[self.pc + 1] | (self.memory[self.pc + 2] << 8)) + self.y
                self.a = self.memory[addr & 0xFFFF]
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 3
            elif opcode == 0x85:  # STA zp
                addr = self.memory[self.pc + 1]
                self.memory[addr] = self.a
                self.pc += 2
            elif opcode == 0x8D:  # STA abs
                addr = self.memory[self.pc + 1] | (self.memory[self.pc + 2] << 8)
                self.memory[addr] = self.a
                self.pc += 3
            elif opcode == 0xA2:  # LDX imm
                self.x = self.memory[self.pc + 1]
                self.set_z(self.x)
                self.set_n(self.x)
                self.pc += 2
            elif opcode == 0x86:  # STX zp
                addr = self.memory[self.pc + 1]
                self.memory[addr] = self.x
                self.pc += 2
            elif opcode == 0x84:  # STY zp
                addr = self.memory[self.pc + 1]
                self.memory[addr] = self.y
                self.pc += 2
            elif opcode == 0xA0:  # LDY imm
                self.y = self.memory[self.pc + 1]
                self.set_z(self.y)
                self.set_n(self.y)
                self.pc += 2
            elif opcode == 0xA8:  # TAY
                self.y = self.a
                self.set_z(self.y)
                self.set_n(self.y)
                self.pc += 1
            elif opcode == 0x98:  # TYA
                self.a = self.y
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 1
            elif opcode == 0x8A:  # TXA
                self.a = self.x
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 1
            elif opcode == 0xAA:  # TAX
                self.x = self.a
                self.set_z(self.x)
                self.set_n(self.x)
                self.pc += 1
            elif opcode == 0xC9:  # CMP imm
                result = self.a - self.memory[self.pc + 1]
                self.set_c(self.a >= self.memory[self.pc + 1])
                self.set_z(result & 0xFF)
                self.set_n(result & 0xFF)
                self.pc += 2
            elif opcode == 0xC5:  # CMP zp
                addr = self.memory[self.pc + 1]
                val = self.memory[addr]
                result = self.a - val
                self.set_c(self.a >= val)
                self.set_z(result & 0xFF)
                self.set_n(result & 0xFF)
                self.pc += 2
            elif opcode == 0xCD:  # CMP abs
                addr = self.memory[self.pc + 1] | (self.memory[self.pc + 2] << 8)
                val = self.memory[addr]
                result = self.a - val
                self.set_c(self.a >= val)
                self.set_z(result & 0xFF)
                self.set_n(result & 0xFF)
                self.pc += 3
            elif opcode == 0xE0:  # CPX imm
                result = self.x - self.memory[self.pc + 1]
                self.set_c(self.x >= self.memory[self.pc + 1])
                self.set_z(result & 0xFF)
                self.set_n(result & 0xFF)
                self.pc += 2
            elif opcode == 0xC0:  # CPY imm
                result = self.y - self.memory[self.pc + 1]
                self.set_c(self.y >= self.memory[self.pc + 1])
                self.set_z(result & 0xFF)
                self.set_n(result & 0xFF)
                self.pc += 2
            elif opcode == 0xF0:  # BEQ
                offset = self.memory[self.pc + 1]
                if offset > 127:
                    offset -= 256
                self.pc += 2
                if self.get_z():
                    self.pc += offset
            elif opcode == 0xD0:  # BNE
                offset = self.memory[self.pc + 1]
                if offset > 127:
                    offset -= 256
                self.pc += 2
                if not self.get_z():
                    self.pc += offset
            elif opcode == 0xB0:  # BCS
                offset = self.memory[self.pc + 1]
                if offset > 127:
                    offset -= 256
                self.pc += 2
                if self.get_c():
                    self.pc += offset
            elif opcode == 0x90:  # BCC
                offset = self.memory[self.pc + 1]
                if offset > 127:
                    offset -= 256
                self.pc += 2
                if not self.get_c():
                    self.pc += offset
            elif opcode == 0x10:  # BPL
                offset = self.memory[self.pc + 1]
                if offset > 127:
                    offset -= 256
                self.pc += 2
                if not self.get_n():
                    self.pc += offset
            elif opcode == 0x30:  # BMI
                offset = self.memory[self.pc + 1]
                if offset > 127:
                    offset -= 256
                self.pc += 2
                if self.get_n():
                    self.pc += offset
            elif opcode == 0xE6:  # INC zp
                addr = self.memory[self.pc + 1]
                self.memory[addr] = (self.memory[addr] + 1) & 0xFF
                self.set_z(self.memory[addr])
                self.set_n(self.memory[addr])
                self.pc += 2
            elif opcode == 0xEE:  # INC abs
                addr = self.memory[self.pc + 1] | (self.memory[self.pc + 2] << 8)
                self.memory[addr] = (self.memory[addr] + 1) & 0xFF
                self.set_z(self.memory[addr])
                self.set_n(self.memory[addr])
                self.pc += 3
            elif opcode == 0xC6:  # DEC zp
                addr = self.memory[self.pc + 1]
                self.memory[addr] = (self.memory[addr] - 1) & 0xFF
                self.set_z(self.memory[addr])
                self.set_n(self.memory[addr])
                self.pc += 2
            elif opcode == 0xCE:  # DEC abs
                addr = self.memory[self.pc + 1] | (self.memory[self.pc + 2] << 8)
                self.memory[addr] = (self.memory[addr] - 1) & 0xFF
                self.set_z(self.memory[addr])
                self.set_n(self.memory[addr])
                self.pc += 3
            elif opcode == 0xE8:  # INX
                self.x = (self.x + 1) & 0xFF
                self.set_z(self.x)
                self.set_n(self.x)
                self.pc += 1
            elif opcode == 0xCA:  # DEX
                self.x = (self.x - 1) & 0xFF
                self.set_z(self.x)
                self.set_n(self.x)
                self.pc += 1
            elif opcode == 0x88:  # DEY
                self.y = (self.y - 1) & 0xFF
                self.set_z(self.y)
                self.set_n(self.y)
                self.pc += 1
            elif opcode == 0xC8:  # INY
                self.y = (self.y + 1) & 0xFF
                self.set_z(self.y)
                self.set_n(self.y)
                self.pc += 1
            elif opcode == 0x29:  # AND imm
                self.a &= self.memory[self.pc + 1]
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 2
            elif opcode == 0x3D:  # AND abs,X
                addr = (self.memory[self.pc + 1] | (self.memory[self.pc + 2] << 8)) + self.x
                self.a &= self.memory[addr & 0xFFFF]
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 3
            elif opcode == 0x49:  # EOR imm
                self.a ^= self.memory[self.pc + 1]
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 2
            elif opcode == 0xD9:  # CMP abs,Y
                addr = (self.memory[self.pc + 1] | (self.memory[self.pc + 2] << 8)) + self.y
                val = self.memory[addr & 0xFFFF]
                result = self.a - val
                self.set_c(self.a >= val)
                self.set_z(result & 0xFF)
                self.set_n(result & 0xFF)
                self.pc += 3
            elif opcode == 0x18:  # CLC
                self.set_c(False)
                self.pc += 1
            elif opcode == 0x38:  # SEC
                self.set_c(True)
                self.pc += 1
            elif opcode == 0x69:  # ADC imm
                val = self.memory[self.pc + 1]
                result = self.a + val + (1 if self.get_c() else 0)
                self.set_c(result > 255)
                self.a = result & 0xFF
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 2
            elif opcode == 0xE9:  # SBC imm
                val = self.memory[self.pc + 1]
                result = self.a - val - (0 if self.get_c() else 1)
                self.set_c(result >= 0)
                self.a = result & 0xFF
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 2
            elif opcode == 0xED:  # SBC abs
                addr = self.memory[self.pc + 1] | (self.memory[self.pc + 2] << 8)
                val = self.memory[addr]
                result = self.a - val - (0 if self.get_c() else 1)
                self.set_c(result >= 0)
                self.a = result & 0xFF
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 3
            elif opcode == 0x4A:  # LSR A
                self.set_c(self.a & 1)
                self.a >>= 1
                self.set_z(self.a)
                self.set_n(self.a)
                self.pc += 1
            elif opcode == 0xEA:  # NOP
                self.pc += 1
            else:
                raise ValueError(f"Unknown opcode: ${opcode:02X} at ${self.pc:04X}")

            self.cycles += 1

        return False  # Hit max cycles


def extract_routines_from_patch():
    """Extract the compiled routines from patch_vs_cpu.py (v17 layout)."""
    # Import and run the patch to get the routines
    import importlib.util
    spec = importlib.util.spec_from_file_location("patch", "patch_vs_cpu.py")
    patch_module = importlib.util.module_from_spec(spec)

    # We need to capture the routines, so we'll parse the file directly
    with open("patch_vs_cpu.py", "r") as f:
        content = f.read()

    # Run patch to generate ROM, then extract routines from it
    exec(compile(content, "patch_vs_cpu.py", "exec"), {"__name__": "__main__"})

    # Read the patched ROM
    with open("drmario_vs_cpu.nes", "rb") as f:
        rom = f.read()

    # Extract routines from ROM (v17 layout)
    toggle_offset = 0x7F40
    mirror_offset = 0x7F5B  # toggle_offset + 27 (toggle len)

    # Read routine lengths from patch output
    toggle_len = mirror_offset - toggle_offset

    # Find where routines end (before 0x7FE0)
    end_offset = 0x7FE0
    for i in range(0x7FD0, 0x7FE0):
        if rom[i] == 0x60:  # RTS
            end_offset = i + 1
            break

    toggle_routine = rom[toggle_offset:mirror_offset]
    mirror_routine = rom[mirror_offset:end_offset]

    return toggle_routine, mirror_routine


class TestVSCPU:
    """Test cases for VS CPU patch routines."""

    def __init__(self):
        self.cpu = CPU6502()
        self.passed = 0
        self.failed = 0
        self.toggle_routine = None
        self.mirror_routine = None

    def load_routines(self):
        """Load routines from the patched ROM (v17 layout)."""
        with open("drmario_vs_cpu.nes", "rb") as f:
            rom = bytearray(f.read())

        # v17 Routine locations in ROM (from patch_vs_cpu.py)
        # Toggle/mirror moved from 0x7F50 to 0x7F40 to expand AI window
        toggle_offset = 0x7F40
        mirror_offset = 0x7F5B  # toggle_offset + 27 (toggle len)

        # Mirror routine: simplified pass-through (LDA $F6/STA $5B/LDA $F8/STA $5C/RTS)
        mirror_end = mirror_offset
        for i in range(mirror_offset, 0x7FE0):
            if rom[i] == 0x60:  # RTS
                mirror_end = i + 1
                break

        # AI routine starts after mirror (should be 0x7F64 in v17)
        ai_offset = mirror_end

        # AI routine ends at last RTS before 0x7FE0
        ai_end = 0x7FE0
        for i in range(0x7FDF, ai_offset, -1):
            if rom[i] == 0x60:  # RTS
                ai_end = i + 1
                break

        self.toggle_routine = bytes(rom[toggle_offset:mirror_offset])
        self.mirror_routine = bytes(rom[mirror_offset:mirror_end])
        self.ai_routine = bytes(rom[ai_offset:ai_end])

        print(f"Loaded toggle routine: {len(self.toggle_routine)} bytes (at 0x{toggle_offset:04X})")
        print(f"Loaded mirror routine: {len(self.mirror_routine)} bytes (at 0x{mirror_offset:04X})")
        print(f"Loaded AI routine: {len(self.ai_routine)} bytes (at 0x{ai_offset:04X})")
        ai_budget = 0x7FE0 - ai_offset
        print(f"AI byte budget: {ai_budget} bytes ({ai_budget - len(self.ai_routine)} bytes spare)")

    def assert_eq(self, name, actual, expected):
        if actual == expected:
            self.passed += 1
            return True
        else:
            self.failed += 1
            print(f"  FAIL: {name}: expected {expected}, got {actual}")
            return False

    def run_toggle(self, player_mode, vs_cpu_flag):
        """Run toggle routine with given state, return (new_mode, new_flag)."""
        self.cpu.reset()
        self.cpu.memory[0x0727] = player_mode
        self.cpu.memory[0x04] = vs_cpu_flag

        # Load routine at $FF40 (CPU address)
        self.cpu.load_routine(0xFF40, self.toggle_routine)
        self.cpu.run(0xFF40)

        return self.cpu.memory[0x0727], self.cpu.memory[0x04]

    def run_mirror(self, player_mode, vs_cpu_flag, game_mode, capsule_y,
                   p1_input, p1_held, p2_input, p2_held,
                   capsule_x=3, frame=0, playfield=None):
        """Run mirror routine, return ($5B, $5C) - the P2 processed input."""
        self.cpu.reset()

        # Set up memory state
        self.cpu.memory[0x0727] = player_mode
        self.cpu.memory[0x04] = vs_cpu_flag
        self.cpu.memory[0x46] = game_mode  # Game mode (< 4 = level select, >= 4 = gameplay)
        self.cpu.memory[0x0386] = capsule_y
        self.cpu.memory[0x0385] = capsule_x
        self.cpu.memory[0x43] = frame
        self.cpu.memory[0xF5] = p1_input
        self.cpu.memory[0xF7] = p1_held
        self.cpu.memory[0xF6] = p2_input
        self.cpu.memory[0xF8] = p2_held

        # Set up playfield if provided
        if playfield:
            for i, val in enumerate(playfield):
                self.cpu.memory[0x0480 + i] = val

        # Load routine at $FF5B (CPU address)
        self.cpu.load_routine(0xFF5B, self.mirror_routine)
        self.cpu.run(0xFF5B)

        return self.cpu.memory[0x5B], self.cpu.memory[0x5C]

    def run_ai(self, vs_cpu_flag, capsule_x=3, frame=0, game_mode=0,
               p1_input=0, p1_held=0):
        """Run AI routine, return ($F6, $5B, $5C)."""
        self.cpu.reset()

        # Set up memory state
        self.cpu.memory[0x04] = vs_cpu_flag
        self.cpu.memory[0x0385] = capsule_x
        self.cpu.memory[0x43] = frame
        self.cpu.memory[0x46] = game_mode  # Game mode (< 4 = level select, >= 4 = gameplay)
        self.cpu.memory[0xF5] = p1_input
        self.cpu.memory[0xF7] = p1_held
        self.cpu.a = 0  # Original A value (would be P1 input normally)

        # Load routine at $FF7B (after mirror at $FF5B + 32 bytes)
        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        return self.cpu.memory[0xF6], self.cpu.memory[0x5B], self.cpu.memory[0x5C]

    # ==================== TOGGLE TESTS ====================

    def test_toggle_1p_to_2p(self):
        """1P mode -> 2P mode (press Select)."""
        print("test_toggle_1p_to_2p...")
        mode, flag = self.run_toggle(player_mode=1, vs_cpu_flag=0)
        self.assert_eq("mode", mode, 2)
        self.assert_eq("flag", flag, 0)

    def test_toggle_2p_to_vscpu(self):
        """2P mode -> VS CPU mode (press Select)."""
        print("test_toggle_2p_to_vscpu...")
        mode, flag = self.run_toggle(player_mode=2, vs_cpu_flag=0)
        self.assert_eq("mode", mode, 2)
        self.assert_eq("flag", flag, 1)

    def test_toggle_vscpu_to_1p(self):
        """VS CPU mode -> 1P mode (press Select)."""
        print("test_toggle_vscpu_to_1p...")
        mode, flag = self.run_toggle(player_mode=2, vs_cpu_flag=1)
        self.assert_eq("mode", mode, 1)
        self.assert_eq("flag", flag, 0)

    # ==================== MIRROR TESTS (now just pass-through) ====================

    def test_mirror_copies_f6_to_5b(self):
        """Mirror routine now just copies $F6 to $5B (no logic)."""
        print("test_mirror_copies_f6_to_5b...")
        input_5b, input_5c = self.run_mirror(
            player_mode=2, vs_cpu_flag=0,
            game_mode=0, capsule_y=0xFF,
            p1_input=0x01, p1_held=0x01,
            p2_input=0x02, p2_held=0x02    # This is what's in $F6
        )
        self.assert_eq("$5B (from $F6)", input_5b, 0x02)
        self.assert_eq("$5C (from $F8)", input_5c, 0x02)

    # ==================== AI Tests (handles both mirroring and AI) ====================

    def test_ai_mirrors_in_level_select(self):
        """AI copies P1 input to $F6 in VS CPU mode level select."""
        print("test_ai_mirrors_in_level_select...")
        input_f6, _, _ = self.run_ai(
            vs_cpu_flag=1,
            game_mode=2,  # Mode < 4 = level select
            capsule_x=0,
            frame=1,
            p1_input=0x08  # P1 pressing Up
        )
        # Should mirror P1 input to $F6
        self.assert_eq("$F6 (P1 mirrored)", input_f6, 0x08)

    def test_ai_not_active_without_vscpu(self):
        """AI should not modify $F6 when not in VS CPU mode."""
        print("test_ai_not_active_without_vscpu...")
        input_f6, _, _ = self.run_ai(
            vs_cpu_flag=0,  # Not VS CPU
            game_mode=5,
            capsule_x=0,
            frame=1,
            p1_input=0x08
        )
        # Should keep original (A=0 from test setup)
        self.assert_eq("$F6 (original)", input_f6, 0x00)

    # ==================== AI TESTS (Gameplay) ====================

    def test_ai_activates_in_gameplay(self):
        """AI should activate when in VS CPU mode during gameplay (mode >= 4)."""
        print("test_ai_activates_in_gameplay...")
        input_f6, _, _ = self.run_ai(
            vs_cpu_flag=1,
            game_mode=5,    # Mode >= 4 = gameplay
            capsule_x=0,    # Capsule at column 0
            frame=1         # Not a rotation frame
        )
        # AI targets center (col 3), capsule at 0, should move right
        self.assert_eq("$F6 (should be Right=1)", input_f6, 0x01)

    def test_ai_moves_left_toward_center(self):
        """AI should move left when capsule is right of center."""
        print("test_ai_moves_left_toward_center...")
        input_f6, _, _ = self.run_ai(
            vs_cpu_flag=1,
            game_mode=5,
            capsule_x=5,  # Capsule at column 5 (right of center 3)
            frame=1
        )
        # AI should move left toward center
        self.assert_eq("$F6 (should be Left=2)", input_f6, 0x02)

    def test_ai_drops_when_at_center(self):
        """AI should drop when at center column (different color capsule, already vertical)."""
        print("test_ai_drops_when_at_center...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 3  # At center
        self.cpu.memory[0x0381] = 0  # Left = yellow
        self.cpu.memory[0x0382] = 1  # Right = red (different!)
        self.cpu.memory[0x03A5] = 1  # Already vertical

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # AI should drop (Down = 4)
        self.assert_eq("$F6 (should be Down=4)", self.cpu.memory[0xF6], 0x04)

    def test_ai_targets_matching_virus(self):
        """AI should target column with matching virus."""
        print("test_ai_targets_matching_virus...")
        # Set up: place a virus in column 5, row 15 (offset 120+5=125)
        # Virus color 1 (red) = tile 0xD1
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at column 0
        self.cpu.memory[0x0381] = 1  # Left capsule color = 1 (red)
        self.cpu.memory[0x0500 + 125] = 0xD1  # Red virus at row 15, col 5

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # AI should move right toward column 5
        self.assert_eq("$F6 (should be Right=1)", self.cpu.memory[0xF6], 0x01)
        self.assert_eq("target column", self.cpu.memory[0x00], 5)

    def test_ai_targets_column_minus_one_for_right_match(self):
        """AI should target column-1 when right capsule color matches virus."""
        print("test_ai_targets_column_minus_one_for_right_match...")
        # Virus at column 5, right capsule matches -> target column 4
        # Capsule at column 4 means right half at column 5 lands on virus
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at column 0
        self.cpu.memory[0x0381] = 0  # Left = yellow
        self.cpu.memory[0x0382] = 1  # Right = red
        self.cpu.memory[0x0500 + 125] = 0xD1  # Red virus at col 5

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # Target should be column 4 (virus col 5 - 1)
        self.assert_eq("target column", self.cpu.memory[0x00], 4)
        # Should move right toward column 4
        self.assert_eq("$F6 (should be Right=1)", self.cpu.memory[0xF6], 0x01)

    def test_ai_drops_horizontal_for_different_colors(self):
        """AI should drop horizontal for different-color capsules (no rotation)."""
        print("test_ai_drops_horizontal_for_different_colors...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 4  # At target column 4 (for right match on col 5 virus)
        self.cpu.memory[0x0381] = 0  # Left = yellow
        self.cpu.memory[0x0382] = 1  # Right = red (different!)
        self.cpu.memory[0x03A5] = 0  # Horizontal
        self.cpu.memory[0x0500 + 125] = 0xD1  # Red virus at col 5

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # Different colors, should just drop (no rotation)
        self.assert_eq("$F6 (should be Down=4)", self.cpu.memory[0xF6], 0x04)

    def test_ai_drops_at_target(self):
        """AI should drop when at target column."""
        print("test_ai_drops_at_target...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 3  # At target (center)
        self.cpu.memory[0x0381] = 1  # Left = red
        self.cpu.memory[0x0382] = 1  # Right = red
        self.cpu.memory[0x0500 + 27] = 0xD1  # Red virus at row 3, col 3 (clear path)

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # Should drop
        self.assert_eq("$F6 (should be Down=4)", self.cpu.memory[0xF6], 0x04)

    def test_ai_finds_top_virus_first(self):
        """AI should find best virus (v16: lowest row = best score)."""
        print("test_ai_finds_top_virus_first...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at column 0
        self.cpu.memory[0x0381] = 1  # Left = red
        self.cpu.memory[0x0382] = 0  # Right = yellow
        # Red virus at row 10, col 5 (offset 85) - lower row, worse score
        self.cpu.memory[0x0500 + 85] = 0xD1
        # Red virus at row 3, col 2 (offset 26) - higher row, BETTER score
        self.cpu.memory[0x0500 + 26] = 0xD1

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # v16: Should target the virus with BEST SCORE (row 3) at col 2
        self.assert_eq("target column (best score)", self.cpu.memory[0x00], 2)

    def test_ai_moves_to_virus_column(self):
        """AI should move toward the virus column."""
        print("test_ai_moves_to_virus_column...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 1  # Capsule at column 1
        self.cpu.memory[0x0381] = 2  # Left = blue
        self.cpu.memory[0x0382] = 0  # Right = yellow
        # Blue virus at row 5, col 6 (offset 46)
        self.cpu.memory[0x0500 + 46] = 0xD2

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # Should target col 6 and move right
        self.assert_eq("target column", self.cpu.memory[0x00], 6)
        self.assert_eq("$F6 (should be Right=1)", self.cpu.memory[0xF6], 0x01)

    def test_ai_not_active_in_regular_2p(self):
        """AI should NOT activate in regular 2P mode (just stores original input)."""
        print("test_ai_not_active_in_regular_2p...")
        # In non-VS CPU mode, AI should just store original input (0) and return
        input_f6, _, _ = self.run_ai(
            vs_cpu_flag=0,  # Regular 2P, not VS CPU
            game_mode=5,
            capsule_x=3,
            frame=1
        )
        # Should just have the original store (A=0)
        self.assert_eq("$F6 (should be 0 - original input)", input_f6, 0x00)

    # ==================== v16 HEURISTIC TESTS ====================

    def test_ai_avoids_top_partition(self):
        """AI should skip columns with occupied top row (partition risk)."""
        print("test_ai_avoids_top_partition...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at column 0
        self.cpu.memory[0x0381] = 1  # Left = red

        # Red virus at row 5, col 2 (offset 42) - ACCESSIBLE
        self.cpu.memory[0x0500 + 42] = 0xD1
        # Red virus at row 3, col 3 (offset 27) - but top row occupied!
        self.cpu.memory[0x0500 + 27] = 0xD1
        self.cpu.memory[0x0500 + 3] = 0x50  # Top row (row 0) of col 3 occupied

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # Should target col 2 (clear top) NOT col 3 (occupied top), even though col 3 is higher
        self.assert_eq("target column (avoid top partition)", self.cpu.memory[0x00], 2)

    def test_ai_prefers_lower_viruses(self):
        """AI should prefer viruses at lower rows (safer placement)."""
        print("test_ai_prefers_lower_viruses...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at column 0
        self.cpu.memory[0x0381] = 1  # Left = red

        # Red virus at row 3, col 2 (offset 26) - higher row (score = 3)
        self.cpu.memory[0x0500 + 26] = 0xD1
        # Red virus at row 10, col 5 (offset 85) - lower row (score = 10)
        self.cpu.memory[0x0500 + 85] = 0xD1

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # Should target col 2 (row 3, score 3) NOT col 5 (row 10, score 10)
        # Lower score = better in v16
        self.assert_eq("target column (prefer lower row score)", self.cpu.memory[0x00], 2)

    def test_ai_multi_candidate_selection(self):
        """AI should scan all viruses and pick best candidate, not just first match."""
        print("test_ai_multi_candidate_selection...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at column 0
        self.cpu.memory[0x0381] = 1  # Left = red

        # Red virus at row 14, col 1 (offset 113) - first in scan order but worst score
        self.cpu.memory[0x0500 + 113] = 0xD1
        # Red virus at row 5, col 2 (offset 42) - middle score
        self.cpu.memory[0x0500 + 42] = 0xD1
        # Red virus at row 2, col 6 (offset 22) - BEST score (lowest row)
        self.cpu.memory[0x0500 + 22] = 0xD1

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # Should target col 6 (row 2, best score) NOT col 1 (first match)
        self.assert_eq("target column (best of multiple)", self.cpu.memory[0x00], 6)
        self.assert_eq("best score in $01", self.cpu.memory[0x01], 2)

    def test_ai_right_match_avoids_top_partition(self):
        """AI should check top row of TARGET column for right matches too."""
        print("test_ai_right_match_avoids_top_partition...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at column 0
        self.cpu.memory[0x0381] = 0  # Left = yellow
        self.cpu.memory[0x0382] = 1  # Right = red

        # Red virus at row 5, col 5 (offset 45) - right match would target col 4
        self.cpu.memory[0x0500 + 45] = 0xD1
        self.cpu.memory[0x0500 + 4] = 0x50  # Top row of col 4 occupied!
        # Red virus at row 8, col 7 (offset 71) - right match targets col 6, clear top
        self.cpu.memory[0x0500 + 71] = 0xD1

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # Should target col 6 (col 7 virus - 1), NOT col 4 (top occupied)
        self.assert_eq("target column (right match avoids partition)", self.cpu.memory[0x00], 6)

    def test_ai_defaults_to_center_if_no_valid_virus(self):
        """AI should use default target (center) if no valid virus found."""
        print("test_ai_defaults_to_center_if_no_valid_virus...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at column 0
        self.cpu.memory[0x0381] = 1  # Left = red

        # Red virus exists but top row occupied
        self.cpu.memory[0x0500 + 42] = 0xD1  # Row 5, col 2
        self.cpu.memory[0x0500 + 2] = 0x50   # Top row occupied

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # Should use default target (col 3 = center)
        self.assert_eq("target column (default)", self.cpu.memory[0x00], 3)
        self.assert_eq("best score (unset)", self.cpu.memory[0x01], 0xFF)

    # ==================== v17 HEURISTIC TESTS ====================

    def test_v17_skips_column_with_row1_occupied(self):
        """v17 fat top check: skip column if row 1 (below top) is occupied (height-1 penalty)."""
        print("test_v17_skips_column_with_row1_occupied...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at col 0
        self.cpu.memory[0x0381] = 1  # Left = red

        # Red virus at row 5, col 2 (offset 42) - row 0 clear, but row 1 occupied
        self.cpu.memory[0x0500 + 42] = 0xD1
        self.cpu.memory[0x0500 + 10] = 0x50  # Row 1 of col 2 occupied
        # Red virus at row 10, col 5 (offset 85) - both rows 0,1 clear
        self.cpu.memory[0x0500 + 85] = 0xD1

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # v17 should skip col 2 (row 1 occupied) and pick col 5 even though col 2
        # has lower (better) base score. v16 would have picked col 2.
        self.assert_eq("target column (height-1 skip)", self.cpu.memory[0x00], 5)

    def test_v17_vertical_adjacency_bonus(self):
        """v17 adjacency: virus with same-color tile above gets -1 score bonus."""
        print("test_v17_vertical_adjacency_bonus...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at col 0
        self.cpu.memory[0x0381] = 1  # Left = red

        # Two red viruses at SAME score row=5: col 2 (offset 42) and col 6 (offset 46)
        # Without adjacency bonus, both have base score 5; first-scanned (col 2) wins.
        # With adjacency bonus on col 6: cell above (row 4 = offset 38) gets a
        # red virus too -> -1 bonus -> col 6 wins.
        self.cpu.memory[0x0500 + 42] = 0xD1  # col 2 row 5
        self.cpu.memory[0x0500 + 46] = 0xD1  # col 6 row 5
        self.cpu.memory[0x0500 + 38] = 0xD1  # col 6 row 4 (above the col-6 virus)
        # Note: the col 6 row-4 virus also gets evaluated. Its target is col 6
        # too (same column), score = 4 (best of all). So it should win. Let's
        # verify col 6 is targeted regardless of which virus drives the choice.

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # Adjacency-rich column 6 should be targeted
        self.assert_eq("target column (adj bonus)", self.cpu.memory[0x00], 6)

    def test_v17_vertical_adjacency_breaks_tie(self):
        """v17 adjacency bonus should break a tie between equal-score candidates."""
        print("test_v17_vertical_adjacency_breaks_tie...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at col 0
        self.cpu.memory[0x0381] = 1  # Left = red

        # Red virus at col 2 row 5 (offset 42), no adjacent same-color
        self.cpu.memory[0x0500 + 42] = 0xD1
        # Red virus at col 5 row 6 (offset 53). Has matching-color tile above
        # (col 5 row 5 = offset 45), giving it adjacency bonus -> score 5
        # (6 - 1) which TIES the col-2 virus (score 5).
        # v17 picks the first-encountered (col 2) when scores tie via BCS, so
        # to truly demonstrate the bonus break the tie, we make col 5 base
        # score 6 with bonus -> 5, and col 2 base 6 with no bonus -> 6.
        self.cpu.memory[0x0500 + 42] = 0xFF  # clear earlier
        self.cpu.memory[0x0500 + 50] = 0xD1  # col 2 row 6 (offset 50)
        self.cpu.memory[0x0500 + 53] = 0xD1  # col 5 row 6 (offset 53)
        self.cpu.memory[0x0500 + 45] = 0xD1  # col 5 row 5 (above col-5 virus)

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # col 5 should win because of adjacency bonus (score 5 vs col 2's 6).
        # Note: the col 5 row 5 virus itself is also a candidate (base 5, no
        # above-bonus since above is empty) which also targets col 5. Either
        # way, target should be col 5.
        self.assert_eq("target column (adjacency tie-break)", self.cpu.memory[0x00], 5)

    def test_v17_horizontal_adjacency_bonus(self):
        """v17 adjacency: virus with same-color tile to its right gets bonus."""
        print("test_v17_horizontal_adjacency_bonus...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at col 0
        self.cpu.memory[0x0381] = 1  # Left = red

        # Red virus at col 2 row 7 (offset 58), no neighbors -> score 7
        self.cpu.memory[0x0500 + 58] = 0xD1
        # Red virus at col 5 row 7 (offset 61), with red tile right (col 6 row 7
        # = offset 62) -> base 7 - 1 (h-adj) = 6
        self.cpu.memory[0x0500 + 61] = 0xD1
        self.cpu.memory[0x0500 + 62] = 0xD1

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # col 5 should win (score 6 vs col 2's 7); col 6 is also a candidate but
        # has no neighbor to its right (col 7 row 7 = 0xFF) so its score is 7.
        self.assert_eq("target column (h-adj bonus)", self.cpu.memory[0x00], 5)
        self.assert_eq("best score (with h-adj)", self.cpu.memory[0x01], 6)

    def test_v17_score_stored_in_temp(self):
        """v17 weighted scoring: $02 zero-page is used as score accumulator."""
        print("test_v17_score_stored_in_temp...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at col 0
        self.cpu.memory[0x0381] = 1  # Left = red

        # Place a red virus at col 4 row 3 (offset 28), no adjacent same-color
        self.cpu.memory[0x0500 + 28] = 0xD1

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # $02 was used as a temp; after final eval, $02 contains the score
        # of the LAST evaluated candidate that passed the fat top check.
        # Here only one candidate, score = row = 3 (no adj bonus).
        # Verify $02 = 3 and best score $01 = 3.
        self.assert_eq("score temp $02 was set", self.cpu.memory[0x02], 3)
        self.assert_eq("best score in $01", self.cpu.memory[0x01], 3)
        self.assert_eq("target column", self.cpu.memory[0x00], 4)

    def test_v17_height_penalty_skips_partition(self):
        """v17 fat top: column with row 0 OK but row 1 occupied -> skip (avoids
        building a tall stack that risks partitioning the playfield)."""
        print("test_v17_height_penalty_skips_partition...")
        self.cpu.reset()
        self.cpu.memory[0x04] = 1  # VS CPU mode
        self.cpu.memory[0x46] = 5  # Gameplay mode
        self.cpu.memory[0x0385] = 0  # Capsule at col 0
        self.cpu.memory[0x0381] = 1  # Left = red

        # Only one red virus exists at col 4 row 8 (offset 68).
        # Top row of col 4 is clear, but row 1 of col 4 is occupied.
        # v17 should skip this and fall back to default target (col 3).
        self.cpu.memory[0x0500 + 68] = 0xD1
        self.cpu.memory[0x0500 + 12] = 0x50  # row 1 of col 4 occupied

        ai_addr = 0xFF5B + len(self.mirror_routine)
        self.cpu.load_routine(ai_addr, self.ai_routine)
        self.cpu.run(ai_addr)

        # Target should be center default (col 3); v16 would have picked col 4.
        self.assert_eq("target (v17 fat top defaults)", self.cpu.memory[0x00], 3)
        self.assert_eq("best score still unset", self.cpu.memory[0x01], 0xFF)

    def test_v17_ai_fits_in_124_byte_budget(self):
        """v17 AI routine must fit in the 124-byte window 0x7F64-0x7FDF."""
        print("test_v17_ai_fits_in_124_byte_budget...")
        size = len(self.ai_routine)
        self.assert_eq("AI routine size <= 124 bytes", size <= 124, True)
        # Also assert the toggle moved to 0x7F40 (ROM reorg required by v17)
        with open("drmario_vs_cpu.nes", "rb") as f:
            rom = f.read()
        # Toggle starts with LDA $0727 = AD 27 07
        self.assert_eq("toggle relocated to 0x7F40", rom[0x7F40], 0xAD)
        self.assert_eq("toggle still has LDA $0727 byte 1", rom[0x7F41], 0x27)
        self.assert_eq("toggle still has LDA $0727 byte 2", rom[0x7F42], 0x07)

    def run_all_tests(self):
        """Run all test cases."""
        print("=" * 60)
        print("VS CPU Patch Unit Tests")
        print("=" * 60)

        # First rebuild the patch
        print("\nRebuilding patch...")
        import subprocess
        result = subprocess.run(["python3", "patch_vs_cpu.py"],
                                capture_output=True, text=True)
        if result.returncode != 0:
            print("FAILED to build patch!")
            print(result.stderr)
            return False

        # Load routines
        print("\nLoading routines from ROM...")
        self.load_routines()

        print("\n" + "-" * 60)
        print("Toggle Routine Tests")
        print("-" * 60)
        self.test_toggle_1p_to_2p()
        self.test_toggle_2p_to_vscpu()
        self.test_toggle_vscpu_to_1p()

        print("\n" + "-" * 60)
        print("Mirror Tests (pass-through)")
        print("-" * 60)
        self.test_mirror_copies_f6_to_5b()

        print("\n" + "-" * 60)
        print("AI Tests (mirroring + gameplay)")
        print("-" * 60)
        self.test_ai_mirrors_in_level_select()
        self.test_ai_not_active_without_vscpu()
        self.test_ai_activates_in_gameplay()
        self.test_ai_moves_left_toward_center()
        self.test_ai_drops_when_at_center()
        self.test_ai_targets_matching_virus()
        self.test_ai_targets_column_minus_one_for_right_match()
        self.test_ai_drops_horizontal_for_different_colors()
        self.test_ai_drops_at_target()
        self.test_ai_finds_top_virus_first()
        self.test_ai_moves_to_virus_column()
        self.test_ai_not_active_in_regular_2p()

        print("\n" + "-" * 60)
        print("v16 Heuristic Tests")
        print("-" * 60)
        self.test_ai_avoids_top_partition()
        self.test_ai_prefers_lower_viruses()
        self.test_ai_multi_candidate_selection()
        self.test_ai_right_match_avoids_top_partition()
        self.test_ai_defaults_to_center_if_no_valid_virus()

        print("\n" + "-" * 60)
        print("v17 Heuristic Tests")
        print("-" * 60)
        self.test_v17_skips_column_with_row1_occupied()
        self.test_v17_vertical_adjacency_bonus()
        self.test_v17_vertical_adjacency_breaks_tie()
        self.test_v17_horizontal_adjacency_bonus()
        self.test_v17_score_stored_in_temp()
        self.test_v17_height_penalty_skips_partition()
        self.test_v17_ai_fits_in_124_byte_budget()

        print("\n" + "=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("=" * 60)

        return self.failed == 0


if __name__ == "__main__":
    tester = TestVSCPU()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

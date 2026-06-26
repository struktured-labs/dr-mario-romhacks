#!/usr/bin/env python3
"""py65-based unit-test harness for the cartridge AI 6502 routines.

Lets us load assembled routine bytes at a CPU address, set up a Dr. Mario board
in $0500-$057F, call a subroutine, and read back memory + cycle count -- so we
can validate new routines (board-sim resolve, shape eval) cell-for-cell against a
Python golden model AND measure their cost against the vblank-NMI budget
(~2273 usable cycles/frame) WITHOUT needing Mesen.
"""
import sys
from py65.devices.mpu6502 import MPU

P2_BOARD = 0x0500           # 128 bytes, 16 rows x 8 cols, row-major
EMPTY = 0xFF
HALT = 0x9000               # sentinel return address; RTS lands here, we stop


class Cpu:
    def __init__(self):
        self.mpu = MPU()
        self.mem = self.mpu.memory          # 0x10000 list, default 0

    def load(self, cpu_addr, data):
        for i, b in enumerate(data):
            self.mem[cpu_addr + i] = b & 0xFF

    def set_board(self, board):
        """board: 128 ints (tile bytes)."""
        assert len(board) == 128
        for i, b in enumerate(board):
            self.mem[P2_BOARD + i] = b & 0xFF

    def get_board(self):
        return [self.mem[P2_BOARD + i] for i in range(128)]

    def zp(self, addr):
        return self.mem[addr & 0xFF]

    def set_zp(self, addr, val):
        self.mem[addr & 0xFF] = val & 0xFF

    def call(self, addr, max_steps=200000):
        """Execute a subroutine at CPU `addr` until its RTS returns to HALT.
        Returns cycle count. Raises if it runs away."""
        m = self.mpu
        # Push HALT-1 as the return address (RTS adds 1).
        ret = HALT - 1
        m.sp = 0xFD
        self.mem[0x0100 + 0xFE] = (ret >> 8) & 0xFF   # hi
        self.mem[0x0100 + 0xFF] = ret & 0xFF          # lo  (stack grows down; SP=FD)
        # Standard layout: after JSR, stack has [.. lo, hi] with SP below. We set
        # SP=0xFD so the first RTS pulls from 0x01FE(lo? ) -- match 6502 order:
        # RTS pulls lo then hi from SP+1, SP+2. So put lo at 0x01FE, hi at 0x01FF.
        self.mem[0x01FE] = ret & 0xFF
        self.mem[0x01FF] = (ret >> 8) & 0xFF
        m.pc = addr
        c0 = m.processorCycles
        for _ in range(max_steps):
            m.step()
            if m.pc == HALT:
                return m.processorCycles - c0
        raise RuntimeError(f"routine at ${addr:04X} did not return in {max_steps} steps")

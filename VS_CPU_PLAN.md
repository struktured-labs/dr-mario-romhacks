# Dr. Mario VS CPU Mode - Implementation Plan

## Overview
Convert 2-PLAYER mode into VS CPU mode where Player 2 is controlled by AI.

## Current Status (2025-12-27)

**WORKING**:
- [x] Hook injection at ROM 0x37CF (JMP $FF40)
- [x] P2 capsule movement: Left (0x02), Right (0x01)
- [x] P2 capsule rotation: A (0x40), B (0x80)
- [x] Frame-throttled AI (every 4 frames)
- [x] Random L/R + rotation AI behavior

**TODO**:
- [ ] Find Down button mapping for soft drop
- [ ] Implement smart virus-seeking AI
- [ ] Test game state memory reads ($0385 for P2 X position)

## Phase 1: Random Bot (Proof of Concept)

### Memory Layout Discovered
- **$F5**: Player 1 controller buttons (raw)
- **$F6**: Player 2 controller buttons (raw)
- **$4016**: P1 controller port
- **$4017**: P2 controller port
- Controller read routine: $B7A3 (ROM 0x37B3)

### Dr. Mario Button Format (NON-STANDARD!)

**IMPORTANT BREAKTHROUGH**: Dr. Mario uses a NON-STANDARD button mapping that differs
from typical NES games. This was discovered through systematic bit testing.

```
Standard NES:           Dr. Mario ($F6):
Bit 7: A                Bit 7: B (rotate CCW)  = 0x80
Bit 6: B                Bit 6: A (rotate CW)   = 0x40
Bit 5: Select           Bit 5: (unused/Down?)
Bit 4: Start            Bit 4: (unused/Up?)
Bit 3: Up               Bit 3: Start           = 0x08
Bit 2: Down             Bit 2: Select          = 0x04
Bit 1: Left             Bit 1: Left            = 0x02
Bit 0: Right            Bit 0: Right           = 0x01
```

**Confirmed Working Values for P2 ($F6)**:
- **Right** = 0x01 (tested: capsule moves right)
- **Left**  = 0x02 (tested: capsule moves left)
- **A (rotate CW)**  = 0x40 (tested: capsule rotates)
- **B (rotate CCW)** = 0x80 (tested: capsule rotates)

**Note**: Down button mapping still needs verification (0x04, 0x08, 0x10, 0x20 candidates).

### Free ROM Space (for AI code injection)
- 0x7F40-0x7FDF (~160 bytes available)
- Maps to CPU $FF30-$FFCF

### Implementation Steps

1. **Hook Point**: After controller read routine stores to $F6
   - Location: ROM 0x37CF (CPU $B7BF) - replaces `STA $F6; RTS` with `JMP $FF40`
   - Original bytes at 0x37CF: `85 F6 60` (STA $F6; RTS)
   - Patched bytes: `4C 40 FF` (JMP $FF40)
   - **VERIFIED WORKING** in 2-player mode

2. **AI Routine** (at $FF40 / ROM 0x7F50):

   Current implementation (random L/R + rotation):
   ```asm
   ; Complete original STA $F6 (preserve P1 input)
   STA $F6           ; 00: Store P1 input

   ; Throttle: every 4 frames
   LDA $43           ; 02: Load frame counter
   AND #$03          ; 04: Mask low 2 bits
   BNE exit          ; 06: Skip AI if not frame 0,4,8...

   ; Start with Right (0x01)
   LDA #$01          ; 08: Right button

   ; Check bit 4 for Left/Right toggle
   LDX $43           ; 0A: Load frame counter
   CPX #$10          ; 0C: Compare with 16
   BCC skip_left     ; 0E: If < 16, keep Right
   LDA #$02          ; 10: Else use Left

   ; Check bit 5 for rotation
   skip_left:
   LDX $43           ; 12: Load frame counter
   CPX #$20          ; 14: Compare with 32
   BCC store         ; 16: If < 32, skip rotation
   ORA #$40          ; 18: Add A button (rotate)

   store:
   STA $F6           ; 1A: Store AI input to P2
   exit:
   RTS               ; 1C: Return
   ```

3. **Timing**: AI makes decisions every 4 frames (throttled via `AND #$03`)
   - Prevents jittery input from being registered every frame

## Phase 2: Game State Reading

### Memory Locations Mapped (from Data Crystal)

**Playfield** (8 columns × 16 rows = 128 bytes):
- [x] **$0400-$047F**: Player 1 playfield (top-left to bottom-right)
- [x] **$0500-$057F**: Player 2 playfield (**$100 offset, NOT $80!**)

**Falling Capsule (P1)**:
- [x] **$0301**: Left half color (00=Yellow, 01=Red, 02=Blue)
- [x] **$0302**: Right half color
- [x] **$0305**: X position (0-7 columns)
- [x] **$0306**: Y position (0-15 rows)
- [x] **$00A5**: Rotation (0-3)
- [x] **$0312**: Frames until drop

**Falling Capsule (P2)** (inferred $80 offset):
- [x] **$0381**: Left half color
- [x] **$0382**: Right half color
- [x] **$0385**: X position
- [x] **$0386**: Y position

**Next Capsule**:
- [x] **$031A-$031B**: P1 next colors
- [x] **$039A-$039B**: P2 next colors

**Virus Count**:
- [x] **$0324**: P1 remaining viruses
- [x] **$03A4**: P2 remaining viruses

**Tile Values**:
- Empty: $FF (255)
- Viruses: $D0-$D2 (208-210, one per color)
- Pill halves: $40-$72 (64-114)
- Pellets: $80-$82 (128-130)

**Game State**:
- [x] **$0043**: Frame counter
- [x] **$0046**: Game mode
- [x] **$0727**: Player count

## Phase 3: Rule-Based Bot

### Decision Rules (Priority Order)
1. **Virus Match**: If capsule can match a virus color, prioritize that
2. **Chain Setup**: Look for opportunities to set up combos
3. **Height Management**: Avoid stacking too high
4. **Color Clustering**: Keep same colors together
5. **Avoid Blocking**: Don't cover viruses with wrong colors

### Algorithm Outline
```
1. Read current capsule colors
2. Scan playfield for viruses and pills
3. For each possible column position:
   - Calculate score based on rules
4. Choose highest-scoring position
5. Generate inputs to reach that position
```

## Phase 4: Deep RL (Future)

### Options
1. **External Training**: Train model outside NES, load weights
2. **Lookup Tables**: Pre-computed optimal moves for common states
3. **Hybrid**: Rule-based with learned weights

## Technical Challenges

1. **ROM Space**: Only ~160 bytes free - may need to compress or relocate existing code
2. **CPU Time**: AI logic must complete within frame time
3. **State Complexity**: Full playfield is 8x16 cells × 2 players = complex state
4. **Timing**: Capsule input only registers at certain frames

## File Structure
```
patch_vs_cpu.py          - Main patching script
ai_routines.asm          - 6502 assembly for AI logic (reference)
VS_CPU_PLAN.md           - This document
```

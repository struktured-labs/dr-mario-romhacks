# Dr. Mario VS CPU Mode - Implementation Plan

## Overview
Convert 2-PLAYER mode into VS CPU mode where Player 2 is controlled by AI.

## Phase 1: Random Bot (Proof of Concept)

### Memory Layout Discovered
- **$F5**: Player 1 controller buttons (raw)
- **$F6**: Player 2 controller buttons (raw)
- **$4016**: P1 controller port
- **$4017**: P2 controller port
- Controller read routine: $B7A3 (ROM 0x37B3)

### NES Button Format
```
Bit 7: Right
Bit 6: Left
Bit 5: Down
Bit 4: Up
Bit 3: Start
Bit 2: Select
Bit 1: B (rotate CCW)
Bit 0: A (rotate CW)
```

### Free ROM Space (for AI code injection)
- 0x7F40-0x7FDF (~160 bytes available)
- Maps to CPU $FF30-$FFCF

### Implementation Steps

1. **Hook Point**: After controller read routine stores to $F6
   - Location: End of $B7C7 routine (ROM 0x37D0)
   - Inject: JSR to AI routine

2. **AI Routine** (at $FF40 / ROM 0x7F50):
   ```asm
   ; Check if 2P mode (need to find mode flag)
   ; LDA $mode_flag
   ; CMP #$02  ; 2 player
   ; BNE .skip

   ; Generate pseudo-random input
   LDA $frame_counter  ; Use frame count as random seed
   EOR $F5             ; XOR with P1 input for variety
   AND #$F3            ; Mask to valid directions + A/B
   STA $F6             ; Override P2 input

   .skip:
   RTS
   ```

3. **Timing**: AI should make decisions every N frames, not every frame
   - Add frame counter check to avoid jittery input

## Phase 2: Game State Reading

### Memory Locations to Map
- [ ] Player 2 playfield grid (virus + pill positions)
- [ ] Current capsule position (X, Y)
- [ ] Current capsule colors
- [ ] Current capsule rotation state
- [ ] Next capsule preview colors
- [ ] Game mode flag (1P vs 2P)
- [ ] Frame counter

### Research Method
- Use emulator debugger to trace memory changes
- Compare memory snapshots when capsules move
- Look for grid data structure (likely 8x16 per player)

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

# Validation Tests

**IMPORTANT**: Run these tests BEFORE starting training to verify everything works!

## Quick Validation

Run all tests in one script:

```bash
python tests/test_env_validation.py
```

This validates:
1. ✅ Memory reading (game state, virus count, capsule position)
2. ✅ Controller input (does pressing RIGHT actually move capsule?)
3. ✅ State encoding (12-channel CNN observation)
4. ✅ Reward calculation (viruses cleared, height, game over)
5. ✅ Full episode (reset, step, termination)

**All tests must pass before training!**

---

## Visual Verification

See what the agent actually sees:

```bash
python tests/visualize_observation.py
```

This shows:
- Raw playfield (ASCII art with viruses as 'V')
- All 12 observation channels
- Empty/color/capsule channels
- Automated verification checks

**Use this to debug if agent behaves strangely.**

---

## Known Issues to Check

### Issue 1: Controller Not Moving Capsule

**Symptoms:**
- `test_controller_input()` fails
- Capsule position doesn't change

**Possible causes:**
1. **Game not in active gameplay**
   - Check: `state['mode'] >= 4`
   - Fix: Start game, go past level select

2. **Wrong player**
   - Check: Are you in VS CPU mode with P2 active?
   - Fix: Select "VS CPU" from main menu (press Select twice)

3. **Wrong controller address**
   - Check: We write to `P2_CONTROLLER (0x00F6)`
   - Fix: Verify this is correct address for P2 in VS CPU mode

4. **Frame timing**
   - Check: Are we reading state too soon after write?
   - Fix: Add delay or step more frames

### Issue 2: State Encoding Looks Wrong

**Symptoms:**
- `visualize_observation.py` shows all zeros
- No viruses in color channels

**Possible causes:**
1. **Playfield memory address wrong**
   - Check: We read from `0x0500-0x057F` for P2
   - Fix: Verify P2 playfield address in VS CPU mode

2. **Tile values incorrect**
   - Check: Are viruses actually `0xD0-0xD2`?
   - Fix: Use Mesen's memory viewer to verify

3. **Color extraction wrong**
   - Check: `tile_to_color()` logic in state_encoder.py
   - Fix: Verify tile→color mapping

### Issue 2: Rewards Always Negative

**Symptoms:**
- Episode reward stays around -1000
- Agent never gets positive reward

**Possible causes:**
1. **Time penalty too high**
   - Current: -0.1 per frame
   - Fix: Reduce to -0.01 if episodes are very long

2. **Not clearing viruses**
   - Check: Is agent actually moving capsules?
   - Fix: Run `test_controller_input()` first

3. **Height penalty too high**
   - Check: -0.5 per row might be too harsh
   - Fix: Reduce to -0.1 in `reward_function.py`

### Issue 2: Observation Encoding Wrong

**Symptoms:**
- All channels are zeros
- Color channels don't match viruses

**Debug:**
```bash
python tests/visualize_observation.py
```

**Check:**
- Empty channel (Ch 0): Should have ~100+ tiles at start
- Color channels (1-3): Should show viruses
- Capsule channel (4): Should mark current capsule
- Values in range [0, 1]

**Common problems:**
- Tile value constants wrong (TILE_EMPTY, TILE_VIRUS_*)
- Color extraction logic incorrect
- Playfield indexing wrong (row-major vs column-major)

### Issue 2: Rewards Always Negative

**Symptoms:**
- Episode rewards always around -1000
- No positive rewards even when clearing viruses

**Possible causes:**
1. **Time penalty too high**
   - Check: `-0.1 × 10000 steps = -1000`
   - Fix: This is expected early in training

2. **Virus clearing not detected**
   - Check: Is `prev_virus_count` updating?
   - Fix: Verify virus count reading is correct

3. **Height calculation wrong**
   - Check: Is max_height being computed correctly?
   - Fix: Verify row indexing (0 = top, 15 = bottom)

### Issue 2: Training Not Learning

**Symptoms:**
- Episode reward stays at -1000 after 50K steps
- Agent just spams same action

**Possible causes:**
1. **Reward too sparse**
   - Check: Are any positive rewards being given?
   - Fix: Add intermediate rewards (e.g., bonus for matching 2-3 colors)

2. **State encoding wrong**
   - Check: Run `visualize_observation.py`
   - Fix: Verify channels match actual game state

3. **Episode never ends**
   - Check: Are termination conditions correct?
   - Fix: Lower `max_height <= 2` threshold or add virus count check

4. **Actions don't work**
   - Check: Run `test_controller_input()`
   - Fix: Verify controller address and timing

---

## Integration Test (Old)

The original integration test:

```bash
python tests/test_mesen_integration.py
```

This is more manual (requires following on-screen instructions) but validates:
- Mesen connection
- Memory read/write
- Frame stepping

---

## Debugging Tips

### Problem: Agent takes random actions

**Check:**
```bash
python tests/visualize_observation.py
```

Look for:
- Are viruses visible in color channels?
- Is capsule position marked correctly?
- Are empty tiles actually marked as empty?

### Problem: Rewards always negative

**Check:**
- Are viruses being cleared? (watch virus count decrease)
- Is height increasing too much?
- Are we detecting game over too early?

Run:
```bash
python tests/test_env_validation.py
# Look at "TEST 4: Reward Calculation"
```

### Problem: Episode never ends

**Symptoms:**
- Episode runs for 10,000 steps
- Never terminates or truncates

**Possible causes:**
1. **Win condition not detected**
   - Check: `state['virus_count'] == 0`
   - Fix: Verify virus count address (0x03A4)

2. **Game over not detected**
   - Current check: `max_height <= 2` (very simplistic)
   - May need better game over detection

3. **Max steps too high**
   - Current: 10,000 frames (~3 minutes at 60 FPS)
   - Reduce if episodes are too long

---

## Before Training Checklist

Run through this checklist:

### Setup
- [ ] Mesen is running
- [ ] Dr. Mario ROM loaded
- [ ] Lua bridge loaded (`lua/mesen_bridge.lua`)
- [ ] Game started in VS CPU mode (P2)
- [ ] Game is in active gameplay (capsules falling)

### Validation Tests
- [ ] Run `python tests/test_env_validation.py`
- [ ] All 5 tests pass
- [ ] Run `python tests/visualize_observation.py`
- [ ] Verify observation looks correct

### Environment Test
- [ ] Run `python src/drmario_env.py`
- [ ] Verify no crashes for 100 steps
- [ ] Check rewards make sense
- [ ] Observe Mesen - does capsule move?

### Quick Training Test

Before committing to 1M timesteps, do a short test:

```bash
python scripts/train.py --timesteps 1000 --device cpu
```

This should:
- ✅ Load environment
- ✅ Start training without errors
- ✅ Print episode rewards
- ✅ Save checkpoint

If this works, scale up to full training!

---

## Troubleshooting

### "Connection refused"

**Problem**: Tests can't connect to Mesen

**Fix**:
1. Launch Mesen: `./run_mesen.sh drmario_vs_cpu.nes`
2. Load Lua script: Tools → Script Window → Load `lua/mesen_bridge.lua`
3. Start game in VS CPU mode
4. Run test again

### "Capsule not moving"

**Problem**: Controller input test fails

**Fix**:
1. Check game mode: Should be >= 4 (in gameplay, not menu)
2. Verify VS CPU mode: P2 should be active
3. Check Lua bridge output for errors
4. Try pressing buttons manually in Mesen - do they work?

### "Invalid observation shape"

**Problem**: State encoder produces wrong shape

**Fix**:
1. Run `python tests/visualize_observation.py`
2. Check raw playfield looks correct
3. Verify memory addresses in `memory_map.py`
4. Check for off-by-one errors in state encoder

### "All rewards are negative"

**Problem**: Agent never gets positive rewards

**Fix**:
1. Run `python src/reward_function.py` to test reward logic
2. Check virus count is decreasing (agent is clearing viruses)
3. Verify reward weights are correct
4. This is normal early in training - agent needs time to learn

---

## Validation Checklist

Before starting full training, verify:

- [ ] Mesen runs and loads ROM
- [ ] Lua bridge connects (port 8765)
- [ ] Game starts in VS CPU mode (P2)
- [ ] `test_env_validation.py` passes all 5 tests
- [ ] `visualize_observation.py` shows correct channels
- [ ] `python src/drmario_env.py` runs without errors
- [ ] Short training test works (`--timesteps 1000`)
- [ ] TensorBoard launches (`tensorboard --logdir logs/tensorboard`)

**Only proceed to full training if all items checked!**

---

## After Validation

If all tests pass, you're ready for full training:

```bash
# Full training (1M timesteps, 1-4 days on 3090)
python scripts/train.py --timesteps 1000000 --device cuda

# Monitor progress
tensorboard --logdir logs/tensorboard
```

Good luck! 🚀

# Quick Start: Dr. Mario Python AI

Get the Python AI running in 5 minutes!

## 1. Launch Mesen with Dr. Mario

```bash
cd /home/struktured/projects/dr-mario-mods
./run_mesen.sh drmario_vs_cpu.nes
```

## 2. Load Lua Bridge Script

In Mesen:
1. **Tools** → **Script Window**
2. Click **Load Script**
3. Navigate to: `rl-training-new/lua/mesen_bridge.lua`
4. Click **Open**

You should see in the Script Window:
```
Mesen Bridge Server started on port 8765
Waiting for connections...
Bridge initialized. Load a ROM to start.
```

## 3. Start the Game

In Mesen:
1. Press **F11** to start game (or click Play button)
2. Navigate to **2 PLAYER** mode
3. **IMPORTANT**: Select **VS CPU** mode (press Select twice from main menu)
   - This ensures the AI controls P2
4. Choose virus level and speed
5. Start game

## 4. Run the Python AI

In a terminal:
```bash
cd /home/struktured/projects/dr-mario-mods/rl-training-new
./run_ai.sh
```

Or manually:
```bash
cd rl-training-new
python3 src/python_ai.py
```

## What You Should See

**In Terminal:**
```
===========================================================
Dr. Mario Python AI Started
===========================================================
Oracle AI with full heuristics:
  - Virus clearing optimization
  - Height management
  - Column balance
  - Match potential scoring

Press Ctrl+C to stop
===========================================================

[DECISION] Frame 42
  Capsule at (3, 1), colors: L=0 R=1
  Column heights: [16, 16, 16, 14, 14, 16, 16, 16]
  Viruses remaining: 20
  Decision: column=4, rotation=0
  [MOVE] Right (3 → 4)
  [MOVE] Right (4 → 4)
  [DROP] At column 4
```

**In Mesen:**
- P2 capsules should move automatically
- AI targets viruses and manages height
- Capsules rotate and position optimally

## Troubleshooting

### "Connection refused"
- Make sure Mesen is running
- Make sure Lua script is loaded (check Script Window)
- Make sure game is started (not paused on title screen)

### "Capsule not moving"
- Verify you're in VS CPU mode (P2 should be active)
- Check that game mode >= 4 (in gameplay, not menu)
- Try restarting the game

### "Lua script error"
- Check Script Window for error messages
- Verify `socket` library is available (should be built-in)
- Try reloading the script

### AI makes weird moves
- This is the oracle! It's trying complex heuristics
- Check terminal output to see its reasoning
- May need tuning of heuristic weights

## Next Steps

Once the AI is running:

1. **Observe performance**: How many games does it win? How well does it manage height?

2. **Tune heuristics**: Edit `src/heuristics.py` to adjust scoring weights

3. **Collect data**: Run for many games to gather training data

4. **Move to Phase 2**: Train PPO agent using this AI as baseline

## Advanced Usage

### Run for N frames only
```python
python3 -c "
from src.python_ai import DrMarioAI, MesenInterface
interface = MesenInterface()
interface.connect()
ai = DrMarioAI(interface)
ai.run(max_frames=1000)  # Run for 1000 frames
interface.disconnect()
"
```

### Debug mode
Edit `python_ai.py` and add more print statements in the `get_control_input()` method.

### Record gameplay
Use Mesen's built-in recording:
- **File** → **Movies** → **Record Movie**

## Stopping the AI

Press **Ctrl+C** in the terminal running the AI.

The AI will cleanly disconnect from Mesen.

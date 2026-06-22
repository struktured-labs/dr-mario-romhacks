import sys
from pathlib import Path
sys.path.insert(0, 'src')
from mesen_interface_file import MesenInterface
import numpy as np
import time

work_dir = Path('../mesen2/bin/linux-x64/Release')
mesen = MesenInterface(work_dir=work_dir)

print("Waiting for game to start...")
if not mesen.connect(timeout=5):
    print("Failed to connect")
    sys.exit(1)

# Poll for 10 seconds
for i in range(100):
    state = mesen.get_game_state()
    mode = state['mode']
    virus_count = state['virus_count']
    
    playfield = np.array(state['playfield'], dtype=np.uint8).reshape(16, 8)
    empty = np.sum(playfield == 0xFF)
    viruses = np.sum((playfield >= 0xD0) & (playfield <= 0xD2))
    
    if i % 10 == 0:
        print(f"[{i//10}s] Mode={mode}, Viruses in count={virus_count}, in field={viruses}, empty={empty}")
    
    if mode >= 4 and viruses > 0:
        print(f"\n🎉 GAME STARTED!")
        print(f"  Mode: {mode}")
        print(f"  Virus count: {virus_count}")
        print(f"  Viruses on playfield: {viruses}")
        print(f"  Empty tiles: {empty}")
        
        print(f"\nBottom 3 rows:")
        for r in range(13, 16):
            row = playfield[r, :]
            v = np.sum((row >= 0xD0) & (row <= 0xD2))
            print(f"  Row {r}: {row} ({v} viruses)")
        
        if empty > 100:
            print("\n✓✓✓ CLEAN PLAYFIELD WITH VIRUSES!")
            print("Ready for RL training!")
        break
    
    time.sleep(0.1)

mesen.disconnect()

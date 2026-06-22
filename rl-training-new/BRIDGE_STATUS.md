# Mesen Bridge Status

**Last updated:** 2026-06-21 (handoff session)

## Canonical variant: file-based IPC

We are standardising on the **file-based** bridge:

- Lua side: `lua/mesen_bridge_file.lua`
- Python side: `src/mesen_interface_file.py`
- Mock smoke test: `tests/test_mesen_interface_mock.py`

The TCP variant (`lua/mesen_bridge.lua` + `src/mesen_interface.py`) is kept
around for reference but is **not** the supported entry point.

### Why file-based won

| Concern                                     | TCP variant                                                                                                                                                                              | File variant                                                  |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Mesen security toggles required             | "Allow I/O and OS functions" **and** "Allow network access"                                                                                                                              | Only "Allow I/O and OS functions"                             |
| Socket library availability                 | LuaSocket is compiled in (`mesen2/Lua/luasocket.c`), registered as `socket.core` only when network access is enabled (`Core/Debugger/ScriptingContext.cpp` lines 73-81)                   | n/a                                                           |
| Round-trip latency                          | Lower (microseconds in theory)                                                                                                                                                            | ~1-5 ms (file open/close on local FS, atomic rename)         |
| Failure modes inside Mesen's frame callback | `server:accept()` and `client:receive()` block the emulator main loop unless `settimeout(0)` is set just right; a typo == hung emulator                                                  | Worst case: a stale file lingers, no emulator hang             |
| Resilience to stale state                   | Connections die hard if the emulator pauses                                                                                                                                              | Works across emulator pause/resume                            |

The file-based variant is also easier to debug: you can `cat mesen_cmd.txt`
and `cat mesen_response.txt` from another shell to see exactly what is
flying back and forth.

### What was broken before

1. **Wrong memory-type enum in both Lua scripts.** They used
   `emu.memType.cpuMemory`, but Mesen2's enum is `NesMemory` (see
   `mesen2/Core/Shared/MemoryType.h`), so the Lua call resolves to `nil`
   and `emu.read(addr, nil, false)` raises "invalid memory type". This
   means **neither bridge ever serviced a READ**.
2. **Race conditions in the file-based protocol.**
   - Python wrote `mesen_cmd.txt` non-atomically; Lua could open the file
     while it was being written, producing a truncated command and an
     `ERROR Unknown command` response.
   - Python had no way to distinguish a fresh response from a stale one
     left behind by a previous run or a previous command.
3. **`STEP` did the wrong thing in the TCP variant.** It called
   `emu.breakExecution()` in a loop, which *pauses* the emulator instead
   of advancing frames. Both bridges now treat `STEP` as a cooperative
   acknowledgement; one Lua callback fires per rendered frame, so each
   command-response cycle implicitly waits one frame.
4. The file-based variant deleted the ready file on disconnect, which
   would confuse a second client trying to attach to the same Mesen
   session.

### Fixes applied

- `lua/mesen_bridge_file.lua` v3:
  - Switched all `emu.read`/`emu.write` calls to `emu.memType.nesMemory`.
  - Added a sequence-id protocol: commands are `<seq> <COMMAND ...>` and
    responses echo `<seq> <payload>`.
  - Both sides now use temp-file + `os.rename` for atomic publication.
  - Bridge wipes any leftover IPC files at startup *before* writing
    `mesen_ready.txt`, so Python never connects to a half-state.
  - Heartbeat log every 5 seconds for sanity.
- `src/mesen_interface_file.py`:
  - Mirrors the sequence-id protocol; ignores any response with the
    wrong seq.
  - Uses `os.replace` (atomic on POSIX *and* Windows) and `fsync` before
    rename so Lua sees a complete file.
  - `connect()` clears stale files first, then probes with `PING`.
  - `disconnect()` no longer deletes the ready file.
  - Returns both `mode` and `game_mode` keys in `get_game_state()` so the
    existing training code keeps working.
- `lua/mesen_bridge.lua` (TCP) got the `cpuMemory` -> `nesMemory` fix and
  a comment marking it deprecated, in case someone wants to revive it
  later.

## Mock test (no Mesen needed)

Run from the repo root:

```bash
cd /home/struktured/projects/dr-mario-mods
.venv/bin/python -m pytest rl-training-new/tests/test_mesen_interface_mock.py -v
```

Expected: 8 passed in ~2 seconds.

The test spins up a Python thread that pretends to be the Lua bridge: it
watches the temp directory for `mesen_cmd.txt`, parses the sequence id,
and responds via `mesen_response.txt`. The MesenInterface client never
knows there is no real Mesen on the other side. Coverage:

1. `connect()` + `PING`/`PONG`.
2. `READ` parses uppercase hex into byte lists.
3. `WRITE` serialises payloads with uppercase address and hex bytes.
4. `STEP` is acknowledged for both single and N-frame requests.
5. `GET_STATE` parses all seven colon-separated fields plus the 128-byte
   playfield.
6. `ERROR` responses surface as `RuntimeError`.
7. Silent bridges trigger `TimeoutError`.
8. A stale response left on disk from a prior command is discarded
   instead of being returned for the next command.

## Launching against a real Mesen (manual)

We **cannot** drive Mesen headless. The user has to do these steps once
per session.

### One-time setup in Mesen

1. Launch Mesen.
2. Open the script window: **Tools -> Script Window** (or **Debug ->
   Script Window**, depending on build).
3. Click the cog icon ("Settings") in the script window.
4. Under **Restrictions**, tick **Allow access to I/O and OS functions**.
   You do *not* need to tick "Allow network access" for the file bridge.
5. Close the settings dialog. These restrictions persist across sessions.

### Per-session launch

From a shell with the Python venv activated:

```bash
cd /home/struktured/projects/dr-mario-mods

# 1. Start Mesen with the ROM.
pixi run mesen2/bin/linux-x64/Release/Mesen drmario_vs_cpu.nes &

# 2. In the Mesen window:
#    Tools -> Script Window -> Open Script
#    Choose: rl-training-new/lua/mesen_bridge_file.lua
#    Click "Run". Watch the script log:
#       "File-based bridge loaded (v3, atomic rename + sequence ids)"
#       "Created ready file: mesen_ready.txt"

# 3. Verify connectivity from Python. The work_dir MUST be the directory
#    Mesen was launched from, because the Lua bridge opens its IPC files
#    using relative paths.
cd mesen2/bin/linux-x64/Release   # this is Mesen's CWD when launched via pixi run
ls mesen_ready.txt                # should exist
../../../../.venv/bin/python - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, "../../../../rl-training-new/src")
from mesen_interface_file import MesenInterface
iface = MesenInterface(work_dir=Path.cwd())
assert iface.connect(timeout=5), "connect failed"
print("READ 0x03A4 (virus count):", iface.read_memory(0x03A4, 1))
print("get_game_state:", {k: v for k, v in iface.get_game_state().items() if k != "playfield"})
iface.disconnect()
PY
```

Expected: a 1-byte read prints `[N]` (some virus count) and the state
dictionary prints the current mode/coords. If you see "Failed to connect
to Mesen bridge", the script either failed to create `mesen_ready.txt`
(check Mesen's script log) or you ran the Python from a different CWD.

### Troubleshooting

| Symptom                                                           | Cause                                                                                                                            | Fix                                                                                                                                                                                                              |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lua log: "attempt to index a nil value (global 'io')"             | "Allow I/O and OS functions" is unchecked.                                                                                       | Enable it in **Script Window -> Settings -> Restrictions**.                                                                                                                                                      |
| Lua log: "invalid memory type"                                    | You loaded an old copy of the script.                                                                                            | Re-load `mesen_bridge_file.lua` from this branch (it must say "v3" in the load message).                                                                                                                          |
| `connect()` times out, no `mesen_ready.txt`                        | Script silently errored before signalling ready.                                                                                 | Open the script log inside Mesen and read it. Common cause: I/O permission missing.                                                                                                                              |
| `connect()` times out, `mesen_ready.txt` exists                    | Python is looking in the wrong directory.                                                                                        | `MesenInterface(work_dir=<dir Mesen was launched from>)`. Confirm with `lsof -p $(pgrep Mesen) \| grep mesen_ready`.                                                                                              |
| Commands time out under load                                       | Mesen is paused (Esc / debugger break). The callback only runs on rendered frames, so no commands are serviced while paused.    | Press Esc to resume.                                                                                                                                                                                              |

## Known remaining issues and unverified bits

1. **End-to-end with a real ROM has NOT been confirmed in this session.**
   The mock test exercises only the Python parser and the file protocol.
   Once Mesen is running with the bridge loaded, the smoke test
   `rl-training-new/test_mesen_file.py` (also untracked) should be run
   from `mesen2/bin/linux-x64/Release` to confirm a real `GET_STATE`
   returns a sensible mode/virus count/playfield.
2. **Multi-frame STEP is a no-op.** This is fine for one-decision-per-
   frame RL but if the trainer ever needs to fast-forward N frames in
   one call, the Lua side will need a small state machine
   (counter + early-return + final response).
3. **`disconnect()` does not stop the Lua callback.** The bridge keeps
   processing frames until the script is unloaded from Mesen. Not a
   functional bug; just expected behaviour.
4. **Controller input via `write_memory($00F6, ...)`** is the same
   approach used by `patch_vs_cpu.py`. If a future Mesen build sanitises
   zero-page writes, we may need to switch to `emu.setInput` (which is
   exposed by the Lua API per `LuaApi.cpp` line 140) instead of poking
   memory directly.

## Rough latency estimate

Per-step cost on a local tmpfs/ext4:

| Operation                  | Wall clock (rough) |
| -------------------------- | ------------------ |
| Python write+rename cmd    | ~50 us             |
| Lua callback wakeup        | up to 16.6 ms (next rendered frame at 60 fps) |
| Lua read + execute + write | ~50-200 us         |
| Python poll detect + read  | up to `poll_interval` (default 1 ms) |
| **Total per env-step**     | **~17 ms** (~60 Hz, frame-rate limited) |

Mesen renders at 60 fps by default, so the bridge cannot service more
than ~60 commands per second regardless of file I/O speed. If you crank
the emulator with `Options -> Emulation Speed -> Maximum`, throughput
scales linearly until file I/O becomes the bottleneck (estimated
~500-1000 commands/s on a fast SSD; not measured).

For a PPO training loop with ~50 env-steps per real second per Mesen
instance, expect rollouts of 1 million steps to take roughly 5-6 hours
of wall clock per emulator. Parallelise with multiple Mesen processes
(each with its own `work_dir`) to scale.

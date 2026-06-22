-- Mesen Lua Bridge: File-based IPC for Python RL training
-- No socket dependency - uses files for communication
--
-- Protocol (atomic, sequence-numbered):
--   Python writes "<seq> <command>" to mesen_cmd.txt.new, then os.rename to mesen_cmd.txt
--   Lua reads command from mesen_cmd.txt, deletes it, writes
--     "<seq> <response>" to mesen_response.txt.new, then os.rename to mesen_response.txt
--   Python polls for a response whose <seq> matches its outstanding request.
--
-- Commands:
--   READ <addr> <size>        - Read <size> bytes from <addr>, returns hex string
--   WRITE <addr> <hex_data>   - Write hex bytes to <addr>
--   STEP <frames>             - Acknowledge (frames advance naturally between callbacks)
--   GET_STATE                 - Get full game state (playfield, capsule, etc.)
--   PING                      - Health check (returns PONG)
--
-- Settings required in Mesen:
--   Script -> Settings -> Script Window -> Restrictions
--     [x] Allow access to I/O and OS functions

-- File paths (relative to Mesen's CWD, which is its binary directory)
local CMD_FILE = "mesen_cmd.txt"
local CMD_FILE_TMP = "mesen_cmd.txt.new"
local RESPONSE_FILE = "mesen_response.txt"
local RESPONSE_FILE_TMP = "mesen_response.txt.new"
local READY_FILE = "mesen_ready.txt"

print("Mesen File-based Bridge starting...")
print("  Command file: " .. CMD_FILE)
print("  Response file: " .. RESPONSE_FILE)

-- Clean up any stale IPC files from a previous session.
-- This must happen BEFORE Python starts polling for the ready file,
-- otherwise Python might read a stale response.
os.remove(CMD_FILE)
os.remove(CMD_FILE_TMP)
os.remove(RESPONSE_FILE)
os.remove(RESPONSE_FILE_TMP)
os.remove(READY_FILE)

-- Helper: Convert hex string to byte table
local function hex_to_bytes(hex)
    local bytes = {}
    for i = 1, #hex, 2 do
        local byte_str = hex:sub(i, i + 1)
        table.insert(bytes, tonumber(byte_str, 16))
    end
    return bytes
end

-- Helper: Convert byte table to hex string (preallocate for speed)
local function bytes_to_hex(bytes)
    local parts = {}
    for i, byte in ipairs(bytes) do
        parts[i] = string.format("%02X", byte)
    end
    return table.concat(parts)
end

-- Helper: atomically write the response file using rename
local function write_response(seq, response)
    local file, err = io.open(RESPONSE_FILE_TMP, "w")
    if not file then
        print("ERROR: cannot open " .. RESPONSE_FILE_TMP .. ": " .. tostring(err))
        return
    end
    file:write(seq .. " " .. response)
    file:close()
    -- os.rename overwrites atomically on POSIX. If something is wrong we fall back.
    local ok, rerr = os.rename(RESPONSE_FILE_TMP, RESPONSE_FILE)
    if not ok then
        print("ERROR: rename response failed: " .. tostring(rerr))
        os.remove(RESPONSE_FILE_TMP)
    end
end

-- Command handlers ---------------------------------------------------------

local function handle_read(addr, size)
    addr = tonumber(addr, 16)
    size = tonumber(size)
    if not addr or not size then
        return "ERROR bad READ args"
    end

    local bytes = {}
    for i = 0, size - 1 do
        bytes[i + 1] = emu.read(addr + i, emu.memType.nesMemory, false)
    end

    return "OK " .. bytes_to_hex(bytes)
end

local function handle_write(addr, hex_data)
    addr = tonumber(addr, 16)
    if not addr or not hex_data then
        return "ERROR bad WRITE args"
    end
    local bytes = hex_to_bytes(hex_data)

    for i, byte in ipairs(bytes) do
        emu.write(addr + i - 1, byte, emu.memType.nesMemory)
    end

    return "OK"
end

local function handle_step(frames)
    -- We are already running inside a per-frame callback. The emulator
    -- advances one frame between each invocation of process_command.
    -- True multi-frame stepping requires emu.resume() + sync mechanism,
    -- but for typical RL one command-per-frame this acknowledge is enough.
    return "OK"
end

local function handle_get_state()
    -- Read Dr. Mario P2 game state in one batch.
    local playfield = {}
    for i = 0, 127 do
        playfield[i + 1] = emu.read(0x0500 + i, emu.memType.nesMemory, false)
    end

    local virus_count = emu.read(0x03A4, emu.memType.nesMemory, false)
    local capsule_x = emu.read(0x0385, emu.memType.nesMemory, false)
    local capsule_y = emu.read(0x0386, emu.memType.nesMemory, false)
    local left_color = emu.read(0x0381, emu.memType.nesMemory, false)
    local right_color = emu.read(0x0382, emu.memType.nesMemory, false)
    local game_mode = emu.read(0x0046, emu.memType.nesMemory, false)

    -- Format: OK mode:virus:x:y:left:right:playfield_hex
    return string.format(
        "OK %d:%d:%d:%d:%d:%d:%s",
        game_mode,
        virus_count,
        capsule_x,
        capsule_y,
        left_color,
        right_color,
        bytes_to_hex(playfield)
    )
end

-- Frame loop ---------------------------------------------------------------

local frame_count = 0
local last_debug = 0
local commands_handled = 0

local function dispatch(cmd_line)
    local parts = {}
    for word in string.gmatch(cmd_line, "%S+") do
        table.insert(parts, word)
    end

    if #parts < 2 then
        return nil, "ERROR malformed command"
    end

    local seq = parts[1]
    local cmd = parts[2]

    if cmd == "READ" and #parts >= 4 then
        return seq, handle_read(parts[3], parts[4])
    elseif cmd == "WRITE" and #parts >= 4 then
        return seq, handle_write(parts[3], parts[4])
    elseif cmd == "STEP" then
        return seq, handle_step(parts[3])
    elseif cmd == "GET_STATE" then
        return seq, handle_get_state()
    elseif cmd == "PING" then
        return seq, "PONG"
    end
    return seq, "ERROR unknown command: " .. tostring(cmd)
end

local function process_command()
    frame_count = frame_count + 1

    -- Debug heartbeat every 5 seconds (300 frames @ 60 FPS)
    if frame_count - last_debug >= 300 then
        print(string.format("[bridge] frame=%d cmds_handled=%d", frame_count, commands_handled))
        last_debug = frame_count
    end

    -- Open command file; if absent or unreadable, nothing to do.
    local file = io.open(CMD_FILE, "r")
    if not file then
        return
    end

    local content = file:read("*all")
    file:close()
    -- Delete command file so Python knows it was consumed.
    os.remove(CMD_FILE)

    if not content or content == "" then
        return
    end

    local seq, response = dispatch(content)
    if seq then
        write_response(seq, response)
        commands_handled = commands_handled + 1
    end
end

-- Register frame callback (Mesen invokes us at the end of each rendered frame).
emu.addEventCallback(process_command, emu.eventType.endFrame)

-- Signal ready ONLY after cleanup + callback registration so Python doesn't race us.
local ready = io.open(READY_FILE, "w")
if ready then
    ready:write("READY\n")
    ready:close()
    print("Created ready file: " .. READY_FILE)
else
    print("FAILED to create ready file!")
end

print("===================================")
print("File-based bridge loaded (v3, atomic rename + sequence ids)")
print("Watching for commands every frame...")
print("===================================")

if emu.displayMessage then
    emu.displayMessage("Script", "File bridge ready")
end

print("Bridge ready. Waiting for commands...")

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

-- ---- Controller injection ----------------------------------------------
-- held[port] is a button table applied every input poll via emu.setInput,
-- which overrides the real controller (the only reliable way to drive the
-- game externally; direct $F5/$F6 writes get overwritten by the poll).
-- mask bits: 1=a 2=b 4=up 8=down 16=left 32=right 64=start 128=select
local held = {}
local function bit_on(mask, value)
    return (math.floor(mask / value) % 2) >= 1
end
local function handle_input(port_s, mask_s)
    local port = tonumber(port_s)
    local mask = tonumber(mask_s)
    if not port or not mask then return "ERROR bad input args" end
    held[port] = {
        a = bit_on(mask, 1), b = bit_on(mask, 2),
        up = bit_on(mask, 4), down = bit_on(mask, 8),
        left = bit_on(mask, 16), right = bit_on(mask, 32),
        start = bit_on(mask, 64), select = bit_on(mask, 128),
    }
    return "OK"
end
local function apply_input()
    for port, btns in pairs(held) do
        emu.setInput(btns, port)
    end
end
local function handle_release(port_s)
    local port = tonumber(port_s)
    if port then held[port] = nil end  -- stop overriding -> real controller resumes
    return "OK"
end

-- ---- Save-state load on demand ------------------------------------------
-- emu.loadSavestate must run inside an exec memory callback (IsSaveStateAllowed),
-- so we arm a one-shot exec callback that loads the .mss file then unregisters.
local pending_load_path = nil
local function do_load()
    if pending_load_path then
        local f = io.open(pending_load_path, "rb")
        if f then
            local data = f:read("*all"); f:close()
            if data and #data > 0 then
                local ok = emu.loadSavestate(data)
                print("[bridge] loadSavestate(" .. pending_load_path .. ") -> " .. tostring(ok))
            else
                print("[bridge] loadSavestate: empty file " .. pending_load_path)
            end
        else
            print("[bridge] loadSavestate: cannot open " .. pending_load_path)
        end
        pending_load_path = nil
        emu.removeMemoryCallback(do_load, emu.callbackType.exec, 0x8000, 0xFFFF)
    end
end
local function handle_loadstate(path)
    pending_load_path = path
    emu.addMemoryCallback(do_load, emu.callbackType.exec, 0x8000, 0xFFFF)
    return "OK loading"
end

-- Frame-perfect stepping: when step_mode is on, the emulator advances exactly
-- one frame per STEP and otherwise blocks in the endFrame callback, so Python
-- gets unlimited reads/writes/planning per frame with deterministic placement.
local step_mode = false
local function handle_stepmode(v)
    step_mode = (v == "1")
    return "OK stepmode=" .. tostring(step_mode)
end

-- Soft reset (like the console Reset button) -> returns to title screen, so the
-- driver can always start a fresh game regardless of the current game state.
local function handle_reset()
    emu.reset()
    return "OK reset"
end

-- Hard reset (power cycle) -> full RAM clear.
local function handle_powercycle()
    emu.powerCycle()
    return "OK powercycle"
end

-- PC-execution profiler: register a memory callback over a CPU range that
-- counts every instruction-execution there. Used to find which PCs dominate
-- the trace during a freeze.
local pc_hits = {}      -- pc -> count
local profile_lo = 0
local profile_hi = 0
local profile_cb = nil
local function pc_hit(addr, value, addr_type)
    pc_hits[addr] = (pc_hits[addr] or 0) + 1
end
local function handle_profile(start_hex, end_hex)
    local lo = tonumber(start_hex, 16)
    local hi = tonumber(end_hex, 16)
    -- Stop any prior profile
    if profile_cb then
        emu.removeMemoryCallback(profile_cb, emu.callbackType.exec, profile_lo, profile_hi)
        profile_cb = nil
    end
    pc_hits = {}
    profile_lo = lo
    profile_hi = hi
    profile_cb = pc_hit
    emu.addMemoryCallback(pc_hit, emu.callbackType.exec, lo, hi)
    return string.format("OK profile %04X-%04X", lo, hi)
end
local function handle_profile_stop()
    if profile_cb then
        emu.removeMemoryCallback(profile_cb, emu.callbackType.exec, profile_lo, profile_hi)
        profile_cb = nil
        return "OK profile stopped"
    end
    return "OK no profile active"
end
local function handle_profile_top(n)
    n = tonumber(n) or 20
    local pairs_list = {}
    for pc, cnt in pairs(pc_hits) do
        table.insert(pairs_list, {pc=pc, cnt=cnt})
    end
    table.sort(pairs_list, function(a,b) return a.cnt > b.cnt end)
    local parts = {}
    for i = 1, math.min(n, #pairs_list) do
        local p = pairs_list[i]
        table.insert(parts, string.format("%04X:%d", p.pc, p.cnt))
    end
    return "OK " .. table.concat(parts, " ")
end

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
    elseif cmd == "INPUT" and #parts >= 4 then
        return seq, handle_input(parts[3], parts[4])
    elseif cmd == "RELEASE" and #parts >= 3 then
        return seq, handle_release(parts[3])
    elseif cmd == "LOADSTATE" and #parts >= 3 then
        return seq, handle_loadstate(parts[3])
    elseif cmd == "STEPMODE" and #parts >= 3 then
        return seq, handle_stepmode(parts[3])
    elseif cmd == "RESET" then
        return seq, handle_reset()
    elseif cmd == "POWERCYCLE" then
        return seq, handle_powercycle()
    elseif cmd == "PROFILE" and #parts >= 4 then
        return seq, handle_profile(parts[3], parts[4])
    elseif cmd == "PROFILE_STOP" then
        return seq, handle_profile_stop()
    elseif cmd == "PROFILE_TOP" then
        return seq, handle_profile_top(parts[3])
    elseif cmd == "GETSP" then
        local st = emu.getState()
        local sp = (st and st.cpu and (st.cpu.sp or st.cpu.SP)) or -1
        return seq, "OK " .. tostring(sp)
    elseif cmd == "PING" then
        return seq, "PONG"
    end
    return seq, "ERROR unknown command: " .. tostring(cmd)
end

local function read_one_command()
    local file = io.open(CMD_FILE, "r")
    if not file then return nil end
    local content = file:read("*all")
    file:close()
    os.remove(CMD_FILE)
    if not content or content == "" then return nil end
    return content
end

local function second_word(s)
    local i = 0
    for w in string.gmatch(s, "%S+") do
        i = i + 1
        if i == 2 then return w end
    end
    return nil
end

local function process_command()
    frame_count = frame_count + 1
    if frame_count - last_debug >= 600 then
        print(string.format("[bridge] frame=%d cmds=%d stepmode=%s", frame_count, commands_handled, tostring(step_mode)))
        last_debug = frame_count
    end

    if not step_mode then
        -- free-run: handle at most one command this frame (original behavior)
        local content = read_one_command()
        if content then
            local seq, response = dispatch(content)
            if seq then write_response(seq, response); commands_handled = commands_handled + 1 end
        end
        return
    end

    -- step_mode: BLOCK here servicing commands (no frame advance) until a STEP
    -- (advance exactly one frame) or STEPMODE 0 (resume free-run).
    while true do
        local content = read_one_command()
        if content then
            local cmd = second_word(content)
            local seq, response = dispatch(content)
            if seq then write_response(seq, response); commands_handled = commands_handled + 1 end
            if cmd == "STEP" then return end
            if not step_mode then return end
        end
    end
end

-- Register frame callback (Mesen invokes us at the end of each rendered frame).
emu.addEventCallback(process_command, emu.eventType.endFrame)
-- Apply injected controller input every poll (overrides the real controller).
emu.addEventCallback(apply_input, emu.eventType.inputPolled)

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

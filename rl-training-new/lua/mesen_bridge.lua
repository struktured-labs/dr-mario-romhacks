-- Mesen Lua Bridge: Socket server for Python RL training
-- Provides memory read/write and frame stepping via TCP socket
--
-- Protocol: Simple text-based commands
-- Commands:
--   READ <addr> <size>        - Read <size> bytes from <addr>, returns hex string
--   WRITE <addr> <hex_data>   - Write hex bytes to <addr>
--   STEP <frames>             - Step N frames
--   GET_STATE                 - Get full game state (playfield, capsule, etc.)
--   QUIT                      - Close connection

local socket = require("socket")
local server = assert(socket.bind("*", 8765))
server:settimeout(0.001)  -- Non-blocking with small timeout

print("Mesen Bridge Server started on port 8765")
print("Waiting for connections...")

local client = nil
local client_connected = false

-- Helper: Convert hex string to byte table
function hex_to_bytes(hex)
    local bytes = {}
    for i = 1, #hex, 2 do
        local byte_str = hex:sub(i, i+1)
        table.insert(bytes, tonumber(byte_str, 16))
    end
    return bytes
end

-- Helper: Convert byte table to hex string
function bytes_to_hex(bytes)
    local hex = ""
    for _, byte in ipairs(bytes) do
        hex = hex .. string.format("%02X", byte)
    end
    return hex
end

-- Command handlers
function handle_read(addr, size)
    addr = tonumber(addr, 16)
    size = tonumber(size)

    local bytes = {}
    for i = 0, size-1 do
        local value = emu.read(addr + i, emu.memType.cpuMemory, false)
        table.insert(bytes, value)
    end

    return "OK " .. bytes_to_hex(bytes)
end

function handle_write(addr, hex_data)
    addr = tonumber(addr, 16)
    local bytes = hex_to_bytes(hex_data)

    for i, byte in ipairs(bytes) do
        emu.write(addr + i - 1, byte, emu.memType.cpuMemory)
    end

    return "OK"
end

function handle_step(frames)
    frames = tonumber(frames) or 1
    for i = 1, frames do
        emu.breakExecution()
    end
    return "OK"
end

function handle_get_state()
    -- Read Dr. Mario game state
    -- P2 playfield: $0500-$057F (128 bytes)
    -- P2 capsule X: $0385, Y: $0386
    -- P2 capsule colors: $0381 (left), $0382 (right)
    -- P2 virus count: $03A4

    local state = {}

    -- Read playfield (128 bytes)
    state.playfield = {}
    for addr = 0x0500, 0x057F do
        local value = emu.read(addr, emu.memType.cpuMemory, false)
        table.insert(state.playfield, value)
    end

    -- Read capsule state
    state.capsule_x = emu.read(0x0385, emu.memType.cpuMemory, false)
    state.capsule_y = emu.read(0x0386, emu.memType.cpuMemory, false)
    state.capsule_left_color = emu.read(0x0381, emu.memType.cpuMemory, false)
    state.capsule_right_color = emu.read(0x0382, emu.memType.cpuMemory, false)
    state.virus_count = emu.read(0x03A4, emu.memType.cpuMemory, false)
    state.game_mode = emu.read(0x0046, emu.memType.cpuMemory, false)

    -- Format as JSON-like string
    local result = string.format(
        "OK {playfield:%s,capsule_x:%d,capsule_y:%d,left_color:%d,right_color:%d,virus_count:%d,mode:%d}",
        bytes_to_hex(state.playfield),
        state.capsule_x,
        state.capsule_y,
        state.capsule_left_color,
        state.capsule_right_color,
        state.virus_count,
        state.game_mode
    )

    return result
end

function handle_command(cmd_line)
    local parts = {}
    for part in cmd_line:gmatch("%S+") do
        table.insert(parts, part)
    end

    if #parts == 0 then
        return "ERROR empty command"
    end

    local cmd = parts[1]:upper()

    if cmd == "READ" and #parts >= 3 then
        return handle_read(parts[2], parts[3])
    elseif cmd == "WRITE" and #parts >= 3 then
        return handle_write(parts[2], parts[3])
    elseif cmd == "STEP" then
        local frames = parts[2] or "1"
        return handle_step(frames)
    elseif cmd == "GET_STATE" then
        return handle_get_state()
    elseif cmd == "QUIT" then
        if client then client:close() end
        client = nil
        client_connected = false
        return "OK"
    else
        return "ERROR unknown command: " .. cmd
    end
end

-- Main loop (called every frame)
function on_frame()
    -- Accept new connections
    if not client_connected then
        local new_client, err = server:accept()
        if new_client then
            client = new_client
            client:settimeout(0.001)  -- Non-blocking
            client_connected = true
            print("Client connected!")
        end
    end

    -- Handle client commands
    if client_connected and client then
        local line, err = client:receive()
        if line then
            print("Received: " .. line)
            local response = handle_command(line)
            print("Response: " .. response)
            client:send(response .. "\n")
        elseif err ~= "timeout" then
            -- Connection closed or error
            print("Client disconnected: " .. tostring(err))
            if client then client:close() end
            client = nil
            client_connected = false
        end
    end
end

-- Register frame callback
emu.addEventCallback(on_frame, emu.eventType.endFrame)

print("Bridge initialized. Load a ROM to start.")

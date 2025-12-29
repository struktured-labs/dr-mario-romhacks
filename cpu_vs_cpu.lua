-- Dr. Mario CPU vs CPU Lua Script
-- Handles menu navigation and random AI for both players

local frame = 0
local game_started = false

-- Button constants
local BTN_A = 0x01
local BTN_B = 0x02
local BTN_SELECT = 0x04
local BTN_START = 0x08
local BTN_UP = 0x10
local BTN_DOWN = 0x20
local BTN_LEFT = 0x40
local BTN_RIGHT = 0x80

function main()
    frame = emu.framecount()

    local p1_input = 0
    local p2_input = 0

    if frame < 120 then
        -- Wait for title screen
    elseif frame < 150 then
        -- Press Start to exit title
        p1_input = BTN_START
    elseif frame < 180 then
        -- Wait
    elseif frame < 210 then
        -- Press Right to select 2P
        p1_input = BTN_RIGHT
    elseif frame < 240 then
        -- Wait
    elseif frame < 270 then
        -- Press Start to confirm 2P
        p1_input = BTN_START
    elseif frame < 350 then
        -- On level select, press Up to increase level (want level 11)
        if (frame % 10) < 5 then
            p1_input = BTN_UP
        end
    elseif frame < 380 then
        -- Press Right to increase speed to High
        p1_input = BTN_RIGHT
    elseif frame < 400 then
        -- Wait
    elseif frame < 430 then
        -- Press Start to begin game
        p1_input = BTN_START
        game_started = true
    else
        -- Game running - random inputs for both players
        local rand1 = math.random(0, 255)
        local rand2 = math.random(0, 255)

        -- Only use D-pad and A/B, throttle to every 4 frames
        if (frame % 4) == 0 then
            p1_input = bit.band(rand1, 0xC3)  -- D-pad + A/B
            p2_input = bit.band(rand2, 0xC3)
        end
    end

    -- Apply inputs
    joypad.set(1, {
        A = bit.band(p1_input, BTN_A) > 0,
        B = bit.band(p1_input, BTN_B) > 0,
        select = bit.band(p1_input, BTN_SELECT) > 0,
        start = bit.band(p1_input, BTN_START) > 0,
        up = bit.band(p1_input, BTN_UP) > 0,
        down = bit.band(p1_input, BTN_DOWN) > 0,
        left = bit.band(p1_input, BTN_LEFT) > 0,
        right = bit.band(p1_input, BTN_RIGHT) > 0
    })

    joypad.set(2, {
        A = bit.band(p2_input, BTN_A) > 0,
        B = bit.band(p2_input, BTN_B) > 0,
        select = bit.band(p2_input, BTN_SELECT) > 0,
        start = bit.band(p2_input, BTN_START) > 0,
        up = bit.band(p2_input, BTN_UP) > 0,
        down = bit.band(p2_input, BTN_DOWN) > 0,
        left = bit.band(p2_input, BTN_LEFT) > 0,
        right = bit.band(p2_input, BTN_RIGHT) > 0
    })

    -- Debug display
    if frame % 60 == 0 then
        print("Frame: " .. frame .. " Game started: " .. tostring(game_started))
    end
end

-- Register the main function to run every frame
emu.registerafter(main)
print("Dr. Mario CPU vs CPU script loaded!")

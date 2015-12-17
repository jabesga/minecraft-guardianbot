local component = require ("component")
local sides = require ("sides")
local event = require ("event")
local internet = require("internet")

local rs = component.redstone
local power_n, power_e, power_w, power_s = 0, 0, 0, 0
-- minecraft server and raspberry must be in the same local network

local URL = "http://127.0.0.1:8080" -- Students must write here the private IP of the server instead
local USERNAME = "delegate" -- Students must write here their Telegram username instead

local running = true
local delay_time = 2

print "\tGuardian program started"

while running do
    if event.pull() == "interrupted" then
        running = false
    else
        power_n = rs.getInput (sides.north)
        power_e = rs.getInput (sides.east)
        power_w = rs.getInput (sides.west)
        power_s = rs.getInput (sides.south)
        local message = "north=" .. power_n .. "&east=" .. power_e .. "&west=" .. power_w .. "&south=" .. power_s .. "&username=" .. USERNAME
        print "Making delay..."
        internet.request(URL, message)
        os.sleep(delay_time) -- no es la mejor solucion. pero evita el spam de conexiones abiertas
        print "Delay done"
    end
end

print "\tGuardian program stopped"

-- Posible implementation of rs.setOutput (sides.front, 9)
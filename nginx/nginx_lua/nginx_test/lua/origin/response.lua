--
-- Created by IntelliJ IDEA.
-- User: shih
-- Date: 9/7/16
-- Time: 2:25 PM
-- To change this template use File | Settings | File Templates.
--

local json = require "cjson"

local init_data = {
    [80] = 0.05,
    [8080] = 0.03,
    [8000] = 0.008
}

local port = tonumber(ngx.var.server_port)
local sleep_time = init_data[port] or 1

if port == 80 then
    ngx.exit(500)
end

local begin_time = ngx.now()
ngx.sleep(sleep_time)
local end_time = ngx.now()

ngx.say(json.encode({
    begin_time = begin_time,
    end_time = end_time,
    sleep_time = sleep_time
}))

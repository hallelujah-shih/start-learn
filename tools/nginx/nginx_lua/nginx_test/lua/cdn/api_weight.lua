-- Created by IntelliJ IDEA.
-- User: shih
-- Date: 9/7/16
-- Time: 5:54 PM
-- To change this template use File | Settings | File Templates.
--

local origin = require("origin_server")
local json = require("cjson")

local os_obj = origin:new()
local data = os_obj:get_all_weight() or {}

ngx.say(json.encode(data))

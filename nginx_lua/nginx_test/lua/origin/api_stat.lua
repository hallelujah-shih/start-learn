--
-- Created by IntelliJ IDEA.
-- User: shih
-- Date: 9/7/16
-- Time: 2:34 PM
-- To change this template use File | Settings | File Templates.
--

local json = require "cjson"
local stat = require "stat"

local stat_obj = stat:new()

local stat_info = stat_obj:get_all_stat_info() or {}

ngx.say(json.encode(stat_info))

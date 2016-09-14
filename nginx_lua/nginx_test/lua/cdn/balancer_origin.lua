--
-- Created by IntelliJ IDEA.
-- User: shih
-- Date: 9/5/16
-- Time: 6:30 PM
-- To change this template use File | Settings | File Templates.
--

local origin_server = require "origin_server"
local balancer = require("ngx.balancer")


local os_obj = origin_server:new()
local scheme, server, port, err = os_obj:get_origin()

if err then
    ngx.log(ngx.ERR, err)
else
    -- ngx.log(ngx.ERR, "server:", server, " port:", port)
    local _, err = balancer.set_current_peer(server, port)
    if err then
        ngx.log(ngx.ERR, "set_current_perr err:", err)
    end
end

--
-- Created by IntelliJ IDEA.
-- User: shih
-- Date: 9/8/16
-- Time: 4:10 PM
-- To change this template use File | Settings | File Templates.
--


local origin_server = require "srcip"
local balancer = require("ngx.balancer")


local os_obj = origin_server:new()
local server, port = os_obj:get()

if server and port then
    -- ngx.log(ngx.ERR, "server:", server, " port:", port)
    local _, err = balancer.set_current_peer(server, port)
    if err then
        ngx.log(ngx.ERR, "set_current_perr err:", err)
    end
end



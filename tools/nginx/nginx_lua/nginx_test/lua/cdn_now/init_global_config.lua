--
-- Created by IntelliJ IDEA.
-- User: shih
-- Date: 9/1/16
-- Time: 5:42 PM
-- To change this template use File | Settings | File Templates.
--
-- phase init example:
--[[
--nginx.conf:
--$set host_info "/etc/nginx/host_info.json;"
 - init_by_lua_file init_vhost_config.lua;-
-- ]]--

local json = require "cjson"

local origin = ngx.shared.origin
local fpath = '/etc/nginx/data/host_info.json'
local f = assert(io.open(fpath))
local json_str = f:read("*all")
f:close()

local vhosts_info = json.decode(json_str)

if vhosts_info and type(vhosts_info) == 'table' then
    for host, info in pairs(vhosts_info) do
        local hinfo = json.encode(info)
        origin:set(host, hinfo)
        ngx.log(ngx.ERR, "origin host:", host, " origin_info:", origin:get(host))
    end
end


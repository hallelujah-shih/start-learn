--
-- Created by IntelliJ IDEA.
-- User: shih
-- Date: 9/7/16
-- Time: 6:57 PM
-- To change this template use File | Settings | File Templates.
--

local json = require "cjson"
local math = require "math"

local _M = {}


function _M:new()
    local obj = {
        allow = ngx.shared.control,
        host = ngx.var.host
    }

    local origin = ngx.shared.origin
    local origin_str = origin:get(ngx.var.host)
    -- ngx.log(ngx.ERR, "origin_info:", origin_str, " host:", ngx.var.host)
    if origin_str and origin_str ~= '' then
        local origin = json.decode(origin_str)
        obj.origin = origin
    end

    setmetatable(obj, self)
    self.__index = self

    return obj
end

function _M:get_addr()
    local client_ip = ngx.req.arg_ip
    if client_ip then
        local o1, o2, o3, o4 = string.match(client_ip, "(%d+)%.(%d+)%.(%d+)%.(%d+)")
        if o1 and o2 and o3 and o4 then
            local num = 2^24 *o1 + 2^16*o2 + 2^8*o3 + o4
            return num
        end
    end
    return ngx.var.remote_port
end

function _M:filter_alive_origin_list(origin_list)
    local rt_origin_list = {}
    local o_len = #origin_list
    if o_len == 1 then
        return origin_list
    elseif o_len > 1 then
        for _, oinfo in ipairs(origin_list) do
            local key = self.host .. ':' .. oinfo['host'] .. ':' .. oinfo['port']
            local val = self.allow:get(key) or 0
            if val < 10 then
                rt_origin_list[#rt_origin_list + 1] = oinfo
            end
        end
    end
    if #rt_origin_list >= 1 then
        return rt_origin_list
    else
        return origin_list
    end
end

function _M:get()
    if not self.origin then
        return ""
    end

    local origin_server_list = self.origin["origin_server"]
    if not origin_server_list then
        return ""
    end

    local origin_server_list = self:filter_alive_origin_list(origin_server_list)

    local ss_len = #origin_server_list

    if ss_len == 1 then
        return origin_server_list[1]["host"], origin_server_list[1]['port']
    end

    if ss_len > 1 then
        local total_sum = 0
        for _, v in ipairs(origin_server_list) do
            total_sum = total_sum + v['weight']
        end

        math.randomseed(self:get_addr())
        local choice = math.random()

        local tmp_sum = 0
        for _, v in ipairs(origin_server_list) do
            tmp_sum = tmp_sum + v['weight']
            local w = tmp_sum / total_sum
            if choice < w then
                return v['host'], v['port']
            end
        end
    end
    return ""
end


return _M

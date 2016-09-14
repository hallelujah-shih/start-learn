--
-- Created by IntelliJ IDEA.
-- User: shih
-- Date: 9/1/16
-- Time: 6:36 PM
-- To change this template use File | Settings | File Templates.
--

local math = require "math"

local allow = ngx.shared.origin_allow
local weight = ngx.shared.weight
local host = ngx.var.host
local shared_dict_key = host .. ':' .. ngx.var.upstream_addr
local response_time = ngx.var.upstream_response_time
local status = ngx.var.upstream_status
local response_size = ngx.var.upstream_response_length


local function calc_weight(old_weight, rate, status)
    local new_weight
    if status < 500 then
        local add_rate = math.log(1 + rate * rate)
        new_weight = math.max(math.min(old_weight + math.log10(1 + add_rate), 10000), 0.0001)
    else
        new_weight = old_weight * 0.9
    end
    return new_weight
end

if status and response_time and response_size then
    local resp_time = tonumber(response_time) or 10
    local resp_status = tonumber(status) or 500
    local resp_size = tonumber(response_size) or 1024

    -- FIXME 处理resp_size为0的情况
    local resp_rate = resp_size / (resp_time * 1024 * 512)

    local old_value = allow:get(shared_dict_key) or 0

    -- ngx.log(ngx.ERR, "old_value: ", old_value)
    if resp_status >= 500 then
        if old_value then
            old_value = old_value + 25
        else
            old_value = 10
        end
        old_value = math.min(old_value, 100)
    else
        old_value = old_value - 5
        old_value = math.max(old_value, 0)
    end
    allow:set(shared_dict_key, old_value, 5 * 60)

    local old_weight = weight:get(shared_dict_key) or 50
    local new_weight = calc_weight(old_weight, resp_rate, resp_status)
    weight:set(shared_dict_key, new_weight)
    -- ngx.log(ngx.ERR, ngx.var.upstream_addr, " new_weight:", new_weight, " old_weight:", old_weight)
end



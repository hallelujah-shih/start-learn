--
-- Created by IntelliJ IDEA.
-- User: shih
-- Date: 9/8/16
-- Time: 3:10 PM
-- To change this template use File | Settings | File Templates.
--

local upstream_addr = ngx.var.upstream_addr
local upstream_status = tonumber(ngx.var.upstream_status)
local control_origin = ngx.shared.control

if upstream_addr and upstream_status then
    local key = ngx.var.host .. ':' .. upstream_addr
    if upstream_status >= 500 then
        local new_val = control_origin:incr(key, 1)
        if not new_val then
            control_origin:set(key, 1, 61)
        elseif new_val >= 10 then
            control_origin:set(key, new_val, 3000)
        end
    end
end

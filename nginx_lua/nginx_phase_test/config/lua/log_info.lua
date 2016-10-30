local status = require "status"
local log = ngx.shared.log

_M = {}

function _M.append_log(msg)
    if msg and msg ~= '' then
        local key = ngx.var.remote_addr .. ':' .. ngx.var.remote_port
        local msg = msg .. status.run()
        local old_msg = log:get(key)
        if not old_msg then
            local success, err = log:add(key, '\n' .. msg)
            if not success and err == 'exists' then
                old_msg = log:get(key)
                local new_msg = old_msg .. ':' .. msg
                log:set(key, new_msg)
            end
        else
            local new_msg = old_msg .. ':' .. msg
            log:set(key, new_msg)
        end
    end
end

function _M.rm()
    local key = ngx.var.remote_addr .. ':' .. ngx.var.remote_port
    local msg = log:get(key)
    ngx.log(ngx.ERR, "recored info:", msg)
    log:delete(key)
end

return _M

--
-- Created by IntelliJ IDEA.
-- User: shih
-- Date: 9/7/16
-- Time: 11:25 AM
-- To change this template use File | Settings | File Templates.
--

local _M = {}

function _M:new()
    local o = {
        status = tonumber(ngx.var.status),
        local_addr = ngx.var.server_addr,
        local_port = ngx.var.server_port,
        remote_addr = ngx.var.remote_addr,
        remote_port = ngx.var.remote_port,
        stat_access = ngx.shared.stat_access
    }

    setmetatable(o, self)
    self.__index = self

    return o
end

function _M:get_server_stat_key()
    local status = 'err'
    if self.status and (self.status < 500) then
        status = 'ok'
    end

    local suffix = ":server:" .. status
    return self.local_addr .. ':' .. self.local_port .. suffix
end

function _M:get_client_stat_key()
    local status = 'err'
    if self.status and (self.status < 500) then
        status = 'ok'
    end

    local suffix = ":client:" .. status
    return self.remote_addr .. suffix
end

function _M:stat_update()
    local sk = self:get_server_stat_key()
    local ck = self:get_client_stat_key()

    local newval, err = self.stat_access:incr(sk, 1)
    if not newval and err == 'not found' then
        self.stat_access:add(sk, 0)
        self.stat_access:incr(sk, 1)
    end

    newval, err = self.stat_access:incr(ck, 1)
    if not newval and err == 'not found' then
        self.stat_access:add(ck, 0)
        self.stat_access:incr(ck, 1)
        local tmp = self.stat_access:get(ck)
    end
end


function _M:get_all_stat_info()
    local all_stat_info = {}

    local keys = self.stat_access:get_keys()
    if keys then
        for _, key in ipairs(keys) do
            local val = self.stat_access:get(key)
            if val then
                all_stat_info[key] = val
            end
        end
    end

    return all_stat_info
end

function _M:get_stat_info(addr)
    local stat_info = {}

    local keys = self.stat_access:get_keys()
    if keys then
        for key in ipairs(keys) do
            local index = string.find(key, addr)
            if index == 1 then
                local val = self.stat_access:get(key)
                if val then
                    stat_info[key] = val
                end
            end
        end
    end

    return stat_info
end

function _M:clean_stat_info(addr)
    local keys = self.stat_access:get_keys()
    if keys then
        for key in ipairs(keys) do
            local index = string.find(key, addr)
            if index == 1 then
                self.stat_access:set(key, nil)
            end
        end
    end
end

function _M:clean_all_stat_info()
    self.stat_access:flush_all()
end

return _M

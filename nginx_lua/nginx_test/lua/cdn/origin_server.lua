--
-- Created by IntelliJ IDEA.
-- User: shih
-- Date: 8/31/16
-- Time: 5:00 PM
-- To change this template use File | Settings | File Templates.
--

local json = require "cjson"
local math = require "math"

local _M = {}

function _M.new(self)
    local obj = {
        weight = ngx.shared.weight,
        allow = ngx.shared.origin_allow
    }

    local origin = ngx.shared.origin
    obj.host = ngx.var.host
    local origin_str = origin:get(obj.host)
    -- ngx.log(ngx.ERR, "origin_info:", origin_str, " host:", ngx.var.host)
    if origin_str and origin_str ~= '' then
        local origin = json.decode(origin_str)
        obj.origin = origin
    end

    setmetatable(obj, self)
    self.__index = self

    return obj
end

function _M.get_origin(self)
    local rt_scheme, rt_host, rt_port, err

    if self.origin then
        local origin_server_list = self.origin["origin_server"]
        if origin_server_list then
            origin_server_list = self:filter_online_origin(origin_server_list)
            local total_servers = #origin_server_list
            if total_servers == 1 then
                rt_host = origin_server_list[1]['host']
                rt_port = origin_server_list[1]['port'] or 80
                rt_scheme = origin_server_list[1]['scheme'] or 'http'
            elseif total_servers > 1 then
                rt_scheme, rt_host, rt_port, err = self:get_peer(origin_server_list)
            else
                err = 'config error, has no origin server.'
            end
        else
            err = 'config error, has no origin server.'
        end
    else
        err = 'no vhost config.'
    end
    return rt_scheme, rt_host, rt_port, err
end

function _M.filter_online_origin(self, os_list)
    local origin_server_list = {}
    local os_len = #os_list
    if os_len == 1 then
        origin_server_list[#origin_server_list + 1] = os_list[1]
    elseif os_len > 1 then
        for _, origin_server in ipairs(os_list) do
            local upstream_addr = self.host .. ':' .. origin_server['host'] .. ':' .. origin_server['port']
            if upstream_addr and upstream_addr ~= '' then
                local allow_count = self.allow:get(upstream_addr) or 0
                if allow_count and allow_count < 100 then
                    origin_server_list[#origin_server_list + 1] = origin_server
                end
            end
        end
        if #origin_server_list < 1 then
            origin_server_list = os_list
        end
    end

    return origin_server_list
end

function _M.get_peer(self, origin_info)
    local scheme, host, port, err
    local tmp_origin_info = {}
    local origin_weight = {}
    local total = 0
    -- 计算所有数的和
    for _, v in ipairs(origin_info) do
        local key = self.host .. ':' .. v['host'] .. ':' .. v['port']
        local weight = self.weight:get(key)
        if not weight then
            weight = v['weight']
            self.weight:add(key, weight)
        end
        tmp_origin_info[key] = v
        origin_weight[key] = weight
        total = total + weight
    end

    if total > 0 then
        -- FIXME 上线前需要将port改为client ip的整数
        math.randomseed(ngx.time() + ngx.var.remote_port)
        local choice = math.random()
        -- ngx.log(ngx.ERR, "*choice:", choice)
        -- FIXME 此处可以对表进行排序再处理
        local tmp = 0
        for addr, weight in pairs(origin_weight) do
            tmp = tmp + weight
            local v = tmp / total
            -- ngx.log(ngx.ERR, "-tmp value:", tmp, " choice:", choice, " v:", v)
            if choice < v then
                local oinfo = tmp_origin_info[addr]

                scheme = oinfo['scheme']
                host = oinfo['host']
                port = oinfo['port']
                break
            end
        end
    else
        err = 'weight must gt 0.'
    end

    return scheme, host, port, err
end

function _M.get_weight(self, host)
    local origin = ngx.shared.origin

    local rt = {}
    if host and type(host) == 'string' then
        local oinfo = origin:get(host)
        if oinfo then
            local tmp = json.decode(oinfo) or {}
            local os_list = tmp["origin_server"] or {}
            for _, os in ipairs(os_list) do
                local key = host .. ':' .. os['host'] .. ':' .. os['port']
                rt[key] = self.weight:get(key) or os['weight']
            end
        end
    end

    return rt
end

function _M.get_all_weight(self)
    local rt = {}
    local hosts = ngx.shared.origin:get_keys() or {}
    for _, host in ipairs(hosts) do
        rt[host] = self:get_weight(host)
    end

    return rt
end

return _M

_M = {}

function _M.run()
    local msg = string.format("current_location(%s) status(%s) u_addr(%s) u_cache_status(%s) u_con_time(%s) u_resp_len(%s) u_resp_time(%s) u_status(%s) uri(%s)\n", 
    ngx.var.current_location,
    ngx.status, 
    ngx.var.upstream_addr, 
    ngx.var.upstream_cache_status, 
    ngx.var.upstream_connect_time, 
    ngx.var.upstream_response_length, 
    ngx.var.upstream_response_time, 
    ngx.var.upstream_status,
    ngx.var.request_uri)
    return msg
end

return _M


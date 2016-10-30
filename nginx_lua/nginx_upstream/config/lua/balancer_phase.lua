local balancer = require "ngx.balancer"

print('into balancer')
local alist = ngx.ctx.access_list
ngx.var.srcip = #alist

local data = table.remove(alist, 1)
if #data == 2 and type(data) == 'table' then
    balancer.set_current_peer(data[1], data[2])
    if #alist >= 1 then
        local ok, err = balancer.set_more_tries(1)
        if not ok then 
            print("set more tries error:", err)
        end
    end
else
    print("unknown data:", data)
end

local log = require "log_info"
local balancer = require "ngx.balancer"

local msg = "into balancer_phase status " 
log.append_log(msg)

balancer.set_current_peer("23.22.14.18", 80)

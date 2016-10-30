local log = require "log_info"

local msg = "into content_phase status " 
log.append_log(msg)

ngx.sleep(20)

ngx.status = 504
ngx.say('hello world')
ngx.exit(504)

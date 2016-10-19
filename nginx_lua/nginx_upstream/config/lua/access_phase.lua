ngx.ctx.access_list = {{'122.114.45.153', 9090}, {'122.114.38.225', 9999}, {'122.114.38.225', 80}}
ngx.var.srcip = "hello"
print("into access_phase srcip:", ngx.var.srcip)

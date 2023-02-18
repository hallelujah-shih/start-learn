local key = {}
-- unique key
local mt = { __index = function(t) return t[key] end }
function setDefault(t, d)
    t[key] = d
    setmetatable(t, mt)
end

local test_table = {}
print("before set default: ", test_table.hello)

setDefault(test_table, 1)

print("after set default: ", test_table.hello)

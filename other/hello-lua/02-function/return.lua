function triple(x)
    return x, 2 * x, 3 * x
end

local a, _, c = triple(5)

local results = { triple(3) }

print(a, c)

for k, v in pairs(results) do
    print(k, v)
end

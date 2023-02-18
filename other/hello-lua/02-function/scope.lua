local global = 1

function func()
    local local_val = 2
    global = global + 1
    return global
end

func()

print(global)
-- out scope (nil)
print(local_val)

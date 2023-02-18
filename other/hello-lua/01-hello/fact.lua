function fact(num)
    if num == 0 then
        return 1
    else
        return num * fact(num - 1)
    end
end

print("enter a number:")

value = io.read("*n")
print("input value:", value)
print(fact(value))

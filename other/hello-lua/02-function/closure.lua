function getArea(type_name)
    local return_func
    if type_name == "rect" then
        return_func = function(width, height)
            local area = width * height
            return area
        end
    else
        return_func = function(botton, height)
            local area = 0.5 * botton * height
            return area
        end
    end
    return return_func
end

local area = getArea("rect")
print(area(4, 5))

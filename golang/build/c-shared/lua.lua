local ffi = require("ffi")

local hello = ffi.load("./libhello.so")


ffi.cdef([[
    void PrintHello(void);
    ]])

hello.PrintHello()

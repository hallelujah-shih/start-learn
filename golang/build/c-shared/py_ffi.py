import sys
from cffi import FFI


ffi = FFI()
ffi.cdef("""
    void PrintHello();
""")

hello_lib = ffi.dlopen("./libhello.so")
hello_lib.PrintHello()

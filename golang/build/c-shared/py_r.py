from ctypes import *


hello = cdll.LoadLibrary("./libhello.so")
hello.PrintHello()

#pragma once

class Foo {
public:
  Foo();

  void stack_buf_overflow_func();
  void mem_leak_func();
};
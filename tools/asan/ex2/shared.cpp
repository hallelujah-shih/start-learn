#include "shared.h"

Foo::Foo() {}

void Foo::mem_leak_func() { char *p = new char[1]; }

void Foo::stack_buf_overflow_func() {
  char buf[1];
  buf[2] = 3;
}

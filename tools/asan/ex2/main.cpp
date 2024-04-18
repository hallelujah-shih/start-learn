#include "shared.h"

int main(int, char **) {
  Foo f;
  f.mem_leak_func();
  //   f.stack_buf_overflow_func();
  return 0;
}
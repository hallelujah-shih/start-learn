.PHONY: using-gcc using-gcc-static using-clang

using-gcc:
	g++ -o main-gcc -lasan -O -g -fsanitize=address -fno-omit-frame-pointer main.cpp && \
	ASAN_OPTIONS=symbolize=1 ASAN_SYMBOLIZER_PATH=$(shell which llvm-symbolizer) ./main-gcc

using-gcc-static:
	g++ -o main-gcc-static -static-libstdc++ -static-libasan -O -g -fsanitize=address -fno-omit-frame-pointer main.cpp && \
	ASAN_OPTIONS=symbolize=1 ASAN_SYMBOLIZER_PATH=$(shell which llvm-symbolizer) ./main-gcc-static

using-clang:
	clang -o main-clang -x c++ -O -g -fsanitize=address main.cpp && \
	ASAN_OPTIONS=symbolize=1 ASAN_SYMBOLIZER_PATH=$(shell which llvm-symbolizer) ./main-clang
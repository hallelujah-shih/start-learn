.PHONY: v1 v2 clean

v1:
	g++ -Wl,--no-undefined -shared -o libshared.so shared.cpp -g3
	g++ -fno-omit-frame-pointer -fsanitize=address main.cpp -lshared -L . -Wl,-rpath=. -g3

v2:
	g++ -fno-omit-frame-pointer -fsanitize=address -Wl,--no-undefined -shared -o libshared.so shared.cpp -g3 -lasan -fPIC
	g++ -fno-omit-frame-pointer -fsanitize=address main.cpp -lshared -L . -Wl,-rpath=. -g3

clean:
	rm -f *.so a.out

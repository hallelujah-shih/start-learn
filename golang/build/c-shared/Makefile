ALL: golib hello hello_dl

golib:
	go build -buildmode=c-shared -o libhello.so hello.go

hello:
	gcc hello.c -L. -Wl,-rpath,. -lhello -o hello

hello_dl:
	gcc hello_dl.c -o hello_dl -ldl

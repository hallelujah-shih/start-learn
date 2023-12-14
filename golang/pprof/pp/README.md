go run main.go

代理：
    socat TCP-LISTEN:1337,bind=127.0.0.1,reuseaddr,fork UNIX-CONNECT:/tmp/pprof-test.sock

性能分析:
    go tool pprof -http="127.0.0.1:8000" "http://localhost:1337/debug/pprof/profile?seconds=30"

or
    curl --unix-socket /tmp/pprof-test.sock -X GET http://localhost/debug/pprof/profile?seconds=30 -o mypprof.gz
    go tool pprof -http=127.0.0.1:8000 mypprof.gz


## ref
* [Redirecting TCP-traffic to a UNIX domain socket under Linux](https://stackoverflow.com/questions/2149564/redirecting-tcp-traffic-to-a-unix-domain-socket-under-linux)
* [Using golang's pprof over a Unix Socket](https://www.xkyle.com/Using-golangs-pprof-over-a-Unix-Socket/)
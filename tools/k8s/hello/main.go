package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"net/http"
	"strings"
)

type contextKey struct {
	key string
}

var ConnContextKey = &contextKey{"http-conn"}

func SaveConnInContext(ctx context.Context, c net.Conn) context.Context {
	return context.WithValue(ctx, ConnContextKey, c)
}

func GetConn(r *http.Request) net.Conn {
	return r.Context().Value(ConnContextKey).(net.Conn)
}

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		conn := GetConn(r).(*net.TCPConn)
		var msgBuilder strings.Builder
		msgBuilder.WriteString("-----------conn   info----------\n")
		msgBuilder.WriteString(fmt.Sprintf("%v -> %v\n", conn.RemoteAddr(), conn.LocalAddr()))
		msgBuilder.WriteString("-----------header info----------\n")
		msgBuilder.WriteString(fmt.Sprintf("%v %v %s\n", r.Method, r.URL.RequestURI(), r.Proto))
		msgBuilder.WriteString(fmt.Sprintf("Host: %s\n", r.Host))
		for k, vlist := range r.Header {
			for _, v := range vlist {
				msgBuilder.WriteString(fmt.Sprintf("%v: %v\n", k, v))
			}
		}
		fmt.Fprintf(w, "%s", msgBuilder.String())
	})

	server := http.Server{
		Addr:        ":8080",
		ConnContext: SaveConnInContext,
	}

	log.Fatal(server.ListenAndServe())
}

package main

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/redis/go-redis/v9"
)

func handler(w http.ResponseWriter, r *http.Request) {
	rdb := redis.NewClient(&redis.Options{
		Addr:     "redis:6379",
		Password: "",
		DB:       0,
	})

	s := fmt.Sprintf("client: %v method: %v url: %v", r.RemoteAddr, r.Method, r.URL.RawPath)

	if _, err := rdb.LPush(context.Background(), "req_info", s).Result(); err != nil {
		fmt.Println("lpush err:", err)
	}

	w.Write([]byte("success access\n"))
}

func main() {
	http.HandleFunc("/", handler)
	http.Handle("/metrics", promhttp.Handler())

	fmt.Println("begin listen: 8089")
	log.Fatal(http.ListenAndServe(":8089", nil))
}

package main

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/redis/go-redis/v9"
)

func fetchReqInfo(wg *sync.WaitGroup) {
	defer wg.Done()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "redis:6379",
		Password: "",
		DB:       0,
	})

	timer := time.NewTicker(5 * time.Second)
	for {
		select {
		case <-timer.C:
			data, err := rdb.RPop(context.Background(), "req_info").Result()
			if err != nil {
				fmt.Println("rpop err:", err)
				continue
			}

			fmt.Println("recv req:", data)

			return
		}
	}
}

func fetchMetrics(wg *sync.WaitGroup) {
	defer wg.Done()

	timer := time.NewTicker(30 * time.Second)
	for {
		select {
		case <-timer.C:
			resp, err := http.Get("http://host.docker.internal:8089/metrics")
			if err != nil {
				panic(err)
			}
			body, err := io.ReadAll(resp.Body)
			resp.Body.Close()

			fmt.Println("recv api rsp:", string(body), "err:", err)

			return
		}
	}
}

func autoReq(wg *sync.WaitGroup) {
	defer wg.Done()

	resp, err := http.Get("http://host.docker.internal:8089/")
	if err != nil {
		panic(err)
	}

	defer resp.Body.Close()
	io.Copy(os.Stdout, resp.Body)
}

func main() {
	var wg sync.WaitGroup
	wg.Add(3)

	go autoReq(&wg)
	go fetchReqInfo(&wg)
	go fetchMetrics(&wg)

	wg.Wait()
}

package main

import (
	"log"
	"net"
	"net/http"
	_ "net/http/pprof"
	"os"
	"runtime"
	"syscall"
	"time"
)

func sender(out chan int) {
	i := 0
	for {
		out <- i
		i++
	}
}

func reader(in chan int) {
	builkSize := 10000
	buf := make([]int, builkSize)
	for {
		curIndex := 0
		for data := range in {
			buf[curIndex] = data
			curIndex++
			if curIndex == builkSize {
				break
			}
		}

		//deal
		time.Sleep(200 * time.Millisecond)
	}
}

func main() {
	runtime.SetBlockProfileRate(1000)
	unixAddr := "/tmp/pprof-test.sock"

	fileInfo, err := os.Stat(unixAddr)
	if err == nil {
		if stat, ok := fileInfo.Sys().(*syscall.Stat_t); ok {
			linkCount := stat.Nlink
			if linkCount <= 1 {
				os.Remove(unixAddr)
			}
		}
	}

	unixListener, err := net.Listen("unix", unixAddr)
	if err != nil {
		log.Fatal("Error creating Unix socket:", err)
	}
	defer os.Remove(unixAddr) // 大概率清理不掉

	// 启动 HTTP 服务
	go func() {
		log.Fatal(http.Serve(unixListener, nil))
	}()

	pipeBuf := make(chan int)
	go sender(pipeBuf)

	go reader(pipeBuf)

	num := int64(0)
	for {
		num += 1
		if num%100000 == 0 {
			log.Println(num)
			time.Sleep(500 * time.Millisecond)
		}
	}
}

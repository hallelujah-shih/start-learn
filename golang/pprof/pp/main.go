package main

import (
	"log"
	"net"
	"net/http"
	_ "net/http/pprof"
	"os"
	"syscall"
	"time"
)

func main() {
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

	num := int64(0)
	for {
		num += 1
		if num%100000 == 0 {
			log.Println(num)
			time.Sleep(500 * time.Millisecond)
		}
	}
}

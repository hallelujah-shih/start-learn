package main

import "C"

import (
	"fmt"
	"time"
)

//export PrintHello
func PrintHello() {
	fmt.Println("hello, now:", time.Now())
}

func main() {
}

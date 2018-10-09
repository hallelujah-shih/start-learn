package main

import "fmt"

func recoverName() {
	if r := recover(); r != nil {
		fmt.Println("recovered from ", r)
	}
}

func recoverTest(arg1, arg2 *string) {
	defer recoverName()
	if arg1 == nil {
		panic("runtime error: arg1 is nil")
	}
	if arg2 == nil {
		panic("runtime error: arg2 is nil")
	}
}

func main() {
	defer fmt.Println("vim-go")
	arg1 := ""
	arg2 := ""
	recoverTest(nil, &arg2)
	recoverTest(&arg1, nil)
	recoverTest(&arg1, &arg2)
}

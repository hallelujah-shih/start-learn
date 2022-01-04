//
// main.go
// Copyright (C) 2022 shih <shih@fedora>
//
// Distributed under terms of the MIT license.
//

package main

import (
	"context"
	"errors"
	"fmt"
	"time"
)

func main() {

	ctx, cancel := context.WithCancel(context.Background())

	go func() {
		err := action_1(ctx)

		if err != nil {
			cancel()
		}
	}()

	go func() {
		ctx2, cancel2 := context.WithCancel(ctx)

		err := action_2(ctx2)
		if err != nil {
			cancel2()
		}

	}()

	action_3(ctx)

}

func action_1(ctx context.Context) error {
	time.Sleep(10000 * time.Millisecond)
	return errors.New("failed")
}

func action_2(ctx context.Context) error {
	select {
	case <-time.After(1500 * time.Millisecond):
		fmt.Println("action_2 done")
	case <-ctx.Done():
		fmt.Println("cancel action 2")
	}
	return nil
}

func action_3(ctx context.Context) {
	select {
	case <-time.After(1700 * time.Millisecond):
		fmt.Println("action_3 done")
	case <-ctx.Done():
		fmt.Println("cancel action 3")
	}
}

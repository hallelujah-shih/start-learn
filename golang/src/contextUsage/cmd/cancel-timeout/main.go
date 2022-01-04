//
// main.go
// Copyright (C) 2022 shih <shih@fedora>
//
// Distributed under terms of the MIT license.
//
package main

import (
	"context"
	"fmt"
	"net/http"
	"time"
)

func main() {
	ctx, _ := context.WithTimeout(context.Background(), 500*time.Millisecond)

	req, _ := http.NewRequest(http.MethodGet, "https://www.baidu.com/", nil)

	req = req.WithContext(ctx)

	client := &http.Client{}
	res, err := client.Do(req)

	if err != nil {
		fmt.Println("Request failed:", err)
		return
	}

	fmt.Println("Response received, status code:", res.StatusCode)
}

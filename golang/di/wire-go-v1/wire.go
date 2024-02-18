//go:build wireinject

package main

import "github.com/google/wire"

func InitializeEvent() Event {
	wire.Build(GetMessage, GetGreeter, GetEvent)
	return Event{}
}

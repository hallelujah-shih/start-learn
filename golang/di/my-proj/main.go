package main

import (
	"fmt"
)

type Message string
type Greeter struct {
	Message Message
}
type Event struct {
	Greeter Greeter
}

func GetMessage() Message {
	return Message("Hello world!")
}
func GetGreeter(m Message) Greeter {
	return Greeter{Message: m}
}
func (g Greeter) Greet() Message {
	return g.Message
}
func GetEvent(g Greeter) Event {
	return Event{Greeter: g}
}
func (e Event) Start() {
	msg := e.Greeter.Greet()
	fmt.Println(msg)
}
func main() {
	message := GetMessage()
	greeter := GetGreeter(message)
	event := GetEvent(greeter)

	event.Start()
}

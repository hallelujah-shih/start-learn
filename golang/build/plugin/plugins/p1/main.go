package main

import (
	"fmt"
	"plugin/plugins"
)

var (
	pluginName = "p1"
)

func init() {
	fmt.Println("init  plugin:", pluginName)
}

type plugin1 struct {
	name string
}

func (p *plugin1) Name() string {
	return p.name
}

func New() plugins.Plugin {
	return &plugin1{name: pluginName}
}

var Plugin1 = &plugin1{name: pluginName}

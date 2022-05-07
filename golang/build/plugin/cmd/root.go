/*
Copyright © 2022 shih <shih@knownsec.com>

*/
package cmd

import (
	"fmt"
	"log"
	"os"
	"plugin"
	"plugin/plugins"

	"github.com/spf13/cobra"
)

var (
	pluginPath string
)

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "plugin",
	Short: "测试插件",
	Run: func(cmd *cobra.Command, args []string) {
		p, err := plugin.Open(pluginPath)
		if err != nil {
			log.Panicln(err)
		}
		v, err := p.Lookup("New")
		if err != nil {
			log.Panicln(err)
		}
		vi, ok := v.(func() plugins.Plugin)
		if !ok {
			log.Panicln("cast failed")
		}
		obj := vi()
		fmt.Println(obj.Name())
	},
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.PersistentFlags().StringVarP(&pluginPath, "plugin", "p", "", "插件路径")
	rootCmd.MarkPersistentFlagRequired("plugin")
}

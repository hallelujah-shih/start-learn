/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"os"

	"github.com/spf13/cobra"
)

var (
	listenAddr     string
	caPath         string
	serverCertPath string
	ServerKeyPath  string
	ignoreVerify   bool
)

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "server",
	Short: "测试双向认证",
	// Uncomment the following line if your bare application
	// has an action associated with it:
	Run: func(cmd *cobra.Command, args []string) {
		tlsServer()
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
	rootCmd.Flags().StringVarP(&listenAddr, "listen", "l", ":8443", "server listen addr")
	rootCmd.Flags().StringVar(&caPath, "ca", "ca.pem", "ca path")
	rootCmd.Flags().StringVar(&serverCertPath, "cert", "server.pem", "server cert path")
	rootCmd.Flags().StringVar(&ServerKeyPath, "key", "server-key.pem", "server key path")
	rootCmd.Flags().BoolVarP(&ignoreVerify, "ignore-verify", "i", false, "ignore verify")
	rootCmd.MarkFlagRequired("cert")
	rootCmd.MarkFlagRequired("key")
}

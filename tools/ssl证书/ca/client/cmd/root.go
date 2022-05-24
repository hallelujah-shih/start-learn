/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"context"
	"os"

	"github.com/spf13/cobra"
)

var (
	serverListen   string
	caPath         string
	clientCertPath string
	clientKeyPath  string
	ignoreVerify   bool
)

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "client",
	Short: "证书双向认证客户端",
	Run: func(cmd *cobra.Command, args []string) {
		reqSvc(context.Background())
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
	rootCmd.Flags().StringVarP(&serverListen, "server", "s", "127.0.0.1:8443", "服务端监听地址")
	rootCmd.Flags().StringVar(&caPath, "ca", "ca.pem", "CA证书路径")
	rootCmd.Flags().StringVar(&clientCertPath, "cert", "client.pem", "客户端证书路径")
	rootCmd.Flags().StringVar(&clientKeyPath, "key", "client.key", "客户端私钥路径")
	rootCmd.Flags().BoolVarP(&ignoreVerify, "ignore-verify", "i", false, "忽略服务端证书验证")
	rootCmd.MarkFlagRequired("server")
	rootCmd.MarkFlagRequired("cert")
	rootCmd.MarkFlagRequired("key")
}

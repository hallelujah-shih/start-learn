package cmd

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"github.com/gin-gonic/gin"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

func getTlsCfg() *tls.Config {
	srvCert, err := tls.LoadX509KeyPair(serverCertPath, ServerKeyPath)
	if err != nil {
		log.Panicln("load server cert error:", err, "serverCertPath:", serverCertPath, "ServerKeyPath:", ServerKeyPath)
	}

	var caCertPool *x509.CertPool
	if stat, err := os.Stat(caPath); err == nil && stat.IsDir() == false {
		caCrt, err := ioutil.ReadFile(caPath)
		if err != nil {
			log.Panicln("read ca cert error:", err, "caPath:", caPath)
		}

		caCertPool = x509.NewCertPool()
		caCertPool.AppendCertsFromPEM(caCrt)
	}

	// https tls config
	tlsConfig := &tls.Config{
		Certificates:       []tls.Certificate{srvCert},
		ClientCAs:          caCertPool,
		InsecureSkipVerify: ignoreVerify,
	}
	if ignoreVerify {
		tlsConfig.ClientAuth = tls.NoClientCert
	} else {
		tlsConfig.ClientAuth = tls.RequireAndVerifyClientCert
	}

	return tlsConfig
}

func tlsServer() {
	engine := gin.Default()
	engine.Use(gin.Recovery())

	engine.NoRoute(func(c *gin.Context) {
		c.String(200, fmt.Sprintf("access success: url: %s, now: %v", c.Request.URL.String(), time.Now().Format(time.RFC3339)))
	})

	server := http.Server{
		Addr:      listenAddr,
		Handler:   engine,
		TLSConfig: getTlsCfg(),
	}
	if err := server.ListenAndServeTLS("", ""); err != nil {
		log.Printf("listen and serve tls error: %v\n", err)
	}
}

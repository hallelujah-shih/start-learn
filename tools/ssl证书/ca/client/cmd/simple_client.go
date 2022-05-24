package cmd

import (
	"context"
	"crypto/tls"
	"crypto/x509"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

func getTlsCfg() *tls.Config {
	cliCert, err := tls.LoadX509KeyPair(clientCertPath, clientKeyPath)
	if err != nil {
		log.Panicln("load client cert failed:", err, "cert:", clientCertPath, "key:", clientKeyPath)
	}

	var caCertPool *x509.CertPool
	if stat, err := os.Stat(caPath); err == nil && stat.IsDir() == false {
		caCert, err := ioutil.ReadFile(caPath)
		if err != nil {
			log.Panicln("read ca cert failed:", err, "path:", caPath)
		}

		caCertPool = x509.NewCertPool()
		caCertPool.AppendCertsFromPEM(caCert)
	}

	tlsConfig := &tls.Config{
		Certificates:       []tls.Certificate{cliCert},
		RootCAs:            caCertPool,
		InsecureSkipVerify: ignoreVerify,
		ServerName:         "turbo",
		MaxVersion:         tls.VersionTLS12,
	}
	return tlsConfig
}

func reqSvc(ctx context.Context) {
	c := &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: getTlsCfg(),
		},
		Timeout: 60 * time.Second,
	}

	req, err := http.NewRequestWithContext(ctx, "GET", "https://"+serverListen+"/hello", nil)
	if err != nil {
		log.Panicln("new request failed:", err)
	}

	resp, err := c.Do(req)
	if err != nil {
		log.Println("request failed:", err)
		return
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Println("read response body failed:", err)
		return
	}

	log.Println("request success:", resp.Status, "body:", string(body))
}

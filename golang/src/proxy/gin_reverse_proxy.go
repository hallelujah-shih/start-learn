// 代码片段
	u, _ := url.Parse(urlReq.URL)

    // 新的base_path，不同场景使用不同
	c.Request.URL.Path = "/"
	c.Request.Host = u.Host

	trans := &http.Transport{
		TLSClientConfig: &tls.Config{
			KeyLogWriter: os.Stdout,
		},
	}

	proxy := httputil.NewSingleHostReverseProxy(u)
	proxy.Transport = trans
	proxy.ServeHTTP(c.Writer, c.Request)

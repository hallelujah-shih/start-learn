package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"math/rand/v2"
	"os"
	"strings"
	"time"

	"github.com/chromedp/cdproto/network"
	"github.com/chromedp/cdproto/page"
	"github.com/chromedp/chromedp"
)

// Fetcher 结构体封装了页面抓取器的配置和状态
type Fetcher struct {
	maxRetries        int
	retryDelay        time.Duration
	scrollDelay       time.Duration
	stabilityWait     time.Duration
	userAgent         string
	viewport          Viewport
	deviceScaleFactor float64
	locale            string
	timezoneID        string
	ignoreHTTPSErrors bool
}

// Viewport 定义浏览器视口配置
type Viewport struct {
	Width             int64
	Height            int64
	DeviceScaleFactor float64
}

// NewFetcher 创建一个新的页面抓取器实例
func NewFetcher() *Fetcher {
	return &Fetcher{
		maxRetries:    3,
		retryDelay:    2 * time.Second,
		scrollDelay:   80 * time.Millisecond,
		stabilityWait: 3 * time.Second,
		userAgent:     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		viewport: Viewport{
			Width:             1366,
			Height:            768,
			DeviceScaleFactor: 1.0,
		},
		deviceScaleFactor: 1.0,
		locale:            "en-US",
		timezoneID:        "America/Los_Angeles",
		ignoreHTTPSErrors: true,
	}
}

// createBrowserContext 创建浏览器上下文，配置各种选项
func (f *Fetcher) createBrowserContext(ctx context.Context, hostResolverRules string) (context.Context, context.CancelFunc) {
	// 配置浏览器选项
	opts := append(chromedp.DefaultExecAllocatorOptions[:],
		chromedp.Flag("headless", true),
		chromedp.Flag("blink-settings", "imagesEnabled=false"),
		chromedp.Flag("disable-gpu", true),
		chromedp.Flag("no-sandbox", true),
		chromedp.Flag("disable-dev-shm-usage", true),
		chromedp.Flag("disable-features", "IsolateOrigins,site-per-process"),
		chromedp.Flag("user-agent", f.userAgent),
		chromedp.Flag("window-size", fmt.Sprintf("%d,%d", f.viewport.Width, f.viewport.Height)),
		chromedp.Flag("lang", f.locale),
		chromedp.Flag("timezone", f.timezoneID),
		chromedp.Flag("ignore-certificate-errors", f.ignoreHTTPSErrors),
		chromedp.Flag("disable-blink-features", "AutomationControlled"),
	)

	if hostResolverRules != "" {
		opts = append(opts, chromedp.Flag("host-resolver-rules", hostResolverRules))
	}

	allocCtx, allocCancel := chromedp.NewExecAllocator(ctx, opts...)
	ctx, cancel := chromedp.NewContext(allocCtx, chromedp.WithLogf(log.Printf))

	// 注入stealth脚本
	err := f.injectStealthScript(ctx, "stealth.min.js")
	if err != nil {
		log.Printf("注入stealth脚本失败: %v", err)
	}

	return ctx, func() {
		cancel()
		allocCancel()
	}
}

// injectStealthScript 注入stealth.js脚本以隐藏自动化特征
func (f *Fetcher) injectStealthScript(ctx context.Context, stealthPath string) error {
	var script string

	// 优先使用外部stealth.min.js文件
	if stealthPath != "" {
		estealthContent, err := os.ReadFile(stealthPath)
		if err == nil {
			script = string(estealthContent)
		} else {
			log.Printf("无法读取外部stealth脚本文件 %s: %v，使用内嵌脚本", stealthPath, err)
		}

	}

	// 在新文档加载时注入脚本

	err := chromedp.Run(ctx, chromedp.ActionFunc(func(ctx context.Context) error {
		_, err := page.AddScriptToEvaluateOnNewDocument(script).Do(ctx)
		return err
	}))

	if err != nil {
		return fmt.Errorf("注入stealth脚本失败: %v", err)
	}

	return nil
}

// smartScroll 实现智能滚动以触发懒加载
func (f *Fetcher) smartScroll(ctx context.Context) error {
	// 首先检测页面是否真的需要滚动
	var needsScroll bool
	err := chromedp.Run(ctx, chromedp.Evaluate(`
		(() => {
			const docHeight = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
			const viewportHeight = window.innerHeight;
			return docHeight > viewportHeight * 1.5; // 只有当页面高度超过视口1.5倍时才滚动
		})()
	`, &needsScroll))

	if err != nil {
		return fmt.Errorf("检测滚动必要性失败: %v", err)
	}

	if !needsScroll {
		return nil
	}

	// 智能滚动
	err = chromedp.Run(ctx, chromedp.Evaluate(`
		async (args) => {
			const { step, delay } = args;
			const sleep = ms => new Promise(r => setTimeout(r, ms));
			const getDocHeight = () => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);

			let pos = 0;
			let lastHeight = 0;
			let stableCount = 0;
			const maxStableCount = 3; // 连续3次高度不变则停止

			while (stableCount < maxStableCount) {
				const currentHeight = getDocHeight();
				if (currentHeight === lastHeight) {
					stableCount++;
				} else {
					stableCount = 0;
					lastHeight = currentHeight;
				}

				pos = Math.min(pos + step, getDocHeight());
				window.scrollTo(0, pos);
				await sleep(delay);

				// 如果已经到达底部，也停止
			if (pos >= getDocHeight() - window.innerHeight) {
				break;
			}
			}

			// 回到顶部
			window.scrollTo(0, 0);
		}
	`, map[string]interface{}{
		"step":  400,
		"delay": 80, // 80ms

	}))

	if err != nil {
		return fmt.Errorf("智能滚动失败: %v", err)
	}

	return nil
}

// waitForPageStability 等待页面稳定，与Python版本保持一致
func (f *Fetcher) waitForPageStability(ctx context.Context, timeout time.Duration) error {
	startTime := time.Now()
	var prevHTMLLength int
	stableCount := 0
	maxStableCount := 3
	for time.Since(startTime) < timeout {
		var currentHTML string
		err := chromedp.Run(ctx, chromedp.OuterHTML("html", &currentHTML))
		if err != nil {
			// 忽略错误，继续尝试
			time.Sleep(500 * time.Millisecond)
			continue
		}

		currentHTMLLength := len(currentHTML)
		if abs(currentHTMLLength-prevHTMLLength) < 100 {
			stableCount++
			if stableCount >= maxStableCount {
				return nil // 页面稳定
			}
		} else {
			stableCount = 0
		}

		prevHTMLLength = currentHTMLLength
		time.Sleep(500 * time.Millisecond)
	}

	return nil // 超时也认为是稳定
}

// abs 计算绝对值
func abs(x int) int {
	if x < 0 {
		return -x
	}

	return x
}

// fetchPageWithTiming 获取页面内容并记录详细耗时
func (f *Fetcher) fetchPageWithTiming(ctx context.Context, url string, blockedResources []string) (string, error) {
	var html string

	// 设置视口和设备缩放因子
	err := chromedp.Run(ctx,
		chromedp.EmulateViewport(int64(f.viewport.Width), int64(f.viewport.Height)),
	)

	if err != nil {
		return "", fmt.Errorf("设置视口失败: %v", err)
	}

	// 设置常见的 Accept-Language 头
	err = chromedp.Run(ctx, network.SetExtraHTTPHeaders(network.Headers{
		"Accept-Language": "en-US,en;q=0.9",
	}))

	if err != nil {
		log.Printf("设置Accept-Language头失败: %v", err)
	}

	// 导航到目标页面
	gotoStart := time.Now()
	err = chromedp.Run(ctx,
		network.SetBlockedURLs(blockedResources),
		chromedp.Navigate(url),
	)
	if err != nil {
		return "", fmt.Errorf("导航到页面失败: %v", err)
	}

	log.Printf("页面导航耗时: %.2f秒", time.Since(gotoStart).Seconds())

	// 等待DOM内容加载完成
	domStart := time.Now()
	err = chromedp.Run(ctx, chromedp.WaitReady("body", chromedp.ByQuery))
	if err != nil {
		return "", fmt.Errorf("等待DOM内容加载失败: %v", err)
	}

	log.Printf("DOM内容加载等待耗时: %.2f秒", time.Since(domStart).Seconds())

	// 等待页面稳定
	waitStart := time.Now()
	err = f.waitForPageStability(ctx, 10*time.Second)
	if err != nil {
		log.Printf("等待页面稳定失败: %v", err)
	}

	log.Printf("等待状态耗时: %.2f秒", time.Since(waitStart).Seconds())

	// 执行智能滚动
	scrollStart := time.Now()
	err = f.smartScroll(ctx)
	if err != nil {
		log.Printf("智能滚动警告: %v", err)
	}

	log.Printf("智能滚动耗时: %.2f秒", time.Since(scrollStart).Seconds())

	// 再次等待页面稳定
	dynamicWaitStart := time.Now()
	err = f.waitForPageStability(ctx, 5*time.Second)
	if err != nil {
		log.Printf("滚动后等待页面稳定失败: %v", err)
	}

	log.Printf("动态内容等待耗时: %.2f秒", time.Since(dynamicWaitStart).Seconds())

	// 获取页面HTML
	err = chromedp.Run(ctx, chromedp.OuterHTML("html", &html))
	if err != nil {
		return "", fmt.Errorf("获取页面HTML失败: %v", err)
	}

	return html, nil
}

// printResourceStats 输出资源统计信息
func (f *Fetcher) printResourceStats(allowedResources, blockedResources []string) {
	// 创建去重集合
	allowedSet := make(map[string]bool)
	blockedSet := make(map[string]bool)
	for _, resource := range allowedResources {
		allowedSet[resource] = true
	}

	for _, resource := range blockedResources {
		blockedSet[resource] = true
	}

	log.Printf("允许加载的资源类型: %v", getMapKeys(allowedSet))
	log.Printf("阻止加载的资源类型: %v", getMapKeys(blockedSet))
	log.Printf("总共阻止的资源数量: %d", len(blockedResources))
}

// getMapKeys 获取map的所有键
func getMapKeys(m map[string]bool) []string {
	keys := make([]string, 0, len(m))
	for k := range m {
		keys = append(keys, k)
	}

	return keys
}

func (f *Fetcher) FetchWithRetry(url string, hostResolverRules string) (string, []string, error) {
	var lastErr error
	startTime := time.Now()
	log.Printf("开始获取页面: %s", url)
	var blockedResources []string
	var allowedResources []string
	// 定义允许的资源类型
	allowedResourceTypes := map[network.ResourceType]bool{
		network.ResourceTypeDocument:   true,
		network.ResourceTypeStylesheet: true,
		network.ResourceTypeScript:     true,
		network.ResourceTypeXHR:        true,
		network.ResourceTypeFetch:      true,
		network.ResourceTypeWebSocket:  true,
	}

	for attempt := 1; attempt <= f.maxRetries; attempt++ {
		log.Printf("尝试获取页面 (第 %d/%d 次): %s", attempt, f.maxRetries, url)
		// 创建浏览器上下文
		ctx, cancel := f.createBrowserContext(context.Background(), hostResolverRules)
		// 确保在函数退出时清理资源
		defer cancel()
		// 设置超时
		ctx, cancelTimeout := context.WithTimeout(ctx, 60*time.Second)
		defer cancelTimeout()

		// 监听请求事件
		chromedp.ListenTarget(ctx, func(ev interface{}) {
			switch ev := ev.(type) {
			case *network.EventRequestWillBeSent:
				if !allowedResourceTypes[ev.Type] {
					blockedResources = append(blockedResources, ev.Request.URL)
				} else {
					allowedResources = append(allowedResources, ev.Request.URL)
				}
			}
		})

		// 获取页面内容
		html, err := f.fetchPageWithTiming(ctx, url, blockedResources)
		if err == nil {
			getContentTime := time.Now()
			log.Printf("获取页面内容耗时: %.2f秒", getContentTime.Sub(startTime).Seconds())
			log.Printf("页面内容长度: %d 字符", len(html))

			// 输出资源统计信息
			f.printResourceStats(allowedResources, blockedResources)

			var links []string
			err = chromedp.Run(ctx,
				chromedp.ActionFunc(func(ctx context.Context) error {
					var hrefs []string
					// Get both resource links and <a> tag links
					err := chromedp.Evaluate(`
						(() => {
							const resourceLinks = performance.getEntriesByType("resource").map(r => r.name);
							const aTagLinks = Array.from(document.querySelectorAll('a')).map(a => a.href);
							return resourceLinks.concat(aTagLinks);
						})();
					`, &hrefs).Do(ctx)
					if err != nil {
						return fmt.Errorf("提取链接失败: %v", err)
					}
					links = hrefs
					return nil
				}),
			)
			if err != nil {
				log.Printf("提取链接失败: %v", err)
				// Continue with HTML even if link extraction fails
				return html, nil, nil // Return html and empty links, but no error for fetch
			}

			return html, links, nil
		}

		lastErr = err
		log.Printf("获取页面失败 (第 %d/%d 次): %v", attempt, f.maxRetries, err)

		// 如果不是最后一次尝试，等待一段时间后重试
		if attempt < f.maxRetries {
			// 检查是否是特定网络错误，与Python版本一致
			errStr := err.Error()
			if strings.Contains(errStr, "net::ERR_NETWORK_CHANGED") {
				log.Printf("检测到网络变化错误，等待2秒后重试")
				time.Sleep(2 * time.Second)
				continue
			}

			// 指数退避策略，添加随机抖动避免重试风暴
			baseDelay := f.retryDelay * time.Duration(attempt)
			jitter := time.Duration(rand.N(int64(baseDelay / 2)))
			retryDelay := baseDelay + jitter
			log.Printf("等待 %v 后重试...", retryDelay)
			time.Sleep(retryDelay)
		}
	}

	return "", nil, fmt.Errorf("经过 %d 次重试后仍然失败: %v", f.maxRetries, lastErr)
}

// SaveToFile 将HTML内容保存到文件
func (f *Fetcher) SaveToFile(html, filename string) error {
	file, err := os.Create(filename)
	if err != nil {
		return fmt.Errorf("创建文件失败: %v", err)
	}
	defer file.Close()

	_, err = file.WriteString(html)
	if err != nil {
		return fmt.Errorf("写入文件失败: %v", err)
	}

	log.Printf("HTML内容已保存到: %s", filename)
	return nil
}

func main() {
	resolveFlag := flag.String("resolve", "", "自定义host到IP的解析, 格式: 'hostname:ip'")
	outputFileFlag := flag.String("o", "output.html", "输出文件名")

	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "使用方法: %s [options] <URL>\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "示例: %s --resolve=example.com:1.2.3.4 https://example.com\n\n", os.Args[0])
		fmt.Fprintln(os.Stderr, "参数:")
		flag.PrintDefaults()
	}

	flag.Parse()

	if flag.NArg() != 1 {
		flag.Usage()
		os.Exit(1)
	}

	url := flag.Arg(0)
	filename := *outputFileFlag

	var hostResolverRules string
	if *resolveFlag != "" {
		parts := strings.SplitN(*resolveFlag, ":", 2)
		if len(parts) != 2 {
			log.Fatalf("无效的 --resolve 参数格式. 需要 'hostname:ip', 得到: %s", *resolveFlag)
		}
		host := parts[0]
		ip := parts[1]
		hostResolverRules = fmt.Sprintf("MAP %s %s", host, ip)
		log.Printf("应用host解析规则: %s", hostResolverRules)
	}

	// 创建抓取器
	fetcher := NewFetcher()

	// 获取页面内容和链接
	html, links, err := fetcher.FetchWithRetry(url, hostResolverRules)
	if err != nil {
		log.Fatalf("获取页面失败: %v", err)
	}

	// 保存到文件
	if err := fetcher.SaveToFile(html, filename); err != nil {
		log.Fatalf("保存文件失败: %v", err)
	}

	fmt.Printf("成功获取并保存页面内容到: %s\n", filename)

	// 过滤和去重链接
	validLinks := []string{}
	seenLinks := make(map[string]bool)

	for _, link := range links {
		// 过滤无效链接和重复链接
		if (strings.HasPrefix(link, "http://") || strings.HasPrefix(link, "https://")) && !seenLinks[link] {
			validLinks = append(validLinks, link)
			seenLinks[link] = true
		}
	}

	// 打印提取到的有效链接
	if len(validLinks) > 0 {
		fmt.Println("\n--- 提取到的有效链接 ---")
		for _, link := range validLinks {
			fmt.Println(link)
		}
		fmt.Printf("--- 总共提取到 %d 个有效链接 ---\n", len(validLinks))
	} else {
		fmt.Println("\n--- 未提取到任何有效链接 ---")
	}
}

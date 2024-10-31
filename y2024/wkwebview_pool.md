# WKWebViewPool #

> Write a WKWebView pool that meets following requirments:
> 1. Hold a limit number instance of WKWebView.
> 2. If the number of instance exceed the maxmum limit, new instance won't be strong retained, and will be destroyed 
> immediatelly if no one retain it.
> 3. The webview should know the url already successful loaded, when back into the pool, and then if someone asking for instance > with same url, it should returned first.

Any any other funtionality that will optimize the performance.

To create a `WKWebView` pool that meets your requirements, we need to design it to:

1. **Limit the number of instances**: The pool should hold a maximum number of `WKWebView` instances. If the limit is reached, new web views should be weakly retained so they can be deallocated if not used.
2. **Reuse web views with the same URL**: When a `WKWebView` instance is returned to the pool, it should store the URL it successfully loaded. If a future request matches this URL, the pool should return the already-loaded instance to avoid reloading the content.
3. **Performance Optimization**: Preload `WKWebView` instances, stop loading when returning them to the pool, and avoid unnecessary reinitialization.

### Example Implementation:

```swift
import WebKit

class WebViewPool {
    private var availableWebViews: [String: WKWebView] = [:] // Mapping of URL to WebView
    private var activeWebViews: [WKWebView] = [] // Active, in-use WebViews
    private let maxPoolSize: Int
    private let webViewConfiguration: WKWebViewConfiguration

    // Weak reference set to allow deallocation if no one holds a strong reference
    private var weakWebViews: NSHashTable<WKWebView> = NSHashTable.weakObjects()
    
    init(maxPoolSize: Int, configuration: WKWebViewConfiguration = WKWebViewConfiguration()) {
        self.maxPoolSize = maxPoolSize
        self.webViewConfiguration = configuration
    }
    
    func getWebView(for url: URL) -> WKWebView {
        let urlString = url.absoluteString
        
        // Check if a preloaded WebView for the URL is available
        if let cachedWebView = availableWebViews[urlString] {
            availableWebViews.removeValue(forKey: urlString)
            activeWebViews.append(cachedWebView)
            return cachedWebView
        }
        
        // No cached WebView found, so create a new one
        let webView = createNewWebView()
        activeWebViews.append(webView)
        
        // Load the URL in the new WebView
        let request = URLRequest(url: url)
        webView.load(request)
        
        return webView
    }
    
    func returnWebView(_ webView: WKWebView, for url: URL) {
        let urlString = url.absoluteString
        
        // If the pool has reached its limit, don't retain the webView strongly
        if availableWebViews.count < maxPoolSize {
            availableWebViews[urlString] = webView
        } else {
            // Allow WebView to be weakly retained and deallocated if not used
            weakWebViews.add(webView)
        }
        
        // Remove from active list
        if let index = activeWebViews.firstIndex(of: webView) {
            activeWebViews.remove(at: index)
        }
        
        // Cleanup the WebView
        cleanupWebView(webView)
    }
    
    private func createNewWebView() -> WKWebView {
        return WKWebView(frame: .zero, configuration: webViewConfiguration)
    }
    
    private func cleanupWebView(_ webView: WKWebView) {
        webView.stopLoading()
        webView.navigationDelegate = nil
        webView.scrollView.delegate = nil
        webView.removeFromSuperview()
    }
    
    func preloadWebView(for url: URL) {
        if availableWebViews.count < maxPoolSize {
            let webView = createNewWebView()
            let request = URLRequest(url: url)
            webView.load(request)
            availableWebViews[url.absoluteString] = webView
        }
    }
}
```

### Explanation:
1. **Pool Management**: The `WebViewPool` class has a dictionary (`availableWebViews`) to store available `WKWebView` instances mapped by their loaded URLs, and an array (`activeWebViews`) to track currently active instances.
2. **Weak Reference Handling**: When the pool reaches the maximum size, `WKWebView` instances are added to a `NSHashTable` with weak references (`weakWebViews`). This means they will not be retained by the pool and will be deallocated if not held elsewhere.
3. **URL Caching**: Each `WKWebView` knows what URL it successfully loaded. If the URL matches a future request, the cached instance is reused.
4. **Preloading**: `preloadWebView` can be called to pre-load a `WKWebView` for a specific URL, which can speed up future requests for that URL.
5. **Cleanup**: When returning a `WKWebView` to the pool, it is stopped from loading, cleaned up, and ready to be reused, ensuring minimal memory usage.

### Usage Example:

```swift
let webViewPool = WebViewPool(maxPoolSize: 3)

// Get a WebView for a specific URL
let webView = webViewPool.getWebView(for: URL(string: "https://example.com")!)

// After usage, return the WebView to the pool
webViewPool.returnWebView(webView, for: URL(string: "https://example.com")!)
```

### Benefits:
- **Reuse Cached WebViews**: Reusing `WKWebView` for the same URL prevents reloading, reducing load time.
- **Memory Management**: Weakly retaining `WKWebView` instances when the pool is full prevents excessive memory usage.
- **Preloading**: Improve user experience by preloading web views for anticipated content.

This implementation should optimize your `WKWebView` usage, enhancing performance and resource management.
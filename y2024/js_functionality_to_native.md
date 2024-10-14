# JS bridge module for WKWebView #

```
 want provide functionality from iOS native to webpage run in a WebViewController, the functionality is grouped to module, like "base", "businessA", "businessB", write the Swift code to do that.
```

To provide functionality from an iOS native app to a webpage running in a `WKWebView`, you can use the `WKScriptMessageHandler` protocol to communicate between the native code and the JavaScript code in the web view. Here's a structured way to implement this functionality grouped into modules like "base", "businessA", and "businessB".

### Step 1: Setup Your Project

1. Make sure you import the `WebKit` framework in your project.
2. Create a new Swift file for each module: `BaseModule.swift`, `BusinessAModule.swift`, and `BusinessBModule.swift`.

### Step 2: Create a Base Module

This module can handle common functionalities and register the message handlers.

```swift
import WebKit

class BaseModule: NSObject, WKScriptMessageHandler {
    
    // Function to register the message handlers
    func registerHandlers(for webView: WKWebView) {
        webView.configuration.userContentController.add(self, name: "base")
        webView.configuration.userContentController.add(self, name: "businessA")
        webView.configuration.userContentController.add(self, name: "businessB")
    }
    
    // Handle messages from the JavaScript side
    func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        switch message.name {
        case "base":
            handleBaseFunctionality(message.body)
        case "businessA":
            handleBusinessAFunctionality(message.body)
        case "businessB":
            handleBusinessBFunctionality(message.body)
        default:
            break
        }
    }
    
    // Base functionality
    private func handleBaseFunctionality(_ body: Any) {
        // Implement base functionality
        print("Base module received: \(body)")
    }

    // Business A functionality
    private func handleBusinessAFunctionality(_ body: Any) {
        // Implement business A functionality
        print("Business A module received: \(body)")
    }

    // Business B functionality
    private func handleBusinessBFunctionality(_ body: Any) {
        // Implement business B functionality
        print("Business B module received: \(body)")
    }
}
```

### Step 3: Create Business Modules

For each business module, you can create specific functionalities. Here’s an example for `BusinessAModule`:

```swift
import Foundation

class BusinessAModule {
    // Business A specific functions can go here
    func performAction() {
        // Action implementation
        print("Performing action from Business A module")
    }
}
```

And similarly, you can create `BusinessBModule.swift`:

```swift
import Foundation

class BusinessBModule {
    // Business B specific functions can go here
    func performAction() {
        // Action implementation
        print("Performing action from Business B module")
    }
}
```

### Step 4: Set Up Your Web View Controller

In your `WebViewController`, you will need to instantiate the base module and register it with the web view.

```swift
import UIKit
import WebKit

class WebViewController: UIViewController {
    var webView: WKWebView!
    let baseModule = BaseModule()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Initialize and configure the WKWebView
        webView = WKWebView()
        view.addSubview(webView)
        webView.frame = view.bounds

        // Register message handlers
        baseModule.registerHandlers(for: webView)

        // Load a local HTML file or a remote URL
        if let url = URL(string: "https://your-webpage-url.com") {
            webView.load(URLRequest(url: url))
        }
    }
}
```

### Step 5: JavaScript Side

To send messages from your webpage to the iOS native modules, you can use the following JavaScript code:

```javascript
// Sending a message to the base module
window.webkit.messageHandlers.base.postMessage("Hello from the webpage!");

// Sending a message to business A module
window.webkit.messageHandlers.businessA.postMessage({ action: "performAction", data: "Some data for A" });

// Sending a message to business B module
window.webkit.messageHandlers.businessB.postMessage({ action: "performAction", data: "Some data for B" });
```

### Summary

- **BaseModule**: Handles registration and generic functionalities.
- **BusinessAModule** and **BusinessBModule**: Specific functionalities can be implemented here.
- **WebViewController**: Initializes the `WKWebView`, registers modules, and loads a webpage.
- **JavaScript**: Sends messages to iOS native modules through `window.webkit.messageHandlers`.

### Additional Notes
- Make sure to handle errors and edge cases in your actual implementation.
- You can expand the functionality of each module based on your specific requirements.
- Consider thread safety and data synchronization if your modules will access shared resources.
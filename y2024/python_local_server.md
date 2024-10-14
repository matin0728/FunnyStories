# Python local server #

> Write a python script to run a simple local HTTP service to handle POST request, one 
> endpoint serve HTTPS request, and another do not require HTTPS.

To set up a simple local HTTP service in Python that can handle both HTTPS and non-HTTPS POST requests, you can use the `http.server` module from the standard library along with `ssl` to secure one of the endpoints. Here's a basic example:

1. **Create the HTTP Server**:
   - Set up two different servers: one for HTTP and one for HTTPS.
   - Use `http.server.BaseHTTPRequestHandler` to handle POST requests.
   
2. **Generate SSL Certificates**:
   - You'll need an SSL certificate and key. For local testing, you can generate a self-signed certificate using the following command:
     ```bash
     openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
     ```

Here's the Python script:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(f"Received POST request: {post_data.decode('utf-8')}")
        
        # Send a simple response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"POST request processed successfully")

def run_http_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}")
    httpd.serve_forever()

def run_https_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    # Set up SSL
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   server_side=True,
                                   certfile="server.pem",
                                   ssl_version=ssl.PROTOCOL_TLS)
    
    print(f"Starting HTTPS server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    from threading import Thread
    
    # Start HTTP server
    http_thread = Thread(target=run_http_server)
    http_thread.daemon = True
    http_thread.start()
    
    # Start HTTPS server
    https_thread = Thread(target=run_https_server)
    https_thread.daemon = True
    https_thread.start()
    
    # Keep the main thread running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nServers are shutting down.")
```

### Explanation:

1. **`SimpleHTTPRequestHandler`**:
   - Handles POST requests and simply reads the data sent in the body, printing it to the console.
   - Responds with a simple message to confirm the POST request was processed.

2. **`run_http_server`**:
   - Creates and starts an HTTP server on port `8080`.

3. **`run_https_server`**:
   - Creates and starts an HTTPS server on port `8443`, using the SSL certificate `server.pem`.
   - Requires the generated certificate for local testing.

4. **Threading**:
   - The servers run on separate threads, allowing them to handle requests concurrently.

### Running the Script:
1. Save the script to a file, e.g., `simple_http_service.py`.
2. Ensure you have generated `server.pem` using `openssl`.
3. Run the script:
   ```bash
   python simple_http_service.py
   ```
4. You can now send POST requests to:
   - `http://localhost:8080` (non-HTTPS)
   - `https://localhost:8443` (HTTPS)

This should help you test handling both HTTP and HTTPS requests locally.


The error `"'ssl' has no attribute 'wrap_socket'"` suggests that there might be an issue with the SSL module not having the expected attribute or function. This could be due to a few reasons, such as a Python version incompatibility or an issue with the environment. 

To address this issue, you can try the following:

### Solution 1: Update to Use `SSLContext`

Instead of using `ssl.wrap_socket`, which is deprecated in some Python versions, you can create an `SSLContext` and use `SSLContext.wrap_socket`. Here's an updated version of the script:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(f"Received POST request: {post_data.decode('utf-8')}")
        
        # Send a simple response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"POST request processed successfully")

def run_http_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}")
    httpd.serve_forever()

def run_https_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    # Create an SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="server.pem", keyfile="server.pem")
    
    # Wrap the socket with SSL context
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
    
    print(f"Starting HTTPS server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    from threading import Thread
    
    # Start HTTP server
    http_thread = Thread(target=run_http_server)
    http_thread.daemon = True
    http_thread.start()
    
    # Start HTTPS server
    https_thread = Thread(target=run_https_server)
    https_thread.daemon = True
    https_thread.start()
    
    # Keep the main thread running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nServers are shutting down.")
```

### Explanation:

1. **`ssl.SSLContext`**:
   - Create an `SSLContext` object using `ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)`.
   - Load the certificate and key using `ssl_context.load_cert_chain`.
   - Replace the old `ssl.wrap_socket` call with `ssl_context.wrap_socket`.

2. **Why This Works**:
   - This approach is more robust and compatible with modern Python versions.
   - Using `SSLContext` is recommended for better control over the SSL parameters.

### Verify SSL Certificate

Ensure that your SSL certificate (`server.pem`) is valid. If you haven't already, you can generate it using:
```bash
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
```

This solution should solve the issue and allow your HTTPS server to function correctly.
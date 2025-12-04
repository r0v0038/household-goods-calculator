#!/usr/bin/env python3
"""Simple reverse proxy server to bypass corporate proxy restrictions."""

import http.server
import socketserver
import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qs
import json

PROXY_PORT = 8080
TARGET_URL = "http://127.0.0.1:5000"


class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler that proxies requests to the Flask app."""

    def do_GET(self):
        """Handle GET requests by proxying to the Flask app."""
        try:
            # Build the target URL
            target = f"{TARGET_URL}{self.path}"
            
            # Forward the request
            req = urllib.request.Request(target)
            
            # Copy headers
            for header in ['User-Agent', 'Accept', 'Accept-Language', 'Accept-Encoding']:
                if header in self.headers:
                    req.add_header(header, self.headers[header])
            
            # Get response from Flask app
            response = urllib.request.urlopen(req, timeout=10)
            
            # Send response back to client
            self.send_response(response.status)
            
            # Copy response headers
            for header, value in response.getheaders():
                if header.lower() not in ['server', 'date']:
                    self.send_header(header, value)
            
            self.end_headers()
            
            # Send response body
            self.wfile.write(response.read())
            
        except urllib.error.URLError as e:
            self.send_error(502, f"Bad Gateway: Could not connect to Flask app - {e}")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {e}")

    def do_POST(self):
        """Handle POST requests by proxying to the Flask app."""
        try:
            # Get content length
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Build the target URL
            target = f"{TARGET_URL}{self.path}"
            
            # Forward the request
            req = urllib.request.Request(
                target,
                data=post_data,
                method='POST'
            )
            
            # Copy headers
            for header in ['Content-Type', 'User-Agent', 'Accept']:
                if header in self.headers:
                    req.add_header(header, self.headers[header])
            
            # Get response from Flask app
            response = urllib.request.urlopen(req, timeout=10)
            
            # Send response back to client
            self.send_response(response.status)
            
            # Copy response headers
            for header, value in response.getheaders():
                if header.lower() not in ['server', 'date']:
                    self.send_header(header, value)
            
            self.end_headers()
            
            # Send response body
            self.wfile.write(response.read())
            
        except urllib.error.URLError as e:
            self.send_error(502, f"Bad Gateway: Could not connect to Flask app - {e}")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {e}")

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[PROXY] {self.address_string()} - {format % args}")


def run_proxy():
    """Start the proxy server."""
    print("\n" + "="*70)
    print("  Household Goods Calculator - Proxy Server")
    print("="*70)
    print(f"\n[*] Proxy server starting on port {PROXY_PORT}...")
    print(f"[*] Forwarding requests to: {TARGET_URL}")
    print("\n" + "="*70)
    print("\n[WEB] Access the calculator at:")
    print(f"      http://localhost:{PROXY_PORT}")
    print(f"      http://127.0.0.1:{PROXY_PORT}")
    print(f"      http://10.97.112.102:{PROXY_PORT}")
    print("\n[!!!] Note: Make sure the Flask app is running on port 5000")
    print("\n" + "="*70)
    print("\nPress Ctrl+C to stop the proxy server\n")
    
    try:
        with socketserver.TCPServer(("", PROXY_PORT), ProxyHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n[STOP] Proxy server stopped.")
    except OSError as e:
        if "address already in use" in str(e).lower():
            print(f"\n[ERROR] Port {PROXY_PORT} is already in use.")
            print("        Try changing PROXY_PORT in this script or stop the other service.")
        else:
            print(f"\n[ERROR] {e}")


if __name__ == '__main__':
    run_proxy()

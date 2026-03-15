#!/usr/bin/env python3
"""Test script to verify the server works correctly"""
import os
import sys
import time
import threading
import http.server
import socketserver

# Start server in a thread
def start_server():
    os.chdir("c:/Eren/vscode/open-anamnesis/examples/python_learning_path/build")
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = '/index.html'
            return super().do_GET()
        
        def log_message(self, format, *args):
            pass
    
    with socketserver.TCPServer(("127.0.0.1", 5000), Handler) as httpd:
        print("✓ Server started on http://127.0.0.1:5000")
        print("  Open this URL in your browser")
        print("  Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✗ Server stopped")

if __name__ == "__main__":
    start_server()

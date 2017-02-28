#!/usr/bin/env python3.5
from td2 import SearchEngine
from http.server import BaseHTTPRequestHandler, HTTPServer
from collections import defaultdict
import json


def tree(): return defaultdict(tree)


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        content = tree()
        content['foo'] = 'bar'
        self.wfile.write(bytes(json.dumps(content), encoding="utf-8"))


def run():
    httpd = HTTPServer(('localhost', 8765), AppHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
#!/usr/bin/env python3.5
from os import listdir
from os.path import join, isfile

from td2 import SearchEngine
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from collections import defaultdict
import json


def tree(): return defaultdict(tree)

COURSE_PATH = '02/sample'
FILES = [join(COURSE_PATH, f) for f in listdir(COURSE_PATH) if isfile(join(COURSE_PATH, f))]


class AppHandler(BaseHTTPRequestHandler):
    search_engine = SearchEngine(FILES)

    def do_GET(self):
        query = urlparse(self.path).query
        args = dict(i.split('=') for i in query.split('&'))
        if 'sort' not in args:
            args['sort'] = True
        if 'length' not in args:
            args['length'] = 10
        print(args)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        body = tree()
        search_result = self.search_engine.search(args['acronym'], args['sort'])[:args['length']]
        body['data'] = {acr:{'val': value, 'desc': self.search_engine.files[acr].original_content}
                        for acr, value in search_result}
        self.wfile.write(bytes(json.dumps(body), encoding="utf-8"))


def run():
    httpd = HTTPServer(('localhost', 8765), AppHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
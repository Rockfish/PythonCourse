"""
Sample hander built by subclassing Python's BaseHTTPRequestHandler
"""

import sys

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        body = self.get_body()
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        print(self.raw_requestline)
        print("do_Get - done")

    def do_POST(self):
        body = self.get_body()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        self.print_context()
        print("do_POST - done")

    def print_context(self):
        print(self.request)
        print("Client address:", self.client_address)
        print(self.raw_requestline)
        print(self.command)
        print(self.request_version)
        print(self.path)
        print(self.headers)
        self.parse_query(self.path)
        print(self.pathonly)
        print(self.query.split('&'))
        print(self.extra)
        data = self.rfile.readlines()
        print("body: ", data)

    def parse_query(self, raw_path):
        data = raw_path.split('?', 1)
        self.pathonly = data[0]
        self.query = ''
        self.extra = ''
        if len(data) > 1:
            data = data[1].split('#', 1)
            self.query = data[0]
            if len(data) > 1:
                self.extra = data[1]

    def get_body(self):
        html = "<html><body><h1>Hello World!</h1></body></html>"
        enc = sys.getfilesystemencoding()
        encoded = html.encode(enc)
        return encoded



def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def run2():
    httpd = HTTPServer(('', 8000), MyHandler)
    httpd.serve_forever()

# run(HTTPServer, MyHandler)
run2()


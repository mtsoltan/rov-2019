from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, ParseResult
from threading import Thread
from typing import Callable, Union, Tuple, Optional
import os
import sys
import time

Response = Union[Tuple[int, str], int, str]

STATIC_DIR = os.path.join('..', 'static')
ERROR = 'error.html'
TEMPLATE_DIR = os.path.join('..', 'templates')
TEMPLATE_EXT = '.html'


class ExtendedServerHandler(ThreadingMixIn, BaseHTTPRequestHandler):
    def __init__(self, *args):
        self.path = ''
        self.status_dict = {
            400: 'Bad Request',
            403: 'Forbidden',
            404: 'Not Found',
        }
        super().__init__(*args)

    def error(self, status: int, text: str = None):
        if text is None:
            text = self.status_dict[status]
        if self.headers['X-Requested-With'] == 'XMLHttpRequest':
            content = text
        else:
            f = open(self.normalize(TEMPLATE_DIR, ERROR))
            content = f.read().format(status=status, text=text)
            f.close()
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(content, 'UTF-8'))

    @staticmethod
    def check_mime(path: str) -> Optional[str]:
        mime = None
        if path.endswith(".html"):
            mime = 'text/html'
        if path.endswith(".jpg"):
            mime = 'image/jpg'
        if path.endswith(".png"):
            mime = 'image/png'
        if path.endswith(".js"):
            mime = 'application/javascript'
        if path.endswith(".css"):
            mime = 'text/css'
        if path.endswith(".txt"):
            mime = 'text/plain'
        if path.endswith(".json") or path.endswith(".map"):
            mime = 'application/json'
        if path.endswith(".svg"):
            mime = 'image/svg+xml'
        return mime

    @staticmethod
    def normalize(*paths: str) -> str:
        return os.path.normpath(os.path.join(sys.path[0], *paths))

    def log_message(self, form, *args):
        return

    def do_GET(self):
        if self.path == "/":
            self.path = "/index"
        if self.path.startswith('/'):
            self.path = self.path[1:]

        switchable: ParseResult = urlparse(self.path)  # Has path, query, fragment.
        try:
            mime = self.check_mime(switchable.path)
            if mime:
                f = open(self.normalize(STATIC_DIR, switchable.path))
                content = f.read()
            else:
                f = open(self.normalize(TEMPLATE_DIR, switchable.path + TEMPLATE_EXT))
                content = f.read().format(time=time.time())
                mime = 'text/html'
            self.send_response(200)
            self.send_header('Content-type', mime)
            self.end_headers()
            self.wfile.write(bytes(content, 'UTF-8'))
            f.close()
            return
        except IOError:
            self.error(404, 'Could not find the file you requested to open.')
            return

    def do_POST(self):
        if self.path == "/":
            self.path = "/index"
        if self.path.startswith('/'):
            self.path = self.path[1:]
        switchable: ParseResult = urlparse(self.path)  # Has path, query, fragment.
        body = self.rfile.read(int(self.headers.get('Content-Length')))
        response = self.server.callback({
            'urlobj': switchable,
            'body': body,
        })
        if isinstance(response, int):
            response = (response, None)
        if isinstance(response, Tuple):
            self.error(*response)
            return
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(response, 'UTF-8'))
        return


class ExtendedServer(ThreadingMixIn, HTTPServer):
    def __init__(self, *args):
        self.callback = lambda request: ()
        super().__init__(*args)

    def set_callback(self, callback: Callable):
        self.callback = callback


class WebServer(ThreadingMixIn):
    def __init__(self, url: str = '', port: int = 8000):
        self.URL = url
        self.port = port
        self.httpd = None
        self.server = ExtendedServer((self.URL, self.port), ExtendedServerHandler)
        self.rules = {}
        self.server.set_callback(self.loop_on_rules)
        self.server_thread = None

    def run(self):
        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.daemon = False
        self.server_thread.start()

    def close(self):
        self.server.server_close()

    def add_rule(self, name, callback: Callable):
        self.rules[name] = callback

    def loop_on_rules(self, request: dict) -> Response:
        for key in self.rules:
            if request['urlobj'].path == key:
                return self.rules[key](request['body'].decode("utf-8"))
        return 400, 'Request not in list of valid requests'

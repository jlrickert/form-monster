from http.server import HTTPServer, BaseHTTPRequestHandler

from .abstract_view import AbstractView

class HTTPRequestHandler(BaseHTTPRequestHandler):
    pass


class Web(AbstractView):
    def __init__(self, form):
        super().__init__(form)

    def run(self, addr=("127.0.0.1", 0)):
        # httpd = HTTPServer(addr, HTTPRequestHandler)
        httpd = HTTPServer(addr, HTTPRequestHandler)
        httpd.serve_forever()

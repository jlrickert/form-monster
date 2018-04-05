import logging
import webbrowser
from functools import partial
from http.server import HTTPServer, BaseHTTPRequestHandler, HTTPStatus

from .abstract_view import AbstractView

log = logging.getLogger(__name__)

DEFAULT_MESSAGE = """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Form Monster</title>
    </head>
    <body>
        <code>{}</code>
    </body>
</html>
"""


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, form, *args):
        self.form = form
        super().__init__(*args)

    def do_GET(self):
        form = str(self.form).replace("<", "&lt").replace(">", "&gt")
        content = DEFAULT_MESSAGE.format(form)
        body = content.encode("UTF-8", "replace")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", int(len(body)))
        self.end_headers()
        self.wfile.write(body)


def makeRequest(form):
    def handler(*args):
        return HTTPRequestHandler(form, *args)

    return handler


class Web(AbstractView):
    def __init__(self, form, options={"browser": True}):
        super().__init__(form)

    def run(self, addr=("127.0.0.1", 0)):
        # httpd = HTTPServer(addr, HTTPRequestHandler)
        handler = makeRequest(self.form)
        httpd = HTTPServer(addr, handler)
        log.info("Listening on port %d" % httpd.server_port)
        webbrowser.open_new_tab("http://localhost:%d" % httpd.server_port)
        httpd.serve_forever()

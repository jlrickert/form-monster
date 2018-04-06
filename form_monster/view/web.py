import logging
import webbrowser
from functools import partial
import socket

from aiohttp import web

from .base_view import BaseView

log = logging.getLogger(__name__)

async def open_browser(app):
    app.port
    pass

app = web.Application()
app.on_startup.append(open_browser)

def unused_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

class Web(BaseView):
    def __init__(self, form, options={"browser": True}):
        super().__init__(form)

    def run(self, host="127.0.0.1", port=0):
        if port == 0:
            port = unused_port()
        web.run_app(app, host=host, port=port)
        print(x)
        # httpd = HTTPServer(addr, HTTPRequestHandler)
        # handler = makeRequest(self.form)
        # httpd = HTTPServer(addr, handler)
        # log.info("Listening on port %d" % httpd.server_port)
        # webbrowser.open_new_tab("http://localhost:%d" % httpd.server_port)
        # httpd.serve_forever()

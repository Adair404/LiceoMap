"""Serve only web/, never the repository or .local secrets."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

WEB = Path(__file__).resolve().parents[1] / 'web'


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        if self.path.split('?')[0] in ('/', '/index.html') and '--test' in sys.argv:
            data = (WEB / 'index.html').read_text(encoding='utf-8').replace('http://127.0.0.1:8000/', 'http://127.0.0.1:8001/').encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            super().do_GET()


if __name__ == '__main__':
    ThreadingHTTPServer.request_queue_size = 128
    print('Web local: http://127.0.0.1:5500/ · API ' + ('de pruebas' if '--test' in sys.argv else 'de desarrollo'), flush=True)
    ThreadingHTTPServer(('127.0.0.1',5500), partial(Handler,directory=str(WEB))).serve_forever()

#!/usr/bin/env python3

try:
    import os
    import socket
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
except Exception as e:
    print(f'[ERROR] {e}')

COLOR= os.environ.get('COLOR')
print(f'COLOR is {COLOR}')
COVEO_HOST = os.environ.get('COVEO_HOST')
print(f'COVEO_HOST is {COVEO_HOST}')
PORT = int(os.environ.get('PORT', '8080'))
print(f'PORT is {PORT}')

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/ping':
            self.send_response(200)
            self.end_headers()
            return

        try:
            print('Trying to hit ' + COVEO_HOST.split(':')[0])
            print(socket.gethostbyname(COVEO_HOST.split(':')[0]))
            req = Request(f'http://{COVEO_HOST}')
            res = urlopen(req)
            resstr = res.read()
            resptxt = COLOR + " " + str(resstr,'UTF-8')
            print(resptxt)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(resptxt, 'UTF-8'))

        except HTTPError as e:
            print(f'[ERROR] {e}')
            self.send_error(e.code, e.reason)

        except Exception as e:
            print(f'[ERROR] {e}')
            self.send_error(500, b'Something really bad happened')

print('starting server...')
httpd = HTTPServer(('', PORT), Handler)
print('running server...')
httpd.serve_forever()

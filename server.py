import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from fuzzy_burnout import compute_burnout


class BurnoutHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/static/index.html'
            return super().do_GET()

        if self.path.startswith('/hitung'):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            try:
                beban   = float(params.get('beban',   [50])[0])
                tidur   = float(params.get('tidur',   [50])[0])
                sosial  = float(params.get('sosial',  [50])[0])
                tekanan = float(params.get('tekanan', [50])[0])
                result  = compute_burnout(beban, tidur, sosial, tekanan)
                body    = json.dumps(result, ensure_ascii=False).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        return super().do_GET()


if __name__ == '__main__':
    import os, sys
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    httpd = HTTPServer(('0.0.0.0', port), BurnoutHandler)
    print(f"Sistem Fuzzy Burnout berjalan di http://localhost:{port}")
    httpd.serve_forever()

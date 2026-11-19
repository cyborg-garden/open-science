from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import sys
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
handler = partial(SimpleHTTPRequestHandler, directory='/opt/data/open-science/docs')
print(f'Serving review QA at http://127.0.0.1:{port}', flush=True)
ThreadingHTTPServer(('127.0.0.1', port), handler).serve_forever()

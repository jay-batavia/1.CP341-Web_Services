from http_parser import parser
from wsgiref.simple_server import make_server



httpd = make_server('', 8000, parser.respond_all)
print("Serving on port 8000...")

# Serve until process is killed
httpd.serve_forever()
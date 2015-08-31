from inventory_server import WarehouseApp
from wsgiref.simple_server import make_server

encoding = 'utf-8'
port = 8000
my_obj = WarehouseApp()

def generic_server(environ, start_response):
    response_text = my_obj.parse_request( environ )
    status = response_text['status'] # HTTP Status
    headers = [('Content-type', 'text/plain; charset='+encoding)] # HTTP Headers
    start_response(status, headers)

    # The returned object is going to be printed
    return [ response_text['text'].encode( encoding ) ]

httpd = make_server( '', port, generic_server )
print( "Serving on port %d..." % port )

# Serve until process is killed
httpd.serve_forever()
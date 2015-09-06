from inventory_file import WarehouseApp_Impl_file
from inventory_db import WarehouseApp_Impl_db
from wsgiref.simple_server import make_server
import sys

encoding = 'utf-8'
port = 8000
file_obj = WarehouseApp_Impl_file()
db_obj = WarehouseApp_Impl_db()

def file_server(environ, start_response):
    response_text = file_obj.parse_request( environ )
    status = response_text['status'] # HTTP Status
    headers = [('Content-type', 'text/plain; charset='+encoding)] # HTTP Headers
    start_response(status, headers)

    # The returned object is going to be printed
    return [ response_text['text'].encode( encoding ) ]


def database_server(environ, start_response):
	response_text = db_obj.parse_request( environ )
	status = response_text['status']
	headers=[('Content-type', 'text/plain; charset='+encoding)]
	start_response(status, headers)

	return[ response_text['text'].encode( encoding )]

try:
	if sys.argv[1] == "db":
		httpd = make_server( '', port, database_server )

	elif sys.argv[1] == "file":
		httpd = make_server('', port, file_server )
	
except:
	httpd = make_server('', port, file_server)

print( "Serving on port %d..." % port )

# Serve until process is killed
httpd.serve_forever()
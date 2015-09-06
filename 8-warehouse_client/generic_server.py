#!/usr/bin/env python3

import sys
from wsgiref.simple_server import make_server
import warehouse_dispatcher
import storage_file
import storage_db

encoding   = 'utf-8'
port       = 8000
if len( sys.argv ) < 2:
    print( 'Usage: generic_server ( file or db )' )
    sys.exit( 1 )
if sys.argv[1] == 'file':
    storage = storage_file.StorageFile()
elif sys.argv[1] == 'db':
    storage = storage_db.StorageDB()
else:
    print( 'Usage: generic_server ( file or db )' )
    sys.exit( 1 )

dispatcher = warehouse_dispatcher.WarehouseDispatcher( storage )

def generic_server( environ, start_response ):
    try:
        ( status, response_text ) = dispatcher.dispatch( environ )
    except Exception as e:
        print("IN THE EXCEPTION!")
        print( e )
        status = '500 Internal Server Error'
        response_text = 'Inventory server exploded'

    headers = [ ( 'Content-type', 'text/plain; charset=' + encoding ) ]
    start_response( status, headers )

    return [ response_text.encode( encoding ) ]

httpd = make_server( '', port, generic_server )
print( "Serving on port %d..." % port )

# Serve until process is killed
httpd.serve_forever()
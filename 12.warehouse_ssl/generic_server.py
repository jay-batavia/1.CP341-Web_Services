#!/usr/bin/env python3
import base64
import sys
from wsgiref.simple_server import make_server
import warehouse_dispatcher
import storage_file
import storage_db

encoding   = 'utf-8'
port       = 8000

auth_db = {'jay': 'test',  }

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

def authenticate(credentials):
    authenticated = False

    up_b64_bytes = credentials.encode( 'ascii' )
    user_pass_bytes = base64.decodestring( up_b64_bytes )
    user_pass_str = user_pass_bytes.decode( 'utf-8' )
    user_pass_parts = user_pass_str.split( ':' )
    username = user_pass_parts[0]
    password = user_pass_parts[1]
    if auth_db[username] == password:
        authenticated = True
    return authenticated




def generic_server( environ, start_response ):
    (status, response_text) = ('600 Internal Server Error', 'Dusty Server Rooms')
    
    if environ[ 'REQUEST_METHOD' ] == 'GET' and 'HTTP_AUTHORIZATION' in environ:
        auth_req = environ[ 'HTTP_AUTHORIZATION' ]
        auth_parts = auth_req.split( ' ' )
        if auth_parts[0] == 'Basic':
            authenticated = authenticate(auth_parts[1])
            if authenticated:
                try:
                    (status, response_text) = dispatcher.dispatch(environ)

                except Exception as e:
                    print( e )
                    status = '500 Internal Server Error'
                    response_text = 'Server rooms are dusty.'
            else:
                status = '401 Unauthorized'
                response_text = ''
        else:
            status = '400 Bad Request'
            response_text = ""

    elif environ[ 'REQUEST_METHOD' ] == 'GET' and 'HTTP_AUTHORIZATION' not in environ:
        (status, response_text) = ('403 Forbidden', 'Need authorization')
   
    else:
        try:
            ( status, response_text ) = dispatcher.dispatch( environ )
        except Exception as e:
            print("IN THE EXCEPTION!")
            print( e )
            status = '500 Internal Server Error'
            response_text = 'Inventory server exploded'

    headers = [ ( 'Content-type', 'text/plain; charset=' + encoding ) ]
    print (headers)
    print(status)
    start_response( status, headers )

    return [ response_text.encode( encoding ) ]

httpd = make_server( '', port, generic_server )
print( "Serving on port %d..." % port )

# Serve until process is killed
httpd.serve_forever()
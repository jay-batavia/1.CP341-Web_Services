#!/usr/bin/env python3
import pprint
import sys
import json
from wsgiref.simple_server import make_server
import twitter_client
import nyt_client

encoding   = 'utf-8'
port       = 8100
NYT_URI = 'http://api.nytimes.com/svc/'
def getBody( environ ):
    if 'CONTENT_LENGTH' in environ and environ[ 'CONTENT_LENGTH' ] != '':
        print('CONTENT LENGTH: ', environ['CONTENT_LENGTH'] )
        try:
            cl = int( environ[ 'CONTENT_LENGTH' ] )
        except:
            return ( '500 Internal Server Error', '' )
        return environ[ 'wsgi.input' ].read( cl ).decode( 'utf-8' )
    else:
        return ""

def dispatch( environ ):
    try:
        http_method  = environ[ 'REQUEST_METHOD' ]
        url_path     = environ[ 'PATH_INFO' ]
        query_string = environ[ 'QUERY_STRING' ]
        path_parts   = url_path.split( '/' )
        
        if len(path_parts) == 3 and path_parts[1] == 'search':
            responses = {}
            
            twitter_response = twitter_client.getQueryTweets(path_parts[2])

            nyt_recent = nyt_client.getQueryRecent(path_parts[2])

            nyt_popular = nyt_client.getQueryPopular()

            nyt_wire = nyt_client.getTimesWire()

            responses['twitter'] = twitter_response
            responses['nyt_recent'] = nyt_recent
            responses['nyt_popular'] = nyt_popular
            responses['nyt_wire'] = nyt_wire
            rv = ('200 OK', '%s' %json.dumps(responses))

        

    except Exception as e:
        print("dispatch error: ", e)
        return("500 INTERNAL","something went wrong")

    return rv



def generic_server( environ, start_response ):
    try:
        ( status, response_text ) = dispatch( environ )
    except Exception as e:
        print( 'server error: ', e )
        status = '500 Internal Server Error'
        response_text = 'Inventory server exploded'

    headers = [ ( 'Content-type', 'text/plain; charset=' + encoding ), ('Access-Control-Allow-Origin', '*') ]
    start_response( status, headers )

    return [ response_text.encode( encoding ) ]

httpd = make_server( '', port, generic_server )
print( "Serving on port %d..." % port )

# Serve until process is killed
httpd.serve_forever()
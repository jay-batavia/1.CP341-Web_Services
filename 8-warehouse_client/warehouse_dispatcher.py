from urllib import parse
import json
import sys


def getBody( environ ):
    if 'CONTENT_LENGTH' in environ and environ[ 'CONTENT_LENGTH' ] != '':
        try:
            cl = int( environ[ 'CONTENT_LENGTH' ] )
        except:
            return ( '500 Internal Server Error', '' )
        return environ[ 'wsgi.input' ].read( cl ).decode( 'utf-8' )
    else:
        return ""


class WarehouseDispatcher:
    storage = None

    def __init__( self, storage ):
        self.storage = storage

    def addItem(self, update):

        for i in range(len(update['item_name'])):
            item_name = str.lower(update['item_name'][i])
            try:
                item_quantity = int(update['item_quantity'][i])
            except:
                return ( '400 Bad Request', 'Quantity not an integer' )

            if(item_quantity<0):
                return ( '400 Bad Request', 'Negative quantity' )
                
            self.storage.addItem( item_name, item_quantity)

        return ('201 Created', '')

    def getBoundedItems(self, query_params):
        try:    
            if "lower_bound" in query_params and "upper_bound" in query_params:
                upper_bound = int(query_params["upper_bound"][0])
                lower_bound = int(query_params["lower_bound"][0])
            elif "upper_bound" in query_params:
                upper_bound = int(query_params["upper_bound"][0])
                lower_bound = 0
            elif "lower_bound" in query_params:
                lower_bound = int(query_params["lower_bound"][0])
                upper_bound = sys.maxsize
        except:
            return ('400 Bad Request', ' The bounds must be integers. ')

        bounded_items = self.storage.getBoundedItems( upper_bound, lower_bound )

        if bounded_items is None:
            return( '404 NOT FOUND', 'No items found within the given range.' )
        else:
            return ('200 OK', '%s' % json.dumps(dict(bounded_items)) )

    def updateQty(self, item_name, update):
        try:
            update_int = int(update['update_quantity'][0])
        except:
            return ( '400 Bad Request', 'Parameter must be an integer' )
        original_quantity = self.storage.getItemQty([item_name])
        if original_quantity is None:
            return( '404 NOT FOUND', '' )
        else:
            original_number = original_quantity[item_name]
        new_quantity = original_number + update_int
        if new_quantity < 0:
            return( '400 Bad Request', 'Not enough items in inventory.' )
        else:
            self.storage.updateQty( item_name, new_quantity )
        return ( '200 OK', ' ' )

    def getQty( self, *args ):
        maybe_quantity = self.storage.getItemQty( args )
        if maybe_quantity is None:
            return ( '404 Not Found', '' )
        else:
            return ( '200 OK', '%s' % json.dumps(maybe_quantity))

    def delItem( self, item_name ):
        if self.storage.delItem( str.lower(item_name) ):
            return ( '204 No Content', '' )
        else:
            return ( '404 Not Found', '' )

    def getTotalItems( self ):
        total = self.storage.getTotalItems()
        if total == 0:
            return ('404 Not Found', ' bitches!')
        else:
            return ('200 OK', '%d' % total)

    def dispatch( self, environ ):
        self.storage.open()
        try:
            http_method  = environ[ 'REQUEST_METHOD' ]
            url_path     = environ[ 'PATH_INFO' ]
            query_string = environ[ 'QUERY_STRING' ]
            body = getBody( environ )
            parsed_parts = parse.parse_qs(body)
            path_parts   = url_path.split( '/' )
            #Add Item to inventory
            if http_method == 'POST' and len( path_parts ) == 2 and path_parts[ 1 ] == 'inventory':
                rv = self.addItem( parsed_parts )
            #Get total number of items in the inventory
            elif http_method == 'GET' and len( path_parts ) == 3 and path_parts[ 2 ] == 'total' and path_parts[ 1 ] == 'inventory' :
                rv = self.getTotalItems()
            #Get the quantity of a specific item
            elif http_method == 'GET' and len( path_parts ) == 3 and path_parts[ 1 ] == 'inventory':
                rv = self.getQty( path_parts[2] )
            #Get the full inventory
            elif http_method == 'GET' and len( path_parts ) == 2 and path_parts[ 1 ] == 'inventory':
                rv = self.getQty( )
            #Get the items whose quantities match the given restrictions
            elif http_method == 'POST' and len(path_parts) == 3 and path_parts[2] == 'bounded' and path_parts[1] == "inventory":
                rv = self.getBoundedItems( parsed_parts, query_string )
            #Update the quantity of a given item
            elif http_method == 'POST' and len(path_parts) == 3 and path_parts [1] == 'inventory':          
                rv = self.updateQty( path_parts[2], parsed_parts )
            #Delete an item from the inventory
            elif http_method == 'DELETE' and len( path_parts ) == 3 and path_parts[ 1 ] == 'inventory':
                rv = self.delItem( path_parts[2] )
            else:
                rv = ( "400 Bad Request", "" )
        finally:
            self.storage.close()
        return rv
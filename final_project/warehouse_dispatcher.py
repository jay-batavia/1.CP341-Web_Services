from urllib import parse
import json
import sys
import math




class WarehouseDispatcher:
   
    def getBody( self, environ ):
        if 'CONTENT_LENGTH' in environ and environ[ 'CONTENT_LENGTH' ] != '':
            try:
                cl = int( environ[ 'CONTENT_LENGTH' ] )
            except:
                return ( '500 Internal Server Error', '' )
            return environ[ 'wsgi.input' ].read( cl ).decode( 'utf-8' )
        else:
            return ""

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

    def createFragment(self, result, limit):
        list_number = math.ceil(len(result)/limit)
        result_list =[]
        for i in range(list_number):
            sub_dict = {}
            key_list = []
            lower_bound = i*limit
            upper_bound = (i+1)*limit
            if upper_bound >= len(result):
                key_list = list(sorted(result))[lower_bound:]
                for key in key_list:
                    sub_dict[key] = result[key]
                result_list.append(sub_dict)
            else:
                key_list = list(sorted(result))[lower_bound:upper_bound]
                for key in key_list:
                    sub_dict[key] = result[key]
                result_list.append(sub_dict)
        return result_list

      

    def getBoundedItems(self, query_params, query_string):
        upper_bound = sys.maxsize
        lower_bound = 0
        qs = parse.parse_qs(query_string)
        number = sys.maxsize
        page = 0
        try:    
            if "lower_bound" in query_params and "upper_bound" in query_params:
                upper_bound = int(query_params["upper_bound"][0])
                lower_bound = int(query_params["lower_bound"][0])
            elif "upper_bound" in query_params:
                upper_bound = int(query_params["upper_bound"][0])
            elif "lower_bound" in query_params:
                lower_bound = int(query_params["lower_bound"][0])
            if 'number' in qs:
                number = int(qs['number'][0])
            if 'page' in qs:
                page = int(qs['page'][0])
        except:
            return ('400 Bad Request', ' The parameters must be integers. ')

        bounded_items = self.storage.getBoundedItems( upper_bound, lower_bound )
        limit = min(self.item_limit, number)

        if bounded_items is None:
            return( '404 NOT FOUND', 'No items found within the given range.' )
        else:
            if len(bounded_items) <= limit:
                return ('200 OK', '%s' % json.dumps(bounded_items))
            
            elif len(bounded_items) > limit:
                result_list = self.createFragment(bounded_items, limit)

                result_page = result_list[page-1]

                return ('200 OK', 'Page %d of %d: \n %s' % (page+1, len(result_list), json.dumps(result_page)))


    def getPrefixItems( self, query_string ):
        qs = parse.parse_qs(query_string)
        number = sys.maxsize
        page = 0
        try:
            if 'number' in qs:
                number = int(qs['number'][0])
            if 'page' in qs:
                page = int(qs['page'][0])
            if 'prefix' in qs:
                prefix = qs['prefix'][0] 
        except:
            return ('400 Bad Request', 'The parameters must be integers')
        prefix_items = self.storage.getPrefixItems( prefix )
        limit = min(self.item_limit, number)
        if prefix_items is None:
            return ('404 Not Found', '')
        else:
            if len(prefix_items)<= limit:
                return ('200 OK', '%s' % json.dumps(prefix_items))
            else:
                result_list = self.createFragment(prefix_items, limit)
                result_page = result_list[page-1]
                return('200 OK', 'Page %d of %d: \n %s' % (page+1, len(result_list), json.dumps(result_page)))

    def getQty( self, *args ):
        qs = parse.parse_qs(args[1])
        number = sys.maxsize
        page = 0
        try:
            if 'number' in qs:
                number = int(qs['number'][0])
            if 'page' in qs:
                page = int(qs['page'][0])
        except:
            return ('400 Bad Request', 'The parameters must be integers')

        quantity_list = self.storage.getItemQty( args[0] )
        limit = min(self.item_limit, number)
        if quantity_list is None:
            return ( '404 Not Found', '' )
        else:
            if len(quantity_list) <= limit:
                return ( '200 OK', '%s' % json.dumps(quantity_list))
            else:
                result_list = self.createFragment(quantity_list, limit)
                result_page = result_list[page-1]
                return ('200 OK', 'Page %d of %d: \n %s' % (page+1, len(result_list), json.dumps(result_page)))


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
            body = self.getBody( environ )
            parsed_parts = parse.parse_qs(body)
            path_parts   = url_path.split( '/' )
            #Add Item to inventory
            if http_method == 'POST' and len( path_parts ) == 2 and path_parts[ 1 ] == 'inventory':
                print(parsed_parts)
                rv = self.addItem( parsed_parts )
            elif http_method == 'GET' and len( path_parts ) == 2 and path_parts [ 1 ] == 'inventory' and 'prefix' in query_string:
                rv = self.getPrefixItems( query_string )
            #Get total number of items in the inventory
            elif http_method == 'GET' and len( path_parts ) == 3 and path_parts[ 2 ] == 'total' and path_parts[ 1 ] == 'inventory' :
                rv = self.getTotalItems()
            #Get the quantity of a specific item
            elif http_method == 'GET' and len( path_parts ) == 3 and path_parts[ 1 ] == 'inventory':
                rv = self.getQty( path_parts[2], query_string )
            #Get the full inventory
            elif http_method == 'GET' and len( path_parts ) == 2 and path_parts[ 1 ] == 'inventory':
                rv = self.getQty( '', query_string )
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
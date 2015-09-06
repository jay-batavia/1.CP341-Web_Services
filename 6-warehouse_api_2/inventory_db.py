import warehouse
import os.path
import sqlite3
import json
from urllib import parse

db_filename = 'inventory_test.db'
conn = sqlite3.connect(db_filename)
dbc = conn.cursor()
class WarehouseApp_Impl_db(warehouse.Warehouse):
    
    #Creates and populates the inventory database if it doesn't exist.
    def createInventoryDB(filename):        
            query = dbc.execute('''CREATE TABLE IF NOT EXISTS inventory (item_name text, item_quantity int)''')
            if query.rowcount == -1:
                return
            else:        
                initial_items = [('ps1', 20), ('ps2', 30), ('ps3', 45), ('ps4', 58)]
                dbc.executemany('INSERT INTO inventory VALUES (?,?,?,?)', inital_items)
                conn.commit()


    
    def updateItemQuantity(self, item_name, update):
        dbc.execute('''SELECT * FROM inventory WHERE item_name=?''', [item_name])
        retrieved_item = dbc.fetchall()[0]
        if retrieved_item is not None:
            original_quantity = retrieved_item[1]
        else:
            raise KeyError

        if "add_quantity" in update:
            add_quantity = int(update['add_quantity'][0]) 
            new_quantity = int(original_quantity) + add_quantity

        elif "remove_quantity" in update:
            remove_quantity = int(update['remove_quantity'][0])
            new_quantity = original_quantity - remove_quantity
            if new_quantity < 0:
                raise ValueError

        dbc.execute('''UPDATE inventory SET item_quantity=? WHERE item_name=?''', [new_quantity, item_name])
        conn.commit()

        return

    def updateInventory(self, update):
        for i in range(len(update['item_name'])):
            try:
                item_name = update['item_name'][i]
                item_quantity = update['item_quantity'][i]
            except:
                raise KeyError

            if(int(item_quantity)<0):
                raise ValueError
            else:
                rows_affected = dbc.execute('''UPDATE inventory SET item_quantity=? WHERE item_name=?''', [item_quantity, str.lower(item_name)])
                if(rows_affected.rowcount < 0):
                    dbc.execute('''INSERT INTO inventory VALUES (?,?)''', [str.lower(item_name), item_quantity]) 
        conn.commit()
        return



    def getItemQuantity(self, *args):

        item_quantity = {}
        if(len(args)==1):
            item_name = str.lower(args[0])
            dbc.execute('''SELECT * from inventory WHERE item_name=?''', [item_name])
        elif(len(args)==0):
            dbc.execute('''SELECT * from inventory''')

        retrieved_item = dbc.fetchall()
        if len(retrieved_item) == 0:
            raise KeyError
        else:
            item_dict = dict(retrieved_item)

        return item_dict

    def getBoundedItems(self, query_params):
        bounded_dict = {}
        if "lower_bound" in query_params and "upper_bound" in query_params:
            upper_bound = query_params["upper_bound"][0]
            lower_bound = query_params["lower_bound"][0]
        elif "upper_bound" in query_params:
            upper_bound = query_params["upper_bound"][0]
            lower_bound = 0
        elif "lower_bound" in query_params:
            lower_bound = query_params["lower_bound"][0]
            upper_bound = 1000000

        else:
            raise KeyError

        dbc.execute('''SELECT * FROM inventory WHERE item_quantity >= ? and item_quantity <= ?''', [lower_bound, upper_bound])
        retrieved_item = dbc.fetchall()
        if len(retrieved_item)==0:
            raise ValueError
        else:
            item_name = dict(retrieved_item)
        return item_dict

    def deleteItem(self, item_name):
        query = dbc.execute('''DELETE FROM inventory WHERE item_name = ?''', [item_name])
        if query.rowcount < 1:
            raise KeyError
        else:
            pass
        conn.commit()
        return

    def parse_request( self, environ ):
        qs = environ['QUERY_STRING']
        rm = environ['REQUEST_METHOD']
        pi = environ['PATH_INFO']
        response = {'status': "", 'text': ""}
        url_list = pi.split('/')


        if url_list[1] == "inventory" and rm == "GET":
            try:
                if(len(url_list)>2):
                    inventory_id = url_list[2]
                    item_quantity = self.getItemQuantity(inventory_id)
                else:
                    item_quantity = self.getItemQuantity()
                response['status'] = "200 OK"
                response['text'] = json.dumps(item_quantity)

            except KeyError as e:
                response['status'] = "404 NOT FOUND"
                response['text']= str(e)
                pass


        elif len(url_list) == 2 and url_list[1] == "inventory" and rm == "POST":
            if len(environ['CONTENT_LENGTH']) > 0:
                try:
                    request_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode('utf-8')                
                    query_params = parse.parse_qs(request_body)
                    self.updateInventory(query_params)
                    response['status'] = "200 OK"
                    response['text'] = 'Inventory successfully updated'

                except:
                    response['status'] = "400 Bad Request"
                    response['text'] = "Update request not properly formed."
            else:
                response['status'] = "400 Bad Request"
                response['text'] = "request body cannot be empty"



        elif url_list[1] == "inventory" and rm == "DELETE":
            try:
                if(len(url_list)==3):
                    inventory_id = url_list[2]
                    self.deleteItem(inventory_id)
                    response['status'] = "200 OK"
                    response['text'] = "%s has been removed from inventory\n" % inventory_id

                else:
                    response['status'] = "400 Bad Request"
            except LookupError as le:
               response['status'] = "404 NOT FOUND"
               response['text'] = str(le)



        elif url_list[1] == "inventory" and url_list[2] == "bounded" and rm == "POST":
            if len(environ['CONTENT_LENGTH']) > 0:
                request_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode('utf-8')

                try:
                    query_params = parse.parse_qs(request_body)
                    bounded_items = self.getBoundedItems(query_params)
                    response['status'] = '200 OK'
                    response['text'] = json.dumps(bounded_items)

                except:
                    response['status'] = '400 Bad Request'
                    response['text'] = 'Request body not properly formed. Bounds must be integers'



        elif url_list[1] == "inventory" and len(url_list[2]) > 0 and rm == "POST":
            item_name = url_list[2]

            if len(environ['CONTENT_LENGTH']) > 0:
                request_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode('utf-8')

                try:
                    query_params = parse.parse_qs(request_body)
                    self.updateItemQuantity(item_name, query_params)
                    response['status'] = '200 OK'
                    response['text'] = '%s quantity updated' % item_name

                except ValueError:
                    response['status'] = '400 Bad Request'
                    response['text'] = 'Cannot remove more than the number of items'
                except KeyError:
                    response['status'] = '404 NOT FOUND'
                    response['text'] = 'The '
               
                except:
                    response['status'] = '400 Bad Request'
                    response['text'] = 'Update request not properly formed'            

            else:
                response['status'] = '400 Bad Request'
                response['text'] = 'There must be a request_body'

        else:
            response['status'] = "400 Bad Request"
            response['text'] = "You have made an unsupported request. Please check the documentation"

        return response
    # createInventoryDB(db_filename)
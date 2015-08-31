from pprint import pprint
import json
import io
from urllib import parse

class warehouse_app:


    def createInventoryFile(self):
        f = open('inventory.json', 'w')
        f.close()


    def parse_request( self, environ ):
        qs = environ['QUERY_STRING']
        rm = environ['REQUEST_METHOD']
        pi = environ['PATH_INFO']
        print("PATH INFO: ", pi)
        infos = { 'qs':qs, 'rm':rm, 'pi':pi }
        response = {}
        url_list = pi.split('/')


        if "inventory" in url_list[1]:
            inventory_id = url_list[2]
            try:
                f = open('inventory.json', 'r')
                file_content = f.read()
                file_json = json.loads(file_content)

            except:
                response['status'] = "404 NOT FOUND"
                response['text']= "Inventory file not found. Please use the /file/ endpoint to initialize"
                pass

            try:
                item_quantity = file_json[inventory_id]
                response['status'] = "200 OK"
                response['text'] = "Item: "+inventory_id+"\nQuantity: "+item_quantity

            except:
                response['status'] = "404 NOT FOUND"
                response['text'] = "Warehouse item not found. Please verify item name."
                pass
            


        return response
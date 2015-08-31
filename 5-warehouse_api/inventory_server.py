from pprint import pprint
import json
import io
from urllib import parse
import sys

inventory_filename = 'inventory.json'
class warehouse_app:


    def loadInventoryFile(self, filename):
        try:
            f = open(filename, 'r')
            file_content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError("Inventory file does not exist. Refer to documentation for /file endpoint")

        try:
            file_dict = json.loads(file_content)
        except ValueError as e:
            raise ValueError("JSON inventory file badly formed. Please check the file.")
        
        f.close()
        return file_dict

    def writeToInventoryFile(self, json_data, filename):
        try:
            f = open(filename, 'w')
            print("loaded file")

            file_content = f.write(json_data)

        except FileNotFoundError:
            raise FileNotFoundError("Inventory file does not exist. Refer to documentation for /file endpoint")

        except TypeError as e:
            print ("Error:", str(e))
            raise 
        # ose("Inventory file does not exist. Refer to documentation for /file endpoint")

        # f.write(json_data)

        f.close()
        return

    def updateInventory(self, update):
        try:
            file_dict = self.loadInventoryFile("inventory.json")
        except FileNotFoundError as fileError:
            raise fileError("FileError")
        except ValueError as e:
            raise e

        item_name = update['item_name'][0]
        item_quantity = update['item_quantity'][0]

        file_dict[item_name] = item_quantity
        file_json = json.dumps(file_dict, sort_keys=True, indent=4, separators=(',',': '))
        try:
            self.writeToInventoryFile(file_json, "inventory.json")
        except:
            print ("Error:", sys.exc_info()[0])
            raise

        return



    def getItemQuantity(self, item_name):
        item_quantity = {}
        file_json = self.loadInventoryFile('inventory.json')
 
        try:
            item_quantity[item_name] = file_json[item_name]
        except:
            raise KeyError("Item not found in inventory, please check Item name or add it using /inventory/put")
       
        return item_quantity

    def getItemQuantity(self):
        file_json = self.loadInventoryFile('inventory.json')
        
        return file_json


    def parse_request( self, environ ):
        qs = environ['QUERY_STRING']
        rm = environ['REQUEST_METHOD']
        pi = environ['PATH_INFO']
        infos = { 'qs':qs, 'rm':rm, 'pi':pi }
        response = {}
        url_list = pi.split('/')


        if url_list[1] == "inventory" and rm == "GET":
            try:
                if(len(url_list)>2):
                    inventory_id = url_list[2]
                    item_quantity = self.getItemQuantity(inventory_id)
                else:
                    item_quantity = self.getItemQuantity()
                response['status'] = "200 OK"
                response['text'] = json.dumps(item_quantity, sort_keys=True, indent=4, separators=(',',': '))

            except KeyError as e:
                print("Exception occurred: ", e)
                response['status'] = "404 NOT FOUND"
                response['text']= str(e)
                pass

        if url_list[1] == "inventory" and rm == "POST":
            if len(environ['CONTENT_LENGTH']) > 0:
                try:
                    request_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode('utf-8')
                    query_params = parse.parse_qs(request_body)
                    self.updateInventory(query_params)
                    response['status'] = "200 OK"
                    response['text'] = 'Inventory successfully updated'
                except:
                    print("Error:", sys.exc_info()[0])

        return response
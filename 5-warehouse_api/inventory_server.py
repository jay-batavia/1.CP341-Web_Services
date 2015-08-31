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

        try:
            print("Update type ", type(update['item_name']))
            item_name = update['item_name'][0]
            item_quantity = update['item_quantity'][0]
        except KeyError:
            raise KeyError("Badly formed post body. Please try again")

        if(int(item_quantity)<0):
            raise ValueError("Quantity must be a positive number or zero")
        else: 
 
            file_dict[item_name] = item_quantity
            file_json = json.dumps(file_dict, sort_keys=True, indent=4, separators=(',',': '))
       
        try:
            self.writeToInventoryFile(file_json, "inventory.json")
        except:
            print ("Error:", sys.exc_info()[0])
            raise

        return


    def getItemQuantity(self, *args):
        item_quantity = {}
        file_json = self.loadInventoryFile('inventory.json')
        if(len(args)==1):
            item_name = args[0]
 
            try:
                item_quantity[item_name] = file_json[item_name]
            except:
                raise KeyError("Item not found in inventory, please check Item name or add it using /inventory/put")
 
        elif(len(args)==0):
            item_quantity = file_json
        return item_quantity


    def deleteItem(self, inventory_id):
        file_dict = self.loadInventoryFile('inventory.json')
        if inventory_id in file_dict:
            try:
                del file_dict[inventory_id]
                file_json = json.dumps(file_dict, sort_keys=True, indent=4, separators=(',',': '))
                self.writeToInventoryFile(file_json, 'inventory.json')
            except:
                print("Error:", sys.exc_info()[0])
        else:
            raise LookupError("The item you're trying to delete does not exist.")
        return




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

        elif url_list[1] == "inventory" and rm == "POST":
            if len(environ['CONTENT_LENGTH']) > 0:
                try:
                    request_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode('utf-8')
                    query_params = parse.parse_qs(request_body)
                    self.updateInventory(query_params)
                    response['status'] = "200 OK"
                    response['text'] = 'Inventory successfully updated'

                except ValueError as e:
                    response['status'] = "400 Bad Request"
                    response['text'] = "Please input positive quantities for items"

                except KeyError as ke:
                    response['status'] = "400 Bad Request"
                    response['text'] = str(ke)

                except TypeError as te:
                    print("Typerror...", te)

                except:
                    print("Error:", sys.exc_info()[0])

        elif url_list[1] == "inventory" and rm == "DELETE":
            try:
                if(len(url_list)==3):
                    inventory_id = url_list[2]
                    self.deleteItem(inventory_id)
                    response['status'] = "200 OK"
                    response['text'] = "%s has been removed from inventory" % inventory_id

                else:
                    response['status'] = "400 Bad Request"
                    response['text'] = "Can only delete individual items"
            except LookupError as le:
               response['status'] = "404 NOT FOUND"
               response['text'] = str(le)

        else:
            response['status'] = "400 Bad Request"
            response['text'] = "You have made an unsupported request. Please check the documentation"

        return response
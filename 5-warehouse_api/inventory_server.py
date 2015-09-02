import json
import io
from urllib import parse
import sys
import os.path

inventory_filename = "inventory.json"
class WarehouseApp:

    def createInventoryFile(filename):
        if(os.path.isfile(filename)):
            pass;
        else:
            f = open(filename, 'w')
            f.close()


    def loadInventoryFile(self, filename):
        file_dict={}
        try:
            f = open(filename, 'r')
            file_content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError("Inventory file does not exist. Add items to begin.")

        if(len(file_content)==0):
            pass

        else:
            file_dict = json.loads(file_content)
        
        f.close()
        return file_dict


    def writeToInventoryFile(self, json_data, filename):
        try:
            f = open(filename, 'w')
            file_content = f.write(json_data)

        except FileNotFoundError:
            raise FileNotFoundError("Inventory file does not exist.")

        except TypeError as e:
            raise e("TypeError")
        # ose("Inventory file does not exist. Refer to documentation for /file endpoint")

        # f.write(json_data)

        f.close()
        return


    def updateItemQuantity(self, item_name, update):
        print("in updateitemquantity")
        try:
            file_dict = self.loadInventoryFile(inventory_filename)
        except:
            print("Load inventory file error")

        if item_name in file_dict:
            original_quantity = int(file_dict[item_name])

        else:
            raise KeyError("inventory item not found")

        if "add_quantity" in update:
            addition_number = int(update['add_quantity'][0])

            total = original_quantity + addition_number

        elif "remove_quantity" in update:
            remove_number = int(update['remove_quantity'][0])
            total = original_quantity - remove_number
            if total < 0:
                raise ValueError

        file_dict[item_name] = str(total)

        file_json = json.dumps(file_dict)

        try:
            self.writeToInventoryFile(file_json, inventory_filename)
        except:
            raise
        
        return


    def updateInventory(self, update):
        try:
            file_dict = self.loadInventoryFile(inventory_filename)
        except FileNotFoundError as fileError:
            raise fileError("FileError")
        except ValueError as e:
            raise e
        

        for i in range(len(update['item_name'])):
            try:    
                item_name = update['item_name'][i]
                item_quantity = update['item_quantity'][i]
            except:
                raise KeyError("Badly formed post body. Please try again")

            if(int(item_quantity)<0):
                raise ValueError("Quantity must be a positive number")
            else: 
     
                file_dict[str.lower(item_name)] = item_quantity.strip()

        file_json = json.dumps(file_dict)
       
        try:
            self.writeToInventoryFile(file_json, inventory_filename)
        except:
            raise

        return


    def getItemQuantity(self, *args):
        item_quantity = {}
        file_dict = self.loadInventoryFile(inventory_filename)
        if(len(args)==1):
            item_name = str.lower(args[0])
            try:
                item_quantity[item_name] = file_dict[item_name]
            except:
                raise KeyError("Item not found in inventory, please check Item name or add it using /inventory")
 
        elif(len(args)==0):
            item_quantity = file_dict

        return item_quantity

    def getBoundedItems(self, query_params):
        bounded_dict = {}
        file_dict = self.loadInventoryFile(inventory_filename)
        if "lower_bound" in query_params and "upper_bound" in query_params:
            upper_bound = query_params["upper_bound"][0]
            print("upper bound: "+ upper_bound)
            lower_bound = query_params["lower_bound"][0]
            print("lower bound: "+ lower_bound)
        elif "upper_bound" in query_params:
            upper_bound = query_params["upper_bound"][0]
            lower_bound = 0
        elif "lower_bound" in query_params:
            lower_bound = query_params["lower_bound"][0]
            upper_bound = 1000000

        else:
            raise KeyError("Badly formed post body")

        try:
            for key, val in file_dict.items():
                if int(val) >= int(lower_bound) and int(val) <= int(upper_bound):
                    bounded_dict[key] = val
        except:
            raise

        return bounded_dict


    def deleteItem(self, inventory_id):
        file_dict = self.loadInventoryFile(inventory_filename)
        if inventory_id in file_dict:
            del file_dict[inventory_id]
            file_json = json.dumps(file_dict)
            self.writeToInventoryFile(file_json, inventory_filename)
        else:
            raise LookupError("The item you're trying to delete does not exist in the inventory.")
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
                response['text'] = ""



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

    createInventoryFile(inventory_filename)
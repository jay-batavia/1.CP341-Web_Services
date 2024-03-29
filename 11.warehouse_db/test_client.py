from pprint import pprint
import json
import http.client, urllib.parse

encoding = 'utf-8'

def updateInventory(connection, update_params, path):
	params = urllib.parse.urlencode(update_params)
	connection.request('POST', path, params)
	response = connection.getresponse()
	if(response.status == 201):
		return "Success. "+str(response.status)+" "+response.reason	
	else:
		return "FAILED. "+ str(response.status)+" "+response.reason


def getItemQty(connection, path):
	connection.request('GET', path)
	response = connection.getresponse()
	if(response.status == 200):
		data = response.read()
		decoded_data = data.decode(encoding)
		data_list = decoded_data.split('\n')
		json_data = data_list[1]
		inventory_list = json.loads(json_data)
		return str(inventory_list)

	elif(response.status == 404):
		return (str(response.status) + " " +response.reason)

	else:
		return(str(response.status)+" "+response.reason)

def deleteInventoryItem(connection, path):
	connection.request('DELETE', path)
	response = connection.getresponse()
	if(response.status == 204):
		return "Success. "+str(response.status)+" "+response.reason	
	else:
		return "FAILED. "+ str(response.status)+" "+response.reason





url = "localhost:8000"
connection = http.client.HTTPConnection(url)

# #Initialize inventory file
# print("REQ: method=POST params={item_name: NES, item_quantity: 100} /inventory (valid)")
# print("RES: "+ updateInventory(connection, {'item_name': 'SEGA', 'item_quantity':'25'}, "/inventory")+"\n")

#Get quantity of individual item
print("REQ: method=GET /inventory/PS4 (Valid)")
print("RES: "+ getItemQty(connection, "/inventory/PS4")+"\n")

#Call the wrong endpoint with GET
print("REQ: method=GET /invent (invalid)")
print("RES: "+ getItemQty(connection, "/invent")+"\n")

#Check Pagination
print("REQ: method=GET /inventory?page=2")
print("RES: "+getItemQty(connection, '/inventory?page=2')+'\n')

#Get quantity of an item that doesn't exist
print("REQ: method=GET /inventory/P4 (invalid)")
print("RES: "+ getItemQty(connection, "/inventory/P4")+"\n")

#Get full inventory
print("REQ: method=GET /inventory (valid)")
print("RES: "+ getItemQty(connection, "/inventory")+"\n")

#Update inventory with nothing
print("REQ: method=POST params="" /inventory (invalid)")
print("RES: "+ updateInventory(connection, "", "/inventory")+"\n")

#Update quantity of an existing item
print("REQ: method=POST params={item_name: PS4, item_quantity:50} /inventory (valid)")
print("RES: "+ updateInventory(connection, {'item_name':'PS4', 'item_quantity':'50'}, "/inventory")+"\n")

#Check if quantity is updated
print("REQ: method=GET /inventory/PS4 (valid)")
print("RES: "+ getItemQty(connection, "/inventory/PS4")+"\n")


#Add item and its quantity to the inventory
print("REQ: method=POST params={item_name: SEGA, item_quantity: 25} /inventory (valid)")
print("RES: "+ updateInventory(connection, {'item_name': 'sega', 'item_quantity':'25'}, "/inventory")+"\n")

#Check if item was added to inventory
print("REQ: method=GET /inventory/SEGA (valid)")
print("RES: "+ getItemQty(connection, "/inventory/SEGA")+"\n")

#Invalid inventory update.
print("REQ: method=POST params={item_name: SEGA, item_quantity: 2m5} /inventory (invalid)")
print("RES: "+ updateInventory(connection, {'item_name': 'SEGA', 'item_quantity':'2m5'}, "/inventory")+"\n")

#another invalid inventory update
print("REQ: method=POST params={item_name: SEGA, ite m_quantity: 25} /inventory (invalid)")
print("RES: "+ updateInventory(connection, {'item_name': 'SEGA', 'it em_quantity':'25'}, "/inventory")+"\n")

# Attempt to delete entire inventory
print("REQ: method=DELETE /inventory (invalid)")
print("RES: "+ deleteInventoryItem(connection, "/inventory")+"\n")

#Delete individual item
print("REQ: method=DELETE /inventory/SEGA (valid)")
print("RES: "+ deleteInventoryItem(connection, "/inventory/SEGA")+"\n")

#Check if item deleted
print("REQ: method=GET /inventory (valid)")
print("RES: "+ getItemQty(connection, "/inventory")+"\n")

#Add multiple items at once
print("REQ: method=POST params={item_name=snes, item_quantity=23, item_name=nes, item_quantity=28} /inventory (valid)")
print("RES: "+ updateInventory(connection, {'item_name':'snes', 'item_quantity':'23', 'item_name':'nes', 'item_quantity':'28'}, "/inventory")+"\n")

#Check if all items were added
print("REQ: method=GET /inventory")
print("RES: "+getItemQty(connection, "/inventory")+"\n")

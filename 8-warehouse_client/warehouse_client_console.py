import json
import http.client, urllib.parse
from pprint import pprint

encoding = 'utf-8'
def addItem( connection, update_params, path ):
	params = urllib.parse.urlencode(update_params)
	connection.request( 'POST', path, params )
	response = connection.getresponse()
	if response.status == 201:
		print('\nInventory updated with %s %s \n' % (update_params['item_quantity'], update_params['item_name']))
	else:
		print( "Something went wrong" )
	return

def updateQty( connection, update_params, path ):
	params = urllib.parse.urlencode(update_params)
	connection.request( 'POST', path, params)
	response = connection.getresponse()
	if response.status == 200:
		print("Quantity Updated")
	elif response.status == 404:
		print("Could not find item to update")
	elif response.status == 400:
		print('Made a bad request.')
	return

def getBoundedItems( connection, bounds, path ):
	params = urllib.parse.urlencode(bounds)
	connection.request( 'POST', path, params )
	response = connection.getresponse()
	if response.status == 200:
		data = response.read()
		decoded_data = data.decode(encoding)
		data_list = decoded_data.split('\n')
		json_data = data_list[1]
		inventory_list = json.loads(json_data)
		print(data_list[0])
		print("Item     Quantity")
		print("=================")
		for k, v in inventory_list.items():
			print(k+"    |    "+str(v))
	elif response.status == 404:
		print("No items found matching given restrictions")

def getItemQty( connection, path ):
	connection.request('GET', path)
	response = connection.getresponse()
	if response.status == 200:
		data = response.read()
		decoded_data = data.decode(encoding)
		data_list = decoded_data.split('\n')
		json_data = data_list[1]
		inventory_list = json.loads(json_data)
		print(data_list[0])
		if len(path.split("/")) == 3:
			for k,v in inventory_list.items():
				print( "\nItem name: %s, Quantity left: %d.\n"% (k, v))
		elif len(path.split("/")) == 2:
			print("Item     Quantity")
			print("==================")
			for k, v in inventory_list.items():
				print(k+"   |   "+str(v))
	elif response.status == 404:
		print("Item not found!")

def deleteItem( connect, path ):
	connection.request('DELETE', path)
	response = connection.getresponse()
	if response.status == 204:
		print("Successfully deleted the requested item.")
	elif response.status == 404:
		print("Could not find the requested item.")
	return

url = 'localhost:8000'
path = '/inventory'
connection = http.client.HTTPConnection(url)
while True:
	print("What would you like to do?")
	print("1. Add an item in the inventory.")
	print("2. Update item in the inventory.")
	print("3. Get inventory information")
	print("4. Delete an inventory item")
	print("5. Exit")
	choice = input()
	if choice not in ('1', '2', '3', '4', '5'):
		print ("Invalid Choice")

	if choice == '1':
		item_name = input('Please enter the item name.\n')
		item_quantity = input('Please enter the quantity.\n')
		update_params = {'item_name': item_name, 'item_quantity': item_quantity}
		addItem(connection, update_params, path)


	elif choice == '2':
		item_name = input('Please enter the item name.\n')
		print("Would you like to 1. add or 2. remove a quantity?")
		update_choice = input()
		if update_choice == '1':
			update_quantity = input("How many of %s would you like to add?\n" % item_name)
			param = {'update_quantity': update_quantity}
		elif update_choice == '2':
			update_quantity = input("How many of %s would you like to remove?\n" % item_name)
			param = {'update_quantity': "-"+update_quantity}
		else:
			print("Invalid choice")

		updateQty(connection, param, path+"/"+item_name)


	elif choice == '3':
		print( "1. Get a specific item quantity")
		print( "2. Get items with quantities that match given restrictions." )
		print( "3. Get the full Inventory")
		get_choice = input()
		if get_choice == '1':
			item_name = input('Please enter the name of the item you want to retrieve.\n')
			getItemQty(connection, path+"/"+item_name)
		
		elif get_choice == '2':
			lower_bound = input('Please enter a lower bound. Leave blank for 0.\n')
			upper_bound = input('Please enter an upper bound. Leave blank for an absurdly high number.\n')
			if len(lower_bound) == 0:
				lower_bound = 0
			if len(upper_bound) == 0:
				upper_bound = 100000000;
			bounds = {'lower_bound': lower_bound, 'upper_bound': upper_bound}
			getBoundedItems(connection, bounds, path+"/bounded")

		elif get_choice == '3':
			getItemQty( connection, path )
	
	elif choice == '4':
		delete_name = input("Please enter the name of the item you want to delete.\n")
		deleteItem( connection, path+"/"+delete_name)

	elif choice == '5':
		break
import json
import urllib.parse, http.client
import random
import string

encoding = 'utf-8'

def generate_random( size = 7 ):
	charset = string.ascii_uppercase + string.digits
	random_sting = ''
	return ''.join(random.choice(charset) for i in range (size))
	

def populateWarehouse(number_items=50):
	item_list = []
	quantity_list = []
	random_items = {} 
	for i in range (number_items):
		item_quantity = random.randint(1, 1000)
		string_size = random.randint(3, 8)
		random_item = generate_random( string_size )
		item_list.append(random_item)
		quantity_list.append(item_quantity)
	j=0
	string_param = ''
	for item in item_list:
		string_param += 'item_name=%s&item_quantity=%d' % (item_list[j], quantity_list[j])
		if j == len(quantity_list) - 1:
			break
		else:
			string_param += '&'
			j += 1			
			
	
	return string_param



def addItem(connection, path ):
	update_params = populateWarehouse()
	params = urllib.parse.parse_qs(update_params)
	post_params = urllib.parse.urlencode(params)
	connection.request( 'POST', path, params )
	response = connection.getresponse()
	if response.status == 201:
		print("Inventory updated")
		# print('\nInventory updated with %s %s \n' % (update_params['item_quantity'], update_params['item_name']))
	else:
		print( "Something went wrong" )
	return

url  = "localhost:8000"
connection = http.client.HTTPConnection(url)
addItem( connection, '/inventory')

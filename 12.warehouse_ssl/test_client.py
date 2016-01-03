from pprint import pprint
import json
import base64
import http.client, urllib.parse

encoding = 'utf-8'
username = 'jay'
password = 'test'
password2 = 'test2'

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


def get_response( method, url, body=None, headers={}):
	connection.request( method, url, body=body, headers=headers)
	response = connection.getresponse()
	if (response.status == 200):
		data = response.read()
		decoded_data = data.decode(encoding)
		inventory_list = json.loads(decoded_data)
		return str(inventory_list)
	elif (response.status == 403):
		return "FAILED. "+str(response.status)+" "+response.reason
	else:
		return "FAILED. "+str(response.status)+" "+response.reason
	body_bytes = resp.read()
	body = body_bytes.decode( resp.headers.get_content_charset( 'default' ))
	return ( resp, body )

user_str = '%s:' % username
user_auth_bytes = user_str.encode( 'utf-8' ) + password.encode( 'utf-8' )
user_auth_bytes2 = user_str.encode( 'utf-8' ) + password2.encode( 'utf-8' )
up_b64_bytes = base64.b64encode( user_auth_bytes )
up_b64_bytes2 = base64.b64encode( user_auth_bytes2 )
up_b64_str = up_b64_bytes.decode( 'ascii' )
up_b64_str2 = up_b64_bytes2.decode( 'ascii' )
authheader = "Basic %s" % up_b64_str
authheader2 = "Basic %s" % up_b64_str2

url = "localhost:8000"
connection = http.client.HTTPConnection(url)

print("Making request with right credentials. un: jay pw: test.")
resp = get_response( 'GET', '/inventory', headers={'Authorization': authheader})
print("Response:")
print("Body: \n %s" %resp)

print("Making bad request with wrong credentials. un: jay pw: test2")
resp = get_response( 'GET', '/inventory', headers={'Authorization': authheader2})
print(resp)

print("Making request with not credentials.")
resp = get_response( 'GET', '/inventory',)
print (resp)
# #Initialize inventory file
# print("REQ: method=POST params={item_name: NES, item_quantity: 100} /inventory (valid)")
# print("RES: "+ updateInventory(connection, {'item_name': 'SEGA', 'item_quantity':'25'}, "/inventory")+"\n")

#Get quantity of individual item 
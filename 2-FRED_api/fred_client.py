#!/usr/bin/env python3

from pprint import pprint

import json

import http.client, urllib.parse

 

def http_get(connection, path, id, dict={}):

 dict['api_key'] = '65d553164ee45553def2ac6cab3f6c4c'

 dict['file_type'] = 'json'
 
 if not id:
  dict['category_id'] = 0

 else:
  dict['category_id'] = id

 connection.request('GET', path + '?' + urllib.parse.urlencode(dict))

 response = connection.getresponse()

 if response.status == 200:

   data = response.read()

   return json.loads(data.decode('utf-8'))

 else:

   raise Exception("HTTP call failed: " + response.reason)

 

url = 'api.stlouisfed.org'

connection = http.client.HTTPSConnection(url)



def writeFile(data):
	f = open('series.txt', 'w')
	f.write(data)
	f.close()
 

# get the children of the root category

children = http_get(connection, '/fred/category/children', 0)


for c in children['categories']:
	series = http_get(connection, '/fred/category/series', c['id'])
	if series['seriess']:
		writeFile(json.dumps(series))
		break

 # get the series in the given category
 # note: some category may not have any series

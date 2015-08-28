#!/usr/bin/env python3

from pprint import pprint
import xml.etree.ElementTree as ET
import json
import sys
import http.client, urllib.parse


def http_get(connection, path):
	connection.request('GET', path)
	response = connection.getresponse()

	if response.status == 200:
		data = response.read()
		data = data.decode('utf-8')
		xml_check = data[:5]
		if xml_check == "<?xml":
			return data
		else:
			print("Returned data is not xml.")

	else:
		raise Exception("HTTP call failed: " + response.reason)


def writeFile(data, name):
	f = open(name, 'w')
	f.write(data)
	f.close()


url = 'www.uniprot.org'

connection = http.client.HTTPConnection(url)

protein_id = sys.argv[1]
filename = protein_id+".xml"
path = "/uniprot/"+filename

protein_info = http_get(connection, path)

writeFile(protein_info, filename)

tree = ET.ElementTree(file=filename)


name_list = []
for element in tree.iter():
	if element.tag == "{http://uniprot.org/uniprot}gene":
		for child in element:
			if child.tag == "{http://uniprot.org/uniprot}name":
				name_list.append(child.text)

f = open(protein_id+"_names.txt", 'w')

for name in name_list:
	f.write("%s\n" % name)
from pprint import pprint
import json
import io
from urllib import parse

class parser:
	def respond_all(environ, start_response):
	    status = '200 OK' # HTTP Status
	    headers = [('Content-type', 'text/plain; charset=utf-8')] # HTTP Headers
	    start_response(status, headers)

	    my_dict = {'method_name': environ['REQUEST_METHOD'], 'path_info': environ['PATH_INFO']}

	    if len(environ['CONTENT_LENGTH'])>0:
	    	my_dict['content_length'] = environ['CONTENT_LENGTH']
	    	request_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode('utf-8')
	    	request_body = request_body.strip('[] ')
	    	body_dict = parse.parse_qsl(request_body)
	    	my_dict.update(body_dict)
	    else:
	    	pass

	    if len(environ['QUERY_STRING'])>0:
	    	qs = environ['QUERY_STRING']
	    	query_dict = parse.parse_qsl(qs)
	    	my_dict.update(query_dict)
	    else:
	    	pass

	    json_response = json.dumps(my_dict, sort_keys=True, indent=4, separators=(',',': '))
	    
	    return [json_response.encode('utf-8')]

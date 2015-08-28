class some_class:


	def some_method(environ, start_response):
	    status = '200 OK' # HTTP Status
	    headers = [('Content-type', 'text/plain; charset=utf-8')] # HTTP Headers
	    start_response(status, headers)

	    path = b"You requested: " + environ['PATH_INFO'].encode('utf-8')

	    # The returned object is going to be printed
	    return [path]

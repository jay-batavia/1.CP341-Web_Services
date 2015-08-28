from my_class import some_class
from wsgiref.simple_server import make_server


# Every WSGI application must have an application object - a callable
# object that accepts two arguments. For that purpose, we're going to
# use a function (note that you're not limited to a function, you can
# use a class for example). The first argument passed to the function
# is a dictionary containing CGI-style environment variables and the
# second variable is the callable object (see PEP 333).

# def hello_world_app(environ, start_response):
# 	status = '200 OK' # HTTP Status
# 	headers = [('Content-type', 'text/plain; charset=utf-8')]
# 	start_response(status, headers)
# 	print(environ["PATH_INFO"])
# 	# The returned object is going to be printed
# 	return [b"Hello World"]

httpd = make_server('', 8000, some_class.some_method)
print("Serving on port 8000...")

# Serve until process is killed
httpd.serve_forever()
from pprint import pprint
from webob import Request
from webob import Response

req = Request.blank("http://127.0.0.1:8080")
rep = Response()

environ =   {'HTTP_HOST': 'localhost:80',
             'PATH_INFO': '/article',
             'QUERY_STRING': 'id=1',
             'REQUEST_METHOD': 'GET',
             'SCRIPT_NAME': '',
             'SERVER_NAME': 'localhost',
             'SERVER_PORT': '80',
             'SERVER_PROTOCOL': 'HTTP/1.0',}

pprint(req.environ)

pprint(dir(req))
print
pprint(dir(rep))



from os import path
import mimetypes
from webob import Request
from webob import Response


current_dir = path.dirname(path.realpath(__file__))
print "__file__ dirname:", current_dir

def basic_wsgi(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/text')])
    content = "Hello!"
    return [content]



def application1(environ, start_response):
    uri = path.join(current_dir, environ['PATH_INFO'][1:])
    print "URI:", uri
    content_type = mimetypes.guess_type(uri)[0]
    start_response('200 OK', [('Content-Type', content_type)])
    content = open(uri).read()
    return [content]


def app(environ, start_response):
    uri = path.join(current_dir, environ['PATH_INFO'][1:])
    resp = Response()
    resp(environ, start_response)
    resp.body = open(uri).read()
    resp.content_type = mimetypes.guess_type(uri)[0]
    print resp


req = Request.blank('http://127.0.0.1:8080/hi.html')
resp = req.get_response(application)
print resp

print
req = Request.blank('http://127.0.0.1:8080/css/hi.css')
resp = req.get_response(application)
print resp

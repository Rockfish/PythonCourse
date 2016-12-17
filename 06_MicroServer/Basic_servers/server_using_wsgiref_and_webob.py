
from wsgiref.simple_server import make_server

from webob import Request
from webob import Response


htmlpage = """<html>
<body style="font-family: Consolas; font-size: 10pt">
    <h1>Hello!</h1>
</body>
</html>"""

htmlpage2 = """<html>
<body style="font-family: Consolas; font-size: 10pt">
    <h1>Hello!</h1>
    {0}
</body>
</html>"""


def simple_ob(environ, start_response):
    global body
    req = Request(environ)
    print(req.path_info)
    print(req.method)
    print(req.GET)
    print(req.POST)
    print(req.headers)
    print(req.body)

    resp = Response()
    resp.content_type = 'text/html'

    ret = [("%s: %s<br>" % (key, value))
           for key, value in environ.items()]

    table = str.join('', ret)
    page = htmlpage2.format(table)

    resp.body_file.write(page)
    return resp(environ, start_response)


class SmallApp():

    def __call__(self, environ, start_response):
        global htmlpage
        req = Request(environ)
        print("path_info:", req.path_info)
        print("method:", req.method)
        print("GET:", req.GET)
        print("POST:", req.POST)
        print("headers:", req.headers)
        print("body:", req.body)

        resp = Response()
        resp.content_type = 'text/html'
        resp.body_file.write(htmlpage)
        return resp(environ, start_response)


def run():
    print("Serving on port 8000...")
    httpd = make_server('', 8000, SmallApp())
    httpd.serve_forever()

run()

# Example request:
#   http://localhost:8000/foo/bar?a=b&c=d





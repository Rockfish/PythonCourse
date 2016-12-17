from wsgiref.simple_server import make_server

""""
A simple WSGI application.
It prints out the environment dictionary after being updated by setup_testing_defaults
"""

def simple_app(environ, start_response):

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    ret = [("%s: %s\n" % (key, value)).encode("utf-8")
           for key, value in environ.items()]

    return ret


def run():
    print("Serving at http://localhost:8000/ ...")
    httpd = make_server('', 8000, simple_app)
    httpd.serve_forever()

run()

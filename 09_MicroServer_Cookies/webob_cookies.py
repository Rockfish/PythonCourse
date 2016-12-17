"""
Basic cookie example using WebOb Request and Response objects.
"""

import os
import mimetypes

from webob import Request, Response
from wsgiref.simple_server import make_server


class CookieTest(object):

    index_page = """
        <html><body>
            <h1>Cookie Test</h1>
            <a href="/set">Set cookie</a><br>
            <a href="/get">Get cookie</a><br>
        </body></html>"""

    set_cookie_form = """
        <html><body>
        <form action="set" method="post">
            <p>
                <label>Enter cookie value</label>
                <input id="value" type="text" name="value" size="50">
            </p>
            <input type="submit" value="Submit">
    </form></body></html>"""

    set_cookie_reply = """
        <html><body>
            <h3>Cookie has been set to: '{}'</h3>
            <p><a href="/get">Get cookie</a></p>
        </body></html>"""

    get_cookie_page = """
        <html><body>
            <h3>The cookie value is: '{}'</h3>
            <p><a href="/">Index</a></p>
        </body></html>"""

    def __init__(self):
        self.static_root = "static"
        self.current_dir = os.path.dirname(os.path.realpath(__file__))

    def send_text(self, text):
        "Sends html as text."
        self.response.charset = "utf8"
        self.request.content_type = 'text/html'
        self.response.text = text

    def send_static(self):
        "Send a file from the static folder"
        try:
            file_path = os.path.join(self.current_dir, self.static_root, self.request.path_info[1:])
            file_type = mimetypes.guess_type(file_path)[0]
            self.response.content_type = file_type
            data = open(file_path, 'rb').read()
            self.response.body_file.write(data)
        except Exception as e:
            self.response.status = 404
            self.response.write(str(e))

    def index(self):
        self.send_text(self.index_page)

    def set_cookie_test(self):
        """Set a cookie in the response. The cookie will be sent to the client.
        The cookie will be stored on the user's computer by their browser"""

        if self.request.method == "GET":
            # Send page with a simple form asking for a value for the cookie.
            self.send_text(self.set_cookie_form)
        else:
            # Get the value for the cookie the user posted.
            cookie_value = self.request.params.get("value")

            # Set the cookie with the user's value.
            self.response.set_cookie("MyCookie", value=cookie_value, max_age=360, path='/')

            # Send page showing the value.
            self.send_text(self.set_cookie_reply.format(cookie_value))

    def get_cookie_test(self):
        """Gets a cookie from the request. The client's browser will send all
        the cookies it finds that are associated with the request."""

        # Print the dictionary of cookies from the request object.
        print(self.request.cookies)

        # Get the value for my cookie and send it back to the user.
        value = self.request.cookies.get('MyCookie')
        self.send_text(self.get_cookie_page.format(value))


    def __call__(self, environ, start_response):
        self.request = Request(environ)
        self.response = Response()

        print(self.request.path_info)

        if self.request.path_info == "/":
            self.index()
        elif self.request.path_info == "/set":
            self.set_cookie_test()
        elif self.request.path_info == "/get":
            self.get_cookie_test()
        else:
            self.send_static()

        return self.response(environ, start_response)



if __name__ == "__main__":

    print("Serving on port 8000...")
    httpd = make_server('', 8000, CookieTest())
    httpd.serve_forever()





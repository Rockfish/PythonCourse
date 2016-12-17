
import os
import mimetypes
import sqlite3

from datetime import datetime
from webob import Request, Response
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler


class Uploader(object):

    def __init__(self):
        "Connects to the database or creates a new if needed."
        self.connection = sqlite3.connect("users.sqlite")
        self.cusor = self.connection.cursor()
        self.init_table()

    def init_table(self):
        cmd = """ CREATE TABLE IF NOT EXISTS users (
                               id integer primary key,
                               name text,
                               email text,
                               description text,
                               date text);"""
        self.connection.execute(cmd)
        self.connection.commit()

    def __call__(self, environ, start_response):
        """This method is called by the HTTPServer when
        there is a request to be handled."""

        # Create the WebOb Request and Response objects for
        # used to read the request and write the response.
        self.request = Request(environ)
        self.response = Response()

        path_info = self.request.path_info

        if path_info == "/":
            self.static("signup.html")
        elif path_info == "/signup":
            self.signup()
        else:
            self.static()

        return self.response(environ, start_response)

    def signup(self):
        """Registers a user by adding their userid and password to the user table"""

        if self.request.method == "GET":
            self.static("signup.html")

        else:
            # Get the datafile parameter from the POST body.
            name = self.request.params['name']
            email = self.request.params['email']
            description = self.request.params['description']

            cursor = self.connection.execute("SELECT * FROM users WHERE name = ?", (name, ))
            result = cursor.fetchone()

            if result == None:
                values = (name, email, description, datetime.now())
                insert_cmd = "INSERT INTO users (name, email, description, date) VALUES (?, ?, ?, ?)"
                self.connection.execute(insert_cmd, values)
                self.connection.commit()

            cursor = self.connection.execute("SELECT name, email, description FROM users ORDER BY name")
            users = cursor.fetchall()

            table_rows = ""
            for name, email, description in users:
                table_rows = table_rows + "<tr><td>{}</td><td>{}</td><td>{}</td></tr>\n".format(name, email, description)

            page = open("response.html").read()
            html = page.format(table_rows)

            self.response.content_type = "text/html"
            self.response.body_file.write(html)


    def static(self, resource=''):
        """Handles request for static pages. It is the default handler."""

        # Build a file path using either the resource parameter or the path in the request.
        if resource:
            file_path = os.path.join(resource)
        else:
            file_path = os.path.join(self.request.path_info[1:])

        print("File path:", file_path)

        # Try to open the file. If we can then guess its type and write its
        # content to the response object to send it to the client.
        # If we can't find the file then return an error to the client.
        try:
            data = open(file_path).read()
            self.response.content_type = mimetypes.guess_type(file_path)[0]
            self.response.body_file.write(data)
        except Exception as e:
            self.response.status = 404
            self.response.write(str(e))

application = Uploader()


if __name__ == "__main__":
    "Run the web app locally"

    server = WSGIServer(('', 8000), WSGIRequestHandler)
    server.set_app(application)
    print "Serving on http://localhost:8000/ ..."
    server.serve_forever()


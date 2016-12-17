
import mimetypes
import sqlite3

from webob import Request, Response
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler


class Uploader(object):

    def __init__(self):
        "Connects to the database or creates a new if needed."
        self.connection = sqlite3.connect("pagecount.sqlite")
        self.cusor = self.connection.cursor()
        self.init_table()

    def init_table(self):
        cmd = """ CREATE TABLE IF NOT EXISTS pagecount (
                               id integer primary key,
                               page text,
                               count integer);"""
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
            self.static("index.html")
        elif path_info == "/count":
            self.count()
        else:
            self.static()

        return self.response(environ, start_response)

    def pagecount(self):
        cursor = self.connection.execute("SELECT page, count FROM pagecount")
        result = cursor.fetchone()

        table_rows = ""
        for page, count in result:
            table_rows = table_rows + "<tr><td>{}</td><td>{}</td></tr>\n".format(page, count)

        page = open("response.html").read()
        html = page.format(table_rows)

        self.response.content_type = "text/html"
        self.response.body_file.write(html)

    def increment_page_count(self, page):
        cursor = self.connection.execute("SELECT count FROM pagecount WHERE page = '{}'".format(page))
        count = cursor.fetchone()

        if count == None:
            insert_cmd = "INSERT INTO pagecount (page, count) VALUES (?, ?)"
            self.connection.execute(insert_cmd, (page, 0))
            self.connection.commit()
            count = 0
        else:
            count = count[0]

        update_cmd = "UPDATE pagecount set count = ? WHERE page = ?"
        self.connection.execute(update_cmd, (count + 1, page))
        self.connection.commit()

    def static(self, resource=''):
        """Handles request for static pages. It is the default handler."""

        # Build a file path using either the resource parameter or the path in the request.
        if resource:
            file_path = resource
        else:
            file_path = self.request.path_info[1:]

        print("File path:", file_path)

        self.increment_page_count(file_path)

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


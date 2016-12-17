
import os
import mimetypes
import sqlite3

from datetime import datetime
from webob import Request, Response
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler


class MiniBlog(object):

    def __init__(self):
        "Connects to the database or creates a new if needed."
        self.connection = sqlite3.connect("blog.sqlite")
        self.cusor = self.connection.cursor()
        self.init_table()

    def init_table(self):
        cmd = """ CREATE TABLE IF NOT EXISTS messages (
                               id integer primary key,
                               title text,
                               date text,
                               content text,
                               likes integer);"""
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
            self.messages()
        elif path_info == "/new_message":
            self.new_message()
        elif path_info == "/like":
            self.increment_likes()
        else:
            self.static()

        return self.response(environ, start_response)

    def messages(self):
        "Builds the page with all the messages"

        # Get all the messages
        cursor = self.connection.execute("SELECT id, title, date, content, likes FROM messages ORDER BY date DESC")
        messages = cursor.fetchall()

        # Read in the table html
        partial_table = open("table_part.html").read()

        # Replace the table's positional fields with the message value
        # and add it to the html we are building.
        html_tables = ""
        for message in messages:
            html_tables = html_tables + partial_table.format(*message)

        # Read in the message page and replace the field with the html
        page = open("messages.html").read()
        html = page.format(html_tables)

        # Send the page to the client
        self.response.content_type = "text/html"
        self.response.body_file.write(html)

    def new_message(self):
        "Handles the new message form"

        # Handle the GET
        if self.request.method == "GET":
            self.static("new_message.html")

        else:
            # Get the datafile parameter from the POST body.
            title = self.request.params['title']
            content = self.request.params['content']

            # Add the new message to the table
            values = (title, datetime.now(), content, 0)
            insert_cmd = "INSERT INTO messages (title, date, content, likes) VALUES (?, ?, ?, ?)"
            self.connection.execute(insert_cmd, values)
            self.connection.commit()

            # Redirect the client to the message page
            # The 301 status code tells the client to switch URLs
            self.response.headers['Location'] = "/"
            self.response.status = 301
            self.messages()

    def increment_likes(self):
        """Increments the like in the database and send the new value
        back to the client Called by the Ajax method in links.js."""

        # Find the message by its id
        message_id = self.request.params['id']
        cursor = self.connection.execute("SELECT likes FROM messages WHERE id = ?", message_id)
        likes_result = cursor.fetchone()

        # Update the messages likes count
        if likes_result != None:
            likes = likes_result[0] + 1
            update_cmd = "UPDATE messages set likes = ? WHERE id = ?"
            self.connection.execute(update_cmd, (likes, message_id))
            self.connection.commit()
            self.response.body = str(likes).encode()

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


application = MiniBlog()


if __name__ == "__main__":
    "Run the web app locally"

    server = WSGIServer(('', 8000), WSGIRequestHandler)
    server.set_app(application)
    print "Serving on http://localhost:8000/ ..."
    server.serve_forever()


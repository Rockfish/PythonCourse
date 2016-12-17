"""
Micro webapp based on WebOb, Jinja2, WSGI with a simple router
"""

import os
import hmac
import hashlib
import mimetypes

from wsgiref.simple_server import WSGIServer, WSGIRequestHandler

from webob import Request
from webob import Response

from jinja2 import Environment, FileSystemLoader


class MicroServer(object):
    """Small web server."""

    def __init__(self):
        """Initializes the class and configures the paths
        and the Jinja2 environment so it can find and render pages."""

        if self.static_root is None:
            self.static_root = 'static'

        if self.templates_root is None:
            self.templates_root = 'templates'

        if self.routes is None:
            self.routes = {}

        # Set up the paths and environment for Jinja. This is how it finds the templates.
        self.template_path = os.path.join(os.path.dirname(__file__), self.templates_root)
        self.env = Environment(autoescape=True, loader=FileSystemLoader(self.template_path))

        # Figure out what directory the server is running it as save the path.
        # The path will be used later to find the site's resources.
        self.current_dir = os.path.dirname(os.path.realpath(__file__))


    def __call__(self, environ, start_response):
        """This method is called by the HTTPServer when
        there is a request to be handled."""

        # Create the WebOb Request and Response objects for
        # used to read the request and write the response.
        self.request = Request(environ)
        self.response = Response()

        # Find a handler for the path if there is one.
        handler = self.routes.get(self.request.path_info)

        # If there is call it. If not call the static handler.
        if handler:
            handler()
        else:
            self.static()

        return self.response(environ, start_response)


    def static(self, resource=''):
        """Handles request for static pages. It is the default handler."""

        # Build a file path using either the resource parameter or the path in the request.
        if resource:
            file_path = os.path.join(self.current_dir, self.static_root, resource)
        else:
            file_path = os.path.join(self.current_dir, self.static_root, self.request.path_info[1:])

        # Try to open the file. If we can then guess its type and write its
        # content to the response object to send it to the client.
        # If we can't find the file then return an error to the client.
        try:
            file_type = mimetypes.guess_type(file_path)[0]
            self.response.content_type = file_type
            data = open(file_path, 'rb').read()
            self.response.body_file.write(data)
        except Exception as e:
            self.response.status = 404
            self.response.write(str(e))


    def render_template(self, template_name, template_values={}):
        """Renders Jinja2 templates into HTML"""

        # Find the template and render it to HTML
        # then write it to the response object to send it to the client.
        template = self.env.get_template(template_name)
        html = template.render(template_values)
        self.response.write(html)

    def get_signature(self, passphrase, *parts):
        """Creates a hash from strings based on a passphrase."""

        cookiehash = hmac.new(passphrase.encode(), digestmod=hashlib.sha1)

        for part in parts:
            cookiehash.update(part.encode())

        return cookiehash.hexdigest()

    def run(self, port):
        """Starts the HTTP server and tells it what port to listen on"""

        # Create the WSGI HTTP server. Set the port it should listen on.
        # And start the server.
        server = WSGIServer(('', 8000), WSGIRequestHandler)
        server.set_app(self)
        print("Serving on http://localhost:8000/ ...")
        server.serve_forever()



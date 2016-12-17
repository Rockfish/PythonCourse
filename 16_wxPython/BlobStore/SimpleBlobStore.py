"""
    Simple app demostrating how to load files to the Google App Engine Blobstore.
"""

import urllib
import webapp2

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class MainHandler(webapp2.RequestHandler):
    """Displays the upload form with the action field set to the blob upload url.
    The file will be uploaded directly to the blobstore.
    When successful the blobstore will call us back at the path we gave it."""

    def get(self):
        # Create upload URL for POST form and set the call back path.
        upload_url = blobstore.create_upload_url('/upload')

        # Read in the form and replace the format place holder with the upload_url
        upload_form = open("upload.html").read()
        html = upload_form.format(upload_url)

        # Send the form to the client.
        self.response.out.write(html)


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    """Handles the call back from the blobstore upload call.
    Gets the key and redirect to the show page to display the uploaded file"""

    def post(self):
        # Use get_uploads to send the posted file to the blobstore
        upload_files = self.get_uploads('file')

        # Get the blob info for the first file
        blob_info = upload_files[0]

        # Redirect the client to the show method to see the blob.
        self.redirect('/show/%s' % blob_info.key())


class ShowHandler(webapp2.RequestHandler):
    """Show a page with the uploaded image"""

    def get(self, key):
        # Read in the html page
        show_page = open("show.html").read()
        
        # Replace the {0} with the key
        html = show_page.format(key)

        # Send the page to the client
        self.response.out.write(html)


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    """Get use a blob from the blobstore using the key and send it to the client"""

    def get(self, key):
        # Get the key for the blob
        key = str(urllib.unquote(key))

        # Get the blob info from the blobstore
        blob_info = blobstore.BlobInfo.get(key)

        # Send the blob to the client.
        self.send_blob(blob_info)


# Create the webapp2 application to handle requests
app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/upload', UploadHandler),
                               ('/serve/([^/]+)?', ServeHandler),
                               ('/show/([^/]+)?', ShowHandler)],
                              debug=True)


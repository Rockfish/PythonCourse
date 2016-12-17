#import cgi
import datetime
import os
#import re
#import sys
#import smtplib
import hashlib
#import urllib.request, urllib.parse, urllib.error
#import urllib.parse
import mimetypes

#import wsgiref.handlers
#from wsgiref.util import setup_testing_defaults
#from wsgiref.simple_server import make_server
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler

import webapp2
from basehandler import BaseHandler

from sendemail import send_email, Company_email, to_Company_subject, john_email, to_user_subject

_DEBUG = True
stored_salt = "Rockfish!".encode()

current_dir = os.path.dirname(__file__)

def hash_string(instr, salt):
    h = hashlib.md5()
    h.update(salt)
    h.update(instr.encode())
    return h.hexdigest().upper()

def get_passkey(user_email):
    return hash_string(user_email.lower(), stored_salt)

def get_file_timestamp(name):
    root = os.path.join(current_dir, 'files')
    filename = os.path.join(root, name)
    filetimestamp = os.stat(filename).st_mtime
    date = datetime.datetime.fromtimestamp(filetimestamp)
    return date.strftime("%b %d, %Y - %I:%M %p")


class Default(BaseHandler):
    def get(self):
        print('Default')
        user_email = self.get_secure_cookie('CompanyUpdates')
        if user_email:
            self.redirect("/downloads")
        else:
            self.redirect("/login")
            #self.response.write("hi")


class Login(BaseHandler):

    def get(self):
        "Login page"
        data = {'message' : ''}
        print(get_passkey('john@rockfishnw.com'))
        return self.render_response("login.html", **data)

    def post(self):
        email = self.request.params['email'].lower()
        regkey = self.request.params['regkey']
        print(regkey)
        success = (regkey == get_passkey(email))

        data = {'email' : email,
                'regkey' : regkey,
                'data' : [email, regkey, success ]}

        if success:
            expires_date = datetime.datetime.utcnow() + datetime.timedelta(365)
            expires_str = expires_date.strftime("%d %b %Y %H:%M:%S GMT")
            self.set_secure_cookie(name="CompanyUpdates", value=email, expires_days=5)
            self.redirect("/downloads")
        else:
            data = {'message' : 'The registration key or the email was incorrect.<br />Please correct them and try again.'}
            return self.render_response("login.html", **data)


class Downloads(BaseHandler):

    def get(self, filename=None):
        user_email = self.get_secure_cookie('CompanyUpdates')
        if not user_email:
            self.redirect("/login")

        if filename == None:
            from timestamps import get_timestamps
            timestamps = get_timestamps()
            return self.render_response("downloads.html", **timestamps)
        else:
            try:
                if filename.lower().startswith('Music'):
                    filepath = os.path.join('distribution/Music', filename)
                else:
                    filepath = os.path.join('distribution/Video', filename)
                self.response.headers['Content-Length'] = os.stat(filepath).st_size
                self.response.headers['Content-Type'] = 'application/octet-stream'
                self.response.headers['Content-Disposition'] = 'attachment; filename=%s' % filename
                self.response.app_iter = FileIterable(filepath)
                self.response.content_length = os.path.getsize(filepath)
            except Exception as ex:
                print(ex)
                self.error(404)


class Registration(BaseHandler):

    def get(self):
        data = {'message' : ''}
        return self.render_response("register.html", **data)

    def post(self):
        regdata = {}
        items = ['firstname', 'lastname', 'address1', 'address2', 'city',
                 'zipcode', 'country', 'email', 'serialnumber']
        for item in items:
            regdata[item] = self.request.get(item)

        regdata['regkey'] = get_passkey(regdata.get('email'))

        user_email = "%s %s <%s>" % (regdata.get('firstname'),
                                     regdata.get('lastname'),
                                     regdata.get('email'))

        # Send registration data to Company
        send_email(Company_email, to_Company_subject, 'Company_email', regdata)
        send_email(john_email, to_Company_subject, 'Company_email', regdata)

        # Send confirmation email to user
        send_email(user_email, to_user_subject, 'user_email', regdata)

        # Display confirmation page to user
        template_values = { 'data' : regdata } #, 'env' : self.request.environ }
        return self.render_response("confirmation.html", **template_values)
        #return self.render_response("regdata.html", **template_values)


class License(BaseHandler):

    def get(self):
        data = {'message' : ''}
        return self.render_response("license.html", **data)


class SendMail(BaseHandler):

    def send_registration_data(self, email, regkey):
#         sendEmail(email,
#                   'Login Registration',
#                   'User Email: %s\nUser login key: %s' % (email, get_passkey(email)))
        return """<html><body><h1>Email sent</h1><a href="swlogin">Login</a></body></html>"""


class Status(BaseHandler):

    def get(self, uri):
        if uri.startswith('Music'):
            filepath = os.path.join('distribution/Music', uri)
        else:
            filepath = os.path.join('distribution/Video', uri)
        if os.path.isfile(filepath):
            self.response.content_type = mimetypes.guess_type(uri)[0]
            return self.response.write(open(filepath).read())
        else:
            return self.response.write("Not found");

class FileIterable(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        return FileIterator(self.filename)

class FileIterator(object):
    chunk_size = 4096

    def __init__(self, filename):
        self.filename = filename
        self.fileobj = open(self.filename, 'rb')

    def __iter__(self):
        return self

    def __next__(self):
        chunk = self.fileobj.read(self.chunk_size)
        if not chunk:
            raise StopIteration
        return chunk


class Static(BaseHandler):

    def get(self, uri):
        filepath = os.path.join('static', uri)
        if os.path.isfile(filepath):
            self.response.content_type = mimetypes.guess_type(uri)[0]
            self.response.app_iter = FileIterable(filepath)
            self.response.content_length = os.path.getsize(filepath)
            return self.response
        else:
            return self.response.write("Not found");


def run(config, debug):
    application = webapp2.WSGIApplication([
                                ('/', Default),
                                ('/login', Login),
                                ('/downloads', Downloads),
                                ('/downloads/(.*)', Downloads),
                                ('/registration', Registration),
                                ('/license-agreement', License),
                                ('/status/(.*)', Status),
                                ('/(.*)', Static),
                                ], debug=debug)

    server = WSGIServer(('', 8000), WSGIRequestHandler)
    server.set_app(application)
    print("Serving on port 8000...")
    server.serve_forever()


if __name__ == '__main__':
    config = {
        'environment': 'production',
        'log_screen': False,
        'server_host': '127.0.0.1',
        'server_port': 37977
    }
    run(config, True)

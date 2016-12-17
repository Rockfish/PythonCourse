import os
import http.cookies
import base64
import time
import hashlib
import hmac
import datetime
import re
import calendar
import email.utils
import logging
from urllib.error import HTTPError

import webapp2
from webapp2_extras import jinja2

_DEBUG = True
current_dir = os.path.dirname(__file__)

stored_salt = "MusicRocks"

current_dir = os.path.dirname(__file__)

def hash_string(instr, salt):
    h = hashlib.md5()
    h.update(salt)
    h.update(instr)
    return h.hexdigest().upper()

def get_passkey(user_email):
    return hash_string(user_email.lower(), stored_salt)

def _utf8(s):
    if isinstance(s, str):
        return s.encode("utf-8")
    assert isinstance(s, str)
    return s

def _unicode(s):
    if isinstance(s, str):
        try:
            return s.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPError(400, "Non-utf8 argument")
    assert isinstance(s, str)
    return s

def _time_independent_equals(a, b):
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    return result == 0


class BaseHandler(webapp2.RequestHandler):
    """Extends the Google App Engine webapp.RequestHandler."""

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

    def clear_cookie(self,name,path="/",domain=None):
        """Deletes the cookie with the given name."""
        expires = datetime.datetime.utcnow() - datetime.timedelta(days=365)
        self.set_cookie(name, value="", path=path, expires=expires,
                        domain=domain)

    def clear_all_cookies(self):
        """Deletes all the cookies the user sent with this request."""
        for name in list(self.cookies.keys()):
            self.clear_cookie(name)

    def cookies(self):
        """A dictionary of Cookie.Morsel objects."""
        if not hasattr(self,"_cookies"):
            self._cookies = http.cookies.BaseCookie()
            if "Cookie" in self.request.headers:
                try:
                    self._cookies.load(self.request.headers["Cookie"])
                except:
                    self.clear_all_cookies()
        return self._cookies

    def _cookie_signature(self, *parts):
        """Hashes a string based on a pass-phrase."""
        cookiehash = hmac.new("MySecretPhrase".encode(), digestmod=hashlib.sha1)
        for part in parts:
            cookiehash.update(part)
        return cookiehash.hexdigest()

    def get_cookie(self, name, default=None):
        """Gets the value of the cookie with the given name,else default."""
        if name in self.request.cookies:
            return self.request.cookies[name]
        return default

    def set_cookie(self, name, value, domain=None, expires=None, path="/", expires_days=None):
        """Sets the given cookie name/value with the given options."""
        #name = _utf8(name)
        #value = _utf8(value)
        if re.search(r"[\x00-\x20]", name + value): # Don't let us accidentally inject bad stuff
            raise ValueError("Invalid cookie %r:%r" % (name,value))
        new_cookie = http.cookies.BaseCookie()
        new_cookie[name] = value
        if domain:
            new_cookie[name]["domain"] = domain
        if expires_days is not None and not expires:
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=expires_days)
        if expires:
            timestamp = calendar.timegm(expires.utctimetuple())
            new_cookie[name]["expires"] = email.utils.formatdate(timestamp, localtime=False, usegmt=True)
        if path:
            new_cookie[name]["path"] = path
        for morsel in list(new_cookie.values()):
            self.response.headers.add_header('Set-Cookie', morsel.OutputString(None))

    def set_secure_cookie(self, name, value, expires_days=30, **kwargs):
        """Signs and timestamps a cookie so it cannot be forged"""
        timestamp = str(int(time.time()))
        value = str(base64.b64encode(value.encode()))
        signature = str(self._cookie_signature(name.encode(), value.encode(), timestamp.encode()))
        value = "|".join([value, timestamp, signature])
        self.set_cookie(name, value, expires_days=expires_days, **kwargs)

    def get_secure_cookie(self,name, include_name=True, value=None):
        """Returns the given signed cookie if it validates,or None"""
        if value is None:
            value = self.get_cookie(name)
        if not value:
            return None
        parts = value.split("|")
        if len(parts) != 3:
            return None
        if include_name:
            signature = self._cookie_signature(name.encode(), parts[0].encode(), parts[1].encode())
        else:
            signature = self._cookie_signature(parts[0], parts[1])
        if not _time_independent_equals(parts[2], signature):
            logging.warning("Invalid cookie signature %r", value)
            return None
        timestamp = int(parts[1])
        if timestamp < time.time() - 31 * 86400:
            logging.warning("Expired cookie %r", value)
            return None
        try:
            return base64.b64decode(parts[0])
        except:
            return None


class MyHandler(BaseHandler):
    '''
        Example on how to use the cookie setting and getting methods
    '''
    def get(self):
        self.set_cookie(name="MyCookie",value="NewValue",expires_days=10)
        self.set_secure_cookie(name="MySecureCookie",value="SecureValue",expires_days=10)

        value1 = self.get_cookie('MyCookie')
        value2 = self.get_secure_cookie('MySecureCookie')

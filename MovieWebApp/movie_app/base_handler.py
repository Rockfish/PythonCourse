import hmac
import hashlib

import webapp2
from webapp2_extras import jinja2

from movie_database import MovieDatabase
from movie_client import get_movie_data


class BaseHandler(webapp2.RequestHandler):
    """Extends the Google App Engine webapp.RequestHandler."""

    def __init__(self, environ, *args, **kwargs):

        super(BaseHandler, self).__init__(environ, *args, **kwargs)

        # Set the static_root so the server knows where to find the pages.
        self.static_root = "static"
        self.templates_root = 'templates'
        self.passphrase = "LoveMovies"

        # Create MovieDatabase so we can work with the database.
        self.database = MovieDatabase()
        self.database.create_tables()

        # Fill the database with some data if needed
        movies = self.database.get_movies()
        if len(movies) == 0:
            self.initialize_database()

    def initialize_database(self):
        "Fill the database with some movies data."

        movie_titles = ["The Matrix",
                         "The Fifth Element",
                         "Spirited Away",
                         "Princess Mononoke",
                         "Guardians of the Galaxy"]

        for title in movie_titles:
            data = get_movie_data(title)
            if not "Error" in data:
                try:
                    self.database.add_movie_data(data)
                except:
                    print("Error adding: ", data)
            else:
                print("Error getting: {0}. Please check the title.".format(title))

        self.database.commit()


    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, _template, template_values={}, check_login=True):

        if check_login:
            # Get the userid from the cookie if it exists
            userid = self.check_if_logged_in()

            # Add the result to the template values
            template_values["logged_in_user"] = userid

        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **template_values)
        self.response.write(rv)

    def check_if_logged_in(self):
        """Checks to see if the MovieWebApp cookie is set"""

        # Get the MovieWebApp cookie if it exists from the request
        cookie_value = self.request.cookies.get('MovieWebApp')

        # If cookie exists, split it to check it and return the userid.
        if cookie_value:
            result = cookie_value.split('|')

            if len(result) == 3 and result[0] == "logged in":
                userid = result[1]
                cookie_signature = result[2]

                # Recreate the signature
                signature = self.get_signature(self.passphrase, "logged in", userid)

                # Verify the cookie signature is valid before using cookie values.
                if cookie_signature == signature:
                    return userid

        # User not logged in or bad cookie
        return None

    def get_signature(self, passphrase, *parts):
        """Creates a hash from strings based on a passphrase."""

        cookiehash = hmac.new(passphrase.encode(), digestmod=hashlib.sha1)

        for part in parts:
            cookiehash.update(part.encode())

        return cookiehash.hexdigest()


import os
import json
import webapp2
import mimetypes

from base_handler import BaseHandler
from movie_client import get_movie_data
from datetime import datetime


class Static(BaseHandler):

    def get(self, uri):
        """Handles request for static pages. It is the default handler."""

        # Build a file path using either the resource parameter or the path in the request.
        if uri:
            file_path = os.path.join('static', uri)
        else:
            file_path = os.path.join('static', self.request.path_info[1:])

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

class IndexPage(BaseHandler):

    def get(self):
        return self.render_template("index.tmpl")

class MoviesPage(BaseHandler):

    def get(self):
        data = self.database.get_movies()
        self.render_template('movies.tmpl', dict(movies = data))

class ActorsPage(BaseHandler):

    def get(self):
        data = self.database.get_actors()
        self.render_template('actors.tmpl', dict(actors = data))

class AddMovie(BaseHandler):
    """Handles both the GET and POST methods for adding a new movie.
    It first checks to see if the movie is already in the database.
    If the movie is not in the database, then download the data
    from http://www.omdbapi.org and added it to the database."""

    def get(self):
        self.render_template('addmovie.tmpl')

    def post(self):
        # Handling add movie form post
        submitted_data = self.request.POST
        title = submitted_data["movietitle"]
        message = ""

        if title is not None:
            result = self.database.get_movie(title)

            if result is None:
                data = get_movie_data(title)

                if data is not None and "Error" not in data:
                    self.database.add_movie_data(data)
                    message = "Added '{}'".format(title)
                else:
                    message = "Error adding '{}'".format(title)
            else:
                message = "The movie '{}' is already in database.".format(title)

        self.render_template('addmovie_result.tmpl', {"message": message})

class MovieDetails(BaseHandler):

    def get(self):
        query = self.request.GET
        title = query["title"]

        if title is not None:
            result = self.database.get_movie(title)
            data = {'title': result[0],
                    'year': result[1],
                    'plot': result[2],
                    'poster': result[3]}
            self.render_template('movie_details.tmpl', data)

class UploadFile(BaseHandler):
    """Handle the file upload. Saves the file to the uploads folder
    and saves the tile, date, and file path to the database."""

    def get(self):
        self.render_template("upload.tmpl")

    def post(self):
        # Get the datafile parameter from the POST body.
        title = self.request.params['title']
        datafile = self.request.params['datafile']

        # Build the path to where we will save the file.
        filepath = os.path.join(self.static_root, "uploads", datafile.filename)

        # Read the data from the request body and write it to the filesystem.
        with open(filepath,'wb') as fh:
            data = datafile.file.read()
            fh.write(data)

        # Build a url for the img source that is relative to the root of the site.
        file_url = "/uploads/" + datafile.filename

        # Record the uploaded file information to the database
        self.database.add_upload(title, datetime.now(), file_url)

        # Render the results
        self.render_template("upload_result.tmpl", {'name': title, 'file_url': file_url })

class Register(BaseHandler):
    """Registers a user by adding their userid and password to the user table"""

    def get(self):
        self.render_template("register.tmpl", {'success': "none"})

    def post(self):
        # Get the datafile parameter from the POST body.
        userid = self.request.params['userid']
        password = self.request.params['password']

        result = self.database.get_user(userid.lower())

        if result == None:
            password_signature = self.get_signature(self.passphrase, password)
            self.database.add_user(userid.lower(), password_signature)
            self.render_template("register.tmpl", {'success': "yes", 'userid': userid })
        else:
            self.render_template("register.tmpl", {'success': "no", 'error': "User already registered." })

class Login(BaseHandler):
    """Logs a user in by checking their userid and password against the database.
    Set a cookie called MovieWebApp when user is logged in."""

    def get(self):
        self.render_template("login.tmpl")

    def post(self):
        # Get the datafile parameter from the POST body.
        userid = self.request.params['userid']
        password = self.request.params['password']

        # Check to see if the user is in the database
        result = self.database.get_user(userid.lower())

        # Check to see if the password signatures match. If they do set the MovieWebApp cookie.
        if result:
            signature_database = result[1]
            password_signature = self.get_signature(self.passphrase, password)

            if signature_database == password_signature:
                # Create a signed cookie.
                message = "logged in"
                signature = self.get_signature(self.passphrase, message, userid)
                cookie_value = "|".join((message, userid, signature))

                # Set the cookie value. It will be stored on the client when it gets the response.
                self.response.set_cookie("MovieWebApp", value=cookie_value, max_age=360, path='/')

                # Call the base render_template since the cookie won't be ready until after the response is sent to the client.
                # super().render_template("login.tmpl", {'loggedin': "yes", 'logged_in_user': userid }) # Python 3
                self.render_template("login.tmpl", {'loggedin': "yes", 'logged_in_user': userid }, False)

                # Return on success
                return

        # If userid or password was bad, render an error message.
        self.render_template("login.tmpl", {'loggedin': "error", 'error_message': "User id not found or password is incorrect." })

class Logout(BaseHandler):
    """Logout clears the MovieWebApp cookie"""

    def get(self):
        # Clear the cookie value
        self.response.set_cookie("MovieWebApp", value="", max_age=360, path='/')

        # Call base render_template to see the change since the cookie is only changed after the response is sent to the client.
        # super().render_template("index.tmpl", {'loggedin': "no", 'logged_in_user': None }) # Python 3
        super(Logout, self).render_template("index.tmpl", {'loggedin': "no", 'logged_in_user': None })

class Slides(BaseHandler):
    """Handles both the slide page and the Ajax calls to change the picture"""

    def get(self):
        self.render_template('slides.tmpl')

    def post(self):
        # Handling the POST request from the Ajax call

        # Get the data Ajax call sent in the post.
        direction = self.request.params['action']
        slide_number = self.request.params['number']

        # Get a list of all the files in the picture folder
        file_path = os.path.join(self.static_root, "pictures")
        dir_info = next(os.walk(file_path))
        files = dir_info[2]

        # Use the post data to decide the index of the next picture
        if direction == "next":
            number = int(slide_number) + 1;
        else:
            number = int(slide_number) - 1;

        if number >= len(files):
            number = 0

        if number < 0:
            number = len(files) - 1

        # Get the name of the picture we want to display
        picture = files[number];

        # Store the new data in a dictionary and convert to JSON
        data = {'number': number, 'url': '/pictures/' + picture}
        json_data = json.dumps(data)

        # Send the JSON response back to the Ajax call.
        self.response.body = json_data.encode()

class Posters(BaseHandler):
    """Handles both the poster page and the Ajax calls to change the movie"""

    def get(self):
        self.render_template('posters.tmpl')

    def post(self):
        # Handling the POST request from the Ajax call

        # Get the data Ajax call sent in the post.
        direction = self.request.params['action']
        slide_number = self.request.params['number']

        movies = self.database.get_movies()

        # Use the post data to decide the index of the next picture
        if direction == "next":
            number = int(slide_number) + 1;
        else:
            number = int(slide_number) - 1;

        if number >= len(movies):
            number = 0

        if number < 0:
            number = len(movies) - 1

        # Get the data for the movie we want
        movie = movies[number]

        # Store the new data in a dictionary and convert to JSON
        data = {'title': movie[0],
                'year': movie[1],
                'plot': movie[2],
                'poster': movie[3],
                'number': number}
        json_data = json.dumps(data)

        # Send the JSON response back to the Ajax call.
        self.response.body = json_data.encode()


# Create a webapp2 WSGI application and initialize it with
# the url routing data. The app can be served locally or
# on Google App Engine.

app = webapp2.WSGIApplication([
                   ('/', IndexPage),
                   ('/index', IndexPage),
                   ('/movies', MoviesPage),
                   ('/actors', ActorsPage),
                   ('/addmovie', AddMovie),
                   ('/details', MovieDetails),
                   ('/upload', UploadFile),
                   ('/register', Register),
                   ('/login', Login),
                   ('/logout', Logout),
                   ('/slides', Slides),
                   ('/posters', Posters),
                   ('/(.*)', Static),
                   ], debug=True)



if __name__ == "__main__":
    "Run the web app locally"

    from wsgiref.simple_server import WSGIServer, WSGIRequestHandler

    server = WSGIServer(('', 8000), WSGIRequestHandler)
    server.set_app(app)
    print("Serving on port 8000...")
    server.serve_forever()

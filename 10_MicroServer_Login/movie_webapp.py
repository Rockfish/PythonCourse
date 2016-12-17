import os
import json

from micro_server import MicroServer
from movie_database import MovieDatabase
from movie_client import get_movie_data
from datetime import datetime


class MovieWebApp(MicroServer):
    """A small web application built from the Micro server"""

    def __init__(self):
        # Set the static_root so the server knows where to find the pages.
        self.static_root = "static"
        self.templates_root = 'templates'
        self.passphrase = "LoveMovies"

        # Set the routes that map request paths to methods
        self.routes = {
                '/': self.index,
                '/index': self.index,
                '/movies': self.display_movies,
                '/actors': self.display_actors,
                '/addmovie': self.add_movie,
                '/details': self.display_movie_details,
                '/upload': self.upload_file,
                '/register': self.register,
                '/login': self.login,
                '/logout': self.logout,
                '/slides': self.slides,
                '/posters': self.posters
            }

        # Call the base class initializer to make sure
        # everything it set correctly.
        super().__init__()

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
                self.database.add_movie_data(data)
            else:
                print("Error getting: {0}. Please check the title.".format(title))

        self.database.commit()

    def index(self):
        self.render_template('index.tmpl')

    def display_movies(self):
        data = self.database.get_movies()
        self.render_template('movies.tmpl', dict(movies = data))

    def display_actors(self):
        data = self.database.get_actors()
        self.render_template('actors.tmpl', dict(actors = data))

    def add_movie(self):
        """Handles both the GET and POST methods for adding a new movie.
        It first checks to see if the movie is already in the database.
        If the movie is not in the database, then download the data
        from http://www.omdbapi.org and added it to the database."""

        if self.request.method == "GET":
            self.render_template('addmovie.tmpl')
        else:
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

    def display_movie_details(self):
        query = self.request.GET
        title = query["title"]

        if title is not None:
            result = self.database.get_movie(title)
            data = {'title': result[0],
                    'year': result[1],
                    'plot': result[2],
                    'poster': result[3]}
            self.render_template('movie_details.tmpl', data)

    def upload_file(self):
        """Handle the file upload. Saves the file to the uploads folder
        and saves the tile, date, and file path to the database."""

        # Handle the GET
        if self.request.method == "GET":
            self.render_template("upload.tmpl")

        # Handle the POST
        else:
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

    def register(self):
        """Registers a user by adding their userid and password to the user table"""

        if self.request.method == "GET":
            self.render_template("register.tmpl", {'success': "none"})

        else:
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

    def login(self):
        """Logs a user in by checking their userid and password against the database.
        Set a cookie called MovieWebApp when user is logged in."""

        if self.request.method == "GET":
            self.render_template("login.tmpl")

        else:
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
                    super().render_template("login.tmpl", {'loggedin': "yes", 'logged_in_user': userid })

                    # Return on success
                    return

            # If userid or password was bad, render an error message.
            self.render_template("login.tmpl", {'loggedin': "error", 'error_message': "User id not found or password is incorrect." })

    def logout(self):
        """Logout clears the MovieWebApp cookie"""

        # Clear the cookie value
        self.response.set_cookie("MovieWebApp", value="", max_age=360, path='/')

        # Call base render_template to see the change since the cookie is only changed after the response is sent to the client.
        super().render_template("index.tmpl", {'loggedin': "no", 'logged_in_user': None })

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

    def slides(self):
        """Handles both the slide page and the Ajax calls to change the picture"""

        if self.request.method == "GET":
            self.render_template('slides.tmpl')

        else:
            # Handling the POST request from the Ajax call

            # Get the data Ajax call sent in the post.
            direction = self.request.params['action']
            slide_number = self.request.params['number']

            # Get a list of all the files in the picture folder
            file_path = os.path.join(self.current_dir, self.static_root, "pictures")
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

    def posters(self):
        """Handles both the poster page and the Ajax calls to change the movie"""

        if self.request.method == "GET":
            self.render_template('posters.tmpl')

        else:
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

    def render_template(self, template_name, template_values={}):
        """Overrides base render_template. Adds login check to the page and
        then calls the base render_template"""

        # Get the userid from the cookie if it exists
        userid = self.check_if_logged_in()

        # Add the result to the template values
        template_values["logged_in_user"] = userid

        # Call the base render_template
        super().render_template(template_name, template_values)


# Create a webapp object and run it.
app = MovieWebApp()
app.run(8000)






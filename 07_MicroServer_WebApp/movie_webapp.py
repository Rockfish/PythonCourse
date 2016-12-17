from micro_server import MicroServer
from movie_database import MovieDatabase
from movie_client import get_movie_data


class MovieWebApp(MicroServer):
    """A small web application built from the Micro server"""

    def __init__(self):
        # Set the static_root so the server knows where to find the pages.
        self.static_root = "static"
        self.templates_root = 'templates'

        # Set the routes that map request paths to methods
        self.routes = {
                '/': self.index,
                '/index': self.index,
                '/movies': self.display_movies,
                '/actors': self.display_actors,
                '/addmovie': self.add_movie,
                '/details': self.display_movie_details
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
        self.render_template('index.html')

    def display_movies(self):
        data = self.database.get_movies()
        self.render_template('movies.html', dict(movies = data))

    def display_actors(self):
        data = self.database.get_actors()
        self.render_template('actors.html', dict(actors = data))

    def add_movie(self):
        "Handles both the GET and POST methods for adding a new movie"

        if self.request.method == "GET":
            self.render_template('addmovie.html')
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

            self.render_template('addmovie_result.html', {"message": message})

    def display_movie_details(self):
        query = self.request.GET
        title = query["title"]

        if title is not None:
            result = self.database.get_movie(title)
            data = {'title': result[0],
                    'year': result[1],
                    'plot': result[2],
                    'poster': result[3]}
            self.render_template('movie_details.html', data)



# Create a webapp object and run it.
app = MovieWebApp()
app.run(8000)






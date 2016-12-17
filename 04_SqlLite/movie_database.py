import sqlite3
from movie_client import get_movie_data

class MovieDatabase(object):

    def __init__(self):
        "Connects to the database or creates a new if needed."
        self.connection = sqlite3.connect("test.sqlite")

    def create_movie_table(self):
        "Creates the movie table in the database."

        create_movie_data_table_command = '''
        CREATE TABLE Movies (
            id integer primary key,
            title text,
            actors text,
            plot text);'''

        try:
            self.connection.execute(create_movie_data_table_command)
        except:
            "Table already exists"
            pass

    def delete_movie_table(self):
        "Drops the table if needed."
        self.connection.execute("DROP TABLE IF EXISTS Movies")
        self.connection.commit()

    def add_movie_data(self, title, actors, plot):
        "Saves the values to the database."
        values = (title, actors, plot)
        self.connection.execute('INSERT INTO Movies (title, actors, plot) VALUES (?, ?, ?)', values)

    def close_connection(self):
        "Closes the connection"
        self.connection.close()

    def download_movies(self, movie_titles):
        """"Downloads the movie data for the movies in the list.
        Saves the data to the database"""

        for title in movie_titles:

            # Call the client method to get a dictionary with the movies' data.
            data = get_movie_data(title)

            # Check to see if there is a key in the dictionary called 'Error'
            if not "Error" in data:

                title = data['Title']
                actors = data['Actors']
                plot = data['Plot']

                # Add the values to the database.
                self.add_movie_data(title, actors, plot)

            else:
                print("Error getting: {0}. Please check the title.".format(title))

        # Make sure to commit to save the data.
        self.connection.commit()

    def print_movies_with_actor(self, actor):
        "Searches the database for movies with the actor. Prints the result"

        command = "SELECT title FROM Movies WHERE actors LIKE '%{}%'".format(actor)
        cursor = self.connection.execute(command)

        for row in cursor:
            print(row)

        cursor.close()



if __name__ == "__main__":

    favorite_movie_titles = ["Brazil",
                             "The Fifth Element",
                             "Spirited Away",
                             "Princese Monoko",
                             "The Guardians of the Galaxy"]

    # Create a movie database object to work with.
    movie_db = MovieDatabase()

    # Delete any old tables and create a new table.
    movie_db.delete_movie_table()
    movie_db.create_movie_table()

    # Download movie data from omdbapi.com and save it to the database.
    movie_db.download_movies(favorite_movie_titles)

    # Find the movies with the actor in it.
    movie_db.print_movies_with_actor('Bruce Willis')

    # Close the connection when we are done.
    movie_db.close_connection()

    print("Done")

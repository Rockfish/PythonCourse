import os
import logging
# To use MySQLdb first install MySQL and MySQL-python

import MySQLdb

import sql_commands as cmds


class MovieDatabase(object):

    def __init__(self):

        env = os.getenv('SERVER_SOFTWARE')

        if (env and env.startswith('Google App Engine/')):
            # Connect from App Engine
            db = MySQLdb.connect(unix_socket='/cloudsql/moviewebapp:movie-database',
                                 db='my_movies',
                                 user='root')
        else:
            # Connect to local MySQL
            db = MySQLdb.connect(host='127.0.0.1',
                                 port=3306,
                                 db='my_movies',
                                 user='john',
                                 passwd='R0cking')

        self.connection = db
        self.cursor = self.connection.cursor()

    def create_tables(self):
        "Creates all the tables in the database."
        try:
            # Create each table one by one
            for table_cmd in cmds.create_tables:
                self.cursor.execute(table_cmd)

            self.connection.commit()
        except:
            "Table already exists"
            pass

    def delete_tables(self):
        "Drops all the tables in the database."
        # Drop each table one by one
        for drop_cmd in cmds.drop_tables:
            self.cursor.execute(drop_cmd)
        self.connection.commit()

    def commit(self):
        "Commits the transactions."
        self.connection.commit()

    def close(self):
        "Closes the connection"
        # Commit first before close the database to make sure
        # all the data is written to database.
        self.connection.commit()

        # Closes the connection to the database. Any more calls
        # the database will fail. Need to reconnect first.
        self.connection.close()

    def add_movie_data(self, data):
        "Saves the values to the database."

        # First add the movie data
        command = cmds.insert_movie.format(data["Title"], data["Year"], data["Plot"], data["Poster"])
        result = self.cursor.execute(command)

        # Save the id of the last row that was added to the database.
        # It is the id of the movie we just added.
        movie_id = self.cursor.lastrowid

        logging.info('result: %s    movie_id: %s', result, movie_id)

        for actor in data["Actors"].split(','):

            # Remove any leading or trailing spaces
            actor = actor.strip()

            # Slip name into first and last names
            values = actor.split(' ', 1)

            # First check to see if the actor is already in the table

            self.cursor.execute(cmds.get_actor_id.format(*values))
            result = self.cursor.fetchone()

            # If actor_id is None it means the actor is not in the table
            # so we will add actor to the table.
            if result is None:

                # Add the actor to the actor table and save the id we get back.
                result = self.cursor.execute(cmds.insert_actor.format(*values))

                # Save the id of the last row added.
                # It is the actor id of the actor just added.
                actor_id = self.cursor.lastrowid

            else:
                # Results are tuples. We just want the first value.
                actor_id = result[0]

            # Add the actor_id movie_id pair to the actor_in_movie table.
            # Adding the pair connects the actor to a movie.
            command = cmds.insert_actor_in_movie.format(actor_id, movie_id)
            result = self.cursor.execute(command)

        self.commit()

    def get_movie(self, title):
        "Get the data for one movie"
        self.cursor.execute(cmds.get_movie.format(title))
        return self.cursor.fetchone()

    def get_movies(self):
        "Get the data for all movies"
        self.cursor.execute(cmds.get_movies)
        return self.cursor.fetchall()

    def get_actors(self):
        "Get the data for all actors"
        self.cursor.execute(cmds.get_actors)
        result = self.cursor.fetchall()
        return result

    def get_movies_with_actor(self, actor_name):
        "Searches the database for movies with the actor."

        # Search for the actor's id using first and last name.
        first_name, last_name = actor_name.split()
        self.cursor.execute(cmds.get_actor_id.format(first_name, last_name))

        # Get the id from the cursor.
        actor_id = self.cursor.fetchone()

        # Use the actor_id to search for the movies they are in.
        self.cursor.execute(cmds.movies_with_actor.format(*actor_id))

        # Get all the rows at once as a list.
        # It is a list of tuples. One for each row result.
        # [(id, title), (id, title), (id, title)]
        movies_with_actor = self.cursor.fetchall()

        # Return the list of movies.
        return movies_with_actor

    def add_upload(self, title, date, filepath):
        command = cmds.insert_upload.format(title, date, filepath)
        self.cursor.execute(command)
        self.commit()

    def add_user(self, userid, password):
        command = cmds.insert_user.format(userid, password)
        self.cursor.execute(command)
        self.commit()

    def get_user(self, userid):
        self.cursor.execute(cmds.get_user.format(userid) )
        result = self.cursor.fetchone()
        return result


if __name__ == "__main__":

    # Create a movie database object to work with.
    movie_db = MovieDatabase()

    # Delete any old tables and create a new table.
    movie_db.delete_tables()
    movie_db.create_tables()

    the_matrix = {"Title": "The Matrix",
                  "Year": "1999",
                  "Actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving",
                  "Plot": "A computer hacker learns something new.",
                  "Poster": "pic.jpg"}


    johnnie = {"Title": "Johnnie",
               "Year": "1988",
               "Actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving",
               "Plot": "Wired courier goes nuts.",
               "Poster": "pic.jpg"}

    grail = {"Title": "The Holy Grail",
               "Year": "1981",
               "Actors": "John Cleese, Michael Palin, Graham Chapman",
               "Plot": "The Knights search for the grail.",
               "Poster": "pic.jpg"}


    movie_db.add_movie_data(the_matrix)
    movie_db.add_movie_data(johnnie)
    movie_db.add_movie_data(grail)

    movie_db.commit()

    # Find the movies with the actor in it.
    movies = movie_db.get_movies_with_actor("Keanu Reeves")

    for movie in movies:
        print(movie)

    # Close the connection when we are done.
    movie_db.close()

    print("Done")

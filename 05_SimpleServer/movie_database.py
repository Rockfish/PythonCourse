import sqlite3
import sql_commands as cmds


class MovieDatabase(object):

    def __init__(self):
        "Connects to the database or creates a new if needed."
        self.connection = sqlite3.connect("test.sqlite")
        self.cusor = self.connection.cursor()


    def create_tables(self):
        "Creates all the tables in the database."
        try:
            # Create each table one by one
            for table_cmd in cmds.create_tables:
                self.connection.execute(table_cmd)

            self.connection.commit()
        except:
            "Table already exists"
            pass


    def delete_tables(self):
        "Drops all the tables in the database."
        # Drop each table one by one
        for drop_cmd in cmds.drop_tables:
            self.connection.execute(drop_cmd)
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
        values = (data["Title"], data["Year"], data["Plot"])
        result = self.connection.execute('INSERT INTO movie (title, year, plot) VALUES (?, ?, ?)', values)

        # Save the id of the last row that was added to the database.
        # It is the id of the movie we just added.
        movie_id = result.lastrowid

        for actor in data["Actors"].split(','):

            # Remove any leading or trailing spaces
            actor = actor.strip()

            # Slip name into first and last names
            values = actor.split(' ', 1)

            # First check to see if the actor is already in the table
            cursor = self.connection.execute(cmds.get_actor_id, values)
            result = cursor.fetchone()

            # If actor_id is None it means the actor is not in the table
            # so we will add actor to the table.
            if result is None:

                # Add the actor to the actor table and save the id we get back.
                result = self.connection.execute('INSERT INTO actor (first_name, last_name) VALUES (?, ?)', values)

                # Save the id of the last row added.
                # It is the actor id of the actor just added.
                actor_id = result.lastrowid

            else:
                # Results are tuples. We just want the first value.
                actor_id = result[0]

            # Add the actor_id movie_id pair to the actor_in_movie table.
            # Adding the pair connects the actor to a movie.
            values = (actor_id, movie_id)
            result = self.connection.execute('INSERT INTO actor_in_movie (actor_id, movie_id) VALUES (?, ?)', values)


    def get_movie(self, title):

        cursor = self.connection.execute(cmds.get_movie, (title, ) )
        result = cursor.fetchone()
        return result


    def get_movies_with_actor(self, actor_name):
        "Searches the database for movies with the actor."

        # Search for the actor's id using first and last name.
        first_name, last_name = actor_name.split()
        cursor = self.connection.execute(cmds.get_actor_id, (first_name, last_name))

        # Get the id from the cursor.
        actor_id = cursor.fetchone()

        # Use the actor_id to search for the movies they are in.
        cursor = self.connection.execute(cmds.movies_with_actor, actor_id)

        # Get all the rows at once as a list.
        # It is a list of tuples. One for each row result.
        # [(id, title), (id, title), (id, title)]
        movies_with_actor = cursor.fetchall()

        # Close the cursor when done with it.
        cursor.close()

        # Return the list of movies.
        return movies_with_actor



if __name__ == "__main__":

    # Create a movie database object to work with.
    movie_db = MovieDatabase()

    # Delete any old tables and create a new table.
    movie_db.delete_tables()
    movie_db.create_tables()

    the_matrix = {"Title": "The Matrix",
                  "Year": "1999",
                  "Actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving",
                  "Plot": "A computer hacker learns something new."}

    johnnie = {"Title": "Johnnie",
               "Year": "1988",
               "Actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving",
               "Plot": "Wired courier goes nuts."}

    grail = {"Title": "The Holy Grail",
               "Year": "1981",
               "Actors": "John Cleese, Michael Palin, Graham Chapman",
               "Plot": "The Knights search for the grail."}


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

from movie_client import get_movie_data
from movie_database import MovieDatabase

class Controller(object):

    def __init__(self):
        self.movie_db = MovieDatabase()


    def initialize_database(self):
        movie_titles = ["Brazil",
                         "The Fifth Element",
                         "Spirited Away",
                         "Princese Monoko",
                         "The Guardians of the Galaxy"]

        for title in movie_titles:
            self.download_movie(title)

        self.movie_db.commit()


    def download_movie(self, title):
        """"Downloads the movie data for the movies in the list.
        Saves the data to the database"""

        # Call the client method to get a dictionary with the movies' data.
        data = get_movie_data(title)

        # Check to see if there is a key in the dictionary called 'Error'
        if not "Error" in data:

            # Add the values to the database.
            self.movie_db.add_movie_data(data)
            return data

        else:
            print("Error getting: {0}. Please check the title.".format(title))
            return None


    def find_movie(self, title):
        """Looks for the movie in the local database.
        If it is not found, then it downloads the movie data
        and stores it in the local database"""

        result = self.movie_db.get_movie(title)

        if result is None:
            data = self.download_movie(title)

            if data is not None:
                self.movie_db.add_movie_data(data)
                result = self.movie_db.get_movie(title)

        return result


if __name__ == "__main__":

    controller = Controller()
    controller.initialize_database()

    result = controller.find_movie("The Big Lebowski")

    print(result)
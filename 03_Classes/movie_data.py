
class MovieData(object):
    "Stores information about a movie."

    # The __init__ method is always called when a class object is created.
    # In this example it requires a single argument, data.
    def __init__(self, data):
        "Initialize the class with a movie data dictionary."

        try:
            # Adding attributes and setting them
            self.title = data['Title']
            self.actors = data['Actors'].split(',')
            self.plot = data['Plot']

        except Exception as ex:
            print("Error: ", ex)


    def print_data(self):
        "Prints the movie information."

        # The self variable is the class object that was created
        # when the class was instanciated. It is used to access
        # instance data.
        print("Movie name: " + self.title)
        print("Name of the actors: " + ', '.join(self.actors))
        print("The plot: " + self.plot)


# Run some tests if the module is run directly.
if __name__ == "__main__":
    # Fails because d is a string an not a dictionary
    d = "hey"
    movie1 = MovieData(d)

    # Fails because the dictionary does not have the right keys in it.
    d = {}
    movie2 = MovieData(d)

    # Works because the argument is a dictionary with all the right keys.
    d = {'Title': 'Big Movie',
         'Actors': "Joe, Moe, Curly",
         'Plot': 'The Three Stooges try to paint a house.'}
    movie3 = MovieData(d)

    print("Done")



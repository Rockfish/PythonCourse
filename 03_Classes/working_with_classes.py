"""
A class is an object that can have both properties and methods.

They are used as the main building blocks in most programs.
They help you organize your code and create units of my_data along with
the functions that work with the my_data.
"""

#
#  Defining a simple class with a single class attribute.
#

class MyClass(object):
    my_data = "Hello"

#
#  Creating an instance of the class.
#

first = MyClass()

#
#  Setting the attribute
#

first.my_data = "Welcome"

print(first.my_data)


#
#  Creating a second instance of the class.
#
second = MyClass()

second.my_data = "Hoody"

print(second.my_data)

#
#  Each instance is a different object.
#

test = first == second

if not test:
    print("The objects are not the same.")

#
#  But the types are the same.
#

if type(first) == type(second):
    print("The objects are of the same type.")

#
#  Each instance has its own my_data.
#

print(first.my_data)
print(second.my_data)

#
#  You can easily add attributes to an object after it's been created.
#

first.more_stuff = "Hi"
first.even_more = "Wow"


#
#  Defining a class with two attributes and one method.
#
#  A class start with a object type and builds on to it.
#
#  The 'self' object is the class instance. It's how the
#  class methods are connected to the right attributes instances.
#

class MovieData(object):
    "Stores information about a movie."

    title = ""
    actors = []
    plot = ""

    def print_data(self):
        "Prints the movie information."

        # The self variable is the class object that was created
        # when the class was instanciated. It is used to access
        # instance data.
        print("Movie name: " + self.title)
        print("Name of the actors: " + ', '.join(self.actors))
        print("The plot: " + self.plot)


#
#  Creating an instance of the MovieData class and set its attributes.
#

movie_data = MovieData()

movie_data.title = "Monty Python and the Holy Grail"
movie_data.actors = ['Chapman', 'Cleese', 'Idle', 'Gilliam', 'Jones', 'Palin']
movie_data.plot = "King Arthur and the nights of the round table search for the Holy Grail."


#
#  Printing the movie object's attributes
#

print("Movie name: " + movie_data.title)
print("Name of the actors: " + ', '.join(movie_data.actors))
print("The plot: " + movie_data.plot)


#
#  Calling the MovieData's method called print_data.
#

movie_data.print_data()


#
#
#  Using the class to hold data downloaded from an online movie database.
#
#  Import the module with the download method we are going to use.
#
import movie_client

# The list of movies want data for
favorite_movie_titles = ["Brazil",
                         "The Fifth Element",
                         "Spirited Away",
                         "Princese Monoko",
                         "The Guardians of the Galaxy"]

# The list that will hold the MovieData objects.
movie_data_list = []

#
# Loop through list of movies and try to download their data.
# Store the data in a list of MovieData objects
#

for title in favorite_movie_titles:

    # Call the client method to get a dictionary with the movies' data.
    data = movie_client.get_movie_data(title)

    # Check to see if there is a key in the dictionary called 'Error'
    if not "Error" in data:

        # Create a new MovieData object.
        movie_data = MovieData()

        # Set the attributes on the new object.
        movie_data.title = data['Title']
        movie_data.actors = data['Actors'].split(',')
        movie_data.plot = data['Plot']

        # Add the new object to our list of movie data objects.
        movie_data_list.append(movie_data)

    else:
        print("Error getting: {0}. Please check the title.".format(title))


print("")

#
#  Call the print_data method on every MovieData object in the list.
#

for movie in movie_data_list:
    movie.print_data()
    print("")


#
#  Save the data to a file.
#

output_file = open("downloaded_movie_data.txt","w")

for movie in movie_data_list:
    output_file.write("Movie name: " + movie.title + "\n")
    output_file.write("Name of the actors: " + ', '.join(movie.actors) + "\n")
    output_file.write("The plot: " + movie.plot + "\n\n")

output_file.close()

print("")


#
#  Save the movie data list to a file using Python's pickle module.
#  Use pickle a quick and efficient way to serialize an object.
#

import pickle

# Open a file for binary writing
with open("saved_movie_data.pickle", "wb") as output_file:

    # Dump the movie_data_list object to the file
    pickle.dump(movie_data_list, output_file)


# Create a new variable
new_movie_list = None

# Open a file for binary reading.
with open("saved_movie_data.pickle", "rb") as input_file:

    # Load the pickle data and create a new list of
    # movie data objects from the saved data.
    new_movie_list = pickle.load(input_file)


# Print the newly loaded list of movie data objects.
for movie in new_movie_list:
    print("Movie name: " + movie.title)
    print("Name of the actors: " + ', '.join(movie.actors))
    print("The plot: " + movie.plot)
    print("")


print("Done")
















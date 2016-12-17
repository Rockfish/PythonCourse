"""
Modules are files or groups of files that contain Python code.

You can import modules into your own code so that you can use the functions.

Below are common modules that come with Python
"""

#
#  The os module is for working with the operating system
#
import os

#
# environ is a dictionary of environment values.
#

for k, v in os.environ.items():
    print(k, ":", v)

#
# Testing to see if a file exists
#

if os.path.exists("MontyPythonData.csv"):
    print("The file exists.")
else:
    print("The file is missig.")

#
#  The sys module has functions related to the Python environment.
#
import sys

# The Python verion

print(sys.version)

#
#  The datetime module has a bunch of date time functions.
#
import datetime

print(datetime.datetime.now())

#
#  Importing your own functions from a file called movie_facts.
#
import movie_facts

#
#  Seeing what is in movie_facts with the dir() function.
#

print(dir(movie_facts))

#
#  Calling a function in movie_facts
#

data = movie_facts.GetTheMovieData()

for row in data:
    print(row)

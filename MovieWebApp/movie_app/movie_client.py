"""
Methods for downloading movie data from http://omdbapi.com.
"""

import json

# Python 3
# import http.client
# from urllib.parse import quote

# Python 2.7
import httplib
from urllib import quote


def get_movie_data(title):

    """Downloads movie data from imdbapi.com.
    Returns a dictionary with the movie's data."""

    # Create a connection object that will talk to the server.
    server = "www.omdbapi.com"

    # connection = http.client.HTTPConnection(server)  # Python 3
    connection = httplib.HTTPConnection(server)        # Python 2.7

    # Quote the string to make it safe for use in a URL
    url_encoded_title = quote(title)

    # Dictionary with the request parameters.
    query_parameters =  {
             'r': 'JSON',  # Asking for in result to me in JSON format
             't':  url_encoded_title
         }

    # Use list comprehension to build a list the key values pairs as strings: ['k0=v0', 'k1=v1', 'k2=v2']
    query_items = [k + "=" + v for k, v in query_parameters.items()]

    # Start a query string and join all the query items with '&' between item.
    query = "?" + "&".join(query_items)

    # Configure the request with the HTTP command and the url.
    path = "/"
    url = path + query
    connection.request("GET", url)

    # Make the call to the server
    response = connection.getresponse()

    raw_bytes = bytes()
    movie_info = None

    # Read the response data only if the status is good.
    if response.status == 200:

        # Read the bytes from the response convert it to a unicode string.
        raw_bytes = response.read()
        data_string = raw_bytes.decode("utf-8")

        # The data_string is a string in JSON format.
        # Convert the string to a dictionary using the loads method from the json module.
        movie_info = json.loads(data_string)

    else:
        print("Error. Status: {0}   Message: {1}".format(response.status, response.msg))

    return movie_info


if __name__ == "__main__":

    data = get_movie_data("The Matrix")

    for key, value in data.items():
        print("{0}: {1}".format(key, value))


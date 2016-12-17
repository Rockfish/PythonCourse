
xmldata = """<?xml version="1.0" encoding="UTF-8"?>
<movies>
    <movie title="The Matrix" language="English" type="movie" imdbID="tt0133093" imdbVotes="904,215" imdbRating="8.7" metascore="73" poster="http://ia.media-imdb.com/images/M/MV5BMTkxNDYxOTA4M15BMl5BanBnXkFtZTgwNTk0NzQxMTE@._V1_SX300.jpg" awards="Won 4 Oscars. Another 35 wins and 40 nominations." country="USA, Australia" plot="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers." actors="Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving" writer="Andy Wachowski, Lana Wachowski" director="Andy Wachowski, Lana Wachowski" genre="Action, Sci-Fi" runtime="136 min" released="31 Mar 1999" rated="R" year="1999"/>
    <movie title="Big" language="English" type="movie" imdbID="tt0094737" imdbVotes="121,859" imdbRating="7.3" metascore="72" poster="http://ia.media-imdb.com/images/M/MV5BNDk0OTM1Mzk3M15BMl5BanBnXkFtZTgwNDg2NjIyMDE@._V1_SX300.jpg" awards="Nominated for 2 Oscars. Another 12 wins and 12 nominations." country="USA" plot="When a boy wishes to be big at a magic wish machine, he wakes up the next morning and finds himself in an adult body." actors="Tom Hanks, Elizabeth Perkins, Robert Loggia, John Heard" writer="Gary Ross, Anne Spielberg" director="Penny Marshall" genre="Comedy, Drama, Fantasy" runtime="104 min" released="03 Jun 1988" rated="PG" year="1988"/>
    <movie title="A Bug's Life" language="English" type="movie" imdbID="tt0174716" imdbVotes="171,017" imdbRating="7.2" metascore="77" poster="http://ia.media-imdb.com/images/M/MV5BMTI5NTc1NjU2NF5BMl5BanBnXkFtZTcwNzkyNDAyMQ@@._V1_SX300.jpg" awards="Nominated for 1 Oscar. Another 14 wins and 19 nominations." country="USA" plot="A misfit ant, looking for 'warriors' to save his colony from greedy grasshoppers, recruits a group of bugs that turn out to be an inept circus troupe." actors="Dave Foley, Kevin Spacey, Julia Louis-Dreyfus, Hayden Panettiere" writer="John Lasseter (original story by), Andrew Stanton (original story by), Joe Ranft (original story by), Andrew Stanton (screenplay), Don McEnery (screenplay), Bob Shaw (screenplay), Geefwee Boedoe (additional writer), Jason Katz (additional writer), Jorgen Klubien (additional writer), Robert Lence (additional writer), David Reynolds (additional writer)" director="John Lasseter, Andrew Stanton" genre="Animation, Adventure, Comedy" runtime="95 min" released="25 Nov 1998" rated="G" year="1998"/>
</movies>
"""


#
#  ElementTree is an XML parser that lets you walk the XML DOM.
#  See http://effbot.org/zone/element-index.htm
#
import xml.etree.ElementTree as ET


#
# Read the xml from a file
#
tree = ET.parse("country_data.xml")
root = tree.getroot()

for child in root:
    print(child.tag, child.attrib)


#
# Read the xml from a string
#
tree = ET.fromstring(xmldata)
children = tree.getchildren()

for child in children:
    print(child.tag, child.attrib)

#
#  Creating XML
#

# movies is the root node.
movies = ET.Element('movies')

# Add a subelement to movies
movie = ET.SubElement(movies, 'movie')

# Add three subelements to movie and set their text
title = ET.SubElement(movie, 'title')
title.text = "The Matrix"

actors = ET.SubElement(movie, 'actors')
actors.text = "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving"

plot = ET.SubElement(movie, 'plot')
plot.text = "Hacker discovers the world isn't like it seems."

#
# Print the xml we created
#
ET.dump(movies)

#
# Save the xml to a file
#
tree = ET.ElementTree(movies)
tree.write("more_movies.xml")



print("Done")




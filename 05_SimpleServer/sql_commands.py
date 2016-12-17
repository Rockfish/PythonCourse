"""
Contains all the SQL commands needed to work with the movie database.

Movie data available from http://omdbapi.com/

Title,
Director,
Writer,
Actors,
Plot,
Poster,
Runtime,
Rating,
Votes,
Genre,
Released,
Year,
Rated,
ID (IMDb ID)

"""


create_tables = (
    """ CREATE TABLE movie (
        id integer primary key,
        title text,
        year integer,
        plot text);""",
    """CREATE TABLE actor (
        id integer primary key,
        first_name text,
        last_name text);""",
    """CREATE TABLE actor_in_movie (
        actor_id integer,
        movie_id integer);"""
)

drop_tables = (
    """DROP TABLE IF EXISTS movie;""",
    """DROP TABLE IF EXISTS actor;""",
    """DROP TABLE IF EXISTS actor_in_movie;"""
)

insert_movie = """
    INSERT INTO movie (title, year, plot) VALUES (?, ?, ?)
"""

insert_actor = """
    INSERT INTO movie (first_name, last_name) VALUES (?, ?)
"""

insert_actor_in_movie = """
    INSERT INTO movie (actor_id, movie_id) VALUES (?, ?)
"""

get_actor_id = """
    SELECT id FROM actor WHERE first_name = ? AND last_name = ?;
"""

get_movie = """
    SELECT * FROM movie WHERE title = ?;
"""

movies_with_actor = """
    SELECT id, title
    FROM movie, actor_in_movie
    WHERE actor_in_movie.actor_id = ? AND actor_in_movie.movie_id = movie.id
"""


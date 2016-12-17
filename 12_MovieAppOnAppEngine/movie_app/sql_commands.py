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
    """
    CREATE TABLE IF NOT EXISTS movie (
        id int(11) NOT NULL AUTO_INCREMENT,
        title varchar(100) DEFAULT NULL,
        year integer,
        plot varchar(1000) DEFAULT NULL,
        poster varchar(200) DEFAULT NULL,
        PRIMARY KEY (id));""",
    """
    CREATE TABLE IF NOT EXISTS actor (
        id int(11) NOT NULL AUTO_INCREMENT,
        first_name varchar(50) DEFAULT NULL,
        last_name varchar(50) DEFAULT NULL,
        PRIMARY KEY (id));""",
    """
    CREATE TABLE IF NOT EXISTS actor_in_movie (
        actor_id integer,
        movie_id integer);""",
    """
    CREATE TABLE IF NOT EXISTS uploads (
        title text,
        date text,
        path text);""",
    """
    CREATE TABLE IF NOT EXISTS users (
        userid text,
        password text);"""
)

drop_tables = (
    """DROP TABLE IF EXISTS movie;""",
    """DROP TABLE IF EXISTS actor;""",
    """DROP TABLE IF EXISTS actor_in_movie;""",
    """DROP TABLE IF EXISTS uploads;""",
    """DROP TABLE IF EXISTS users;"""
)

insert_movie = """
    INSERT INTO movie (title, year, plot, poster) VALUES ('{}', '{}', '{}', '{}')
"""

insert_actor = """
    INSERT INTO actor (first_name, last_name) VALUES ('{}', '{}')
"""

insert_actor_in_movie = """
    INSERT INTO actor_in_movie (actor_id, movie_id) VALUES ('{}', '{}')
"""

get_actor_id = """
    SELECT id FROM actor WHERE first_name = '{}' AND last_name = '{}';
"""

get_movie = """
    SELECT title, year, plot, poster FROM movie WHERE title = '{}';
"""

get_movies = """
    SELECT title, year, plot, poster FROM movie;
"""

get_actors = """
    SELECT first_name, last_name FROM actor;
"""

movies_with_actor = """
    SELECT id, title
    FROM movie, actor_in_movie
    WHERE actor_in_movie.actor_id = '{}' AND actor_in_movie.movie_id = movie.id
"""

insert_upload = """
    INSERT INTO uploads (title, date, path) VALUES ('{}', '{}', '{}')
"""

insert_user = """
    INSERT INTO users (userid, password) VALUES ('{}', '{}')
"""

get_user = """
    SELECT userid, password FROM users WHERE userid = '{}'
"""







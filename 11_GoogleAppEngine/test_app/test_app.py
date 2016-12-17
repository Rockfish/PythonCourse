import os
import webapp2
from datetime import datetime

# To use MySQLdb first install MySQL and MySQL-python
import MySQLdb

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

insert_command = """
    INSERT INTO movie (title, year, plot, poster)
    VALUES ('Die Hard', '2000', 'Crazy guy blows things up', '{}');
"""

class MainPage(webapp2.RequestHandler):

    def get(self):
        env = os.getenv('SERVER_SOFTWARE')
        result = "Not started"

        action = "starting"

        try:
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

            cursor = db.cursor()

            action = "Create tables"

            for table in create_tables:
                cursor.execute(table)

            db.commit()

            action = "Inserting data"

            command = insert_command.format(str(datetime.now()))
            cursor.execute(command)

            db.commit()

            action = "SELECT * FROM movie;"

            cursor.execute("SELECT * FROM movie;")

            rows = cursor.fetchall()

            result = "<br>"
            for row in rows:
                result = result + str(row) + "<br>"

        except Exception as ex:
            result = ex

        message = "Action: {}<br>Result: {}".format(action, result)

        html = """<html><body><h1>Testing App Engine</h1><h2>{}</h2></body></html>""".format(message)

        self.response.out.write(html)


app = webapp2.WSGIApplication([
                               ('/', MainPage),
                               ], debug=True)

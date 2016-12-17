"""
How to work with the SQLite3 database from http://www.sqlite.org

An easy way to view and work with SQLite database is to use the
FireFox Add-on called SQLite Manager.

FireFox SQLite Manager Add-on:
https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager/

"""

#
# First import the SQLite module
#

import sqlite3

#
#  Open a connection to the database.
#
#  If the database does not exist SQLite will create it.
#

db_connection = sqlite3.connect("test.sqlite")

#
#  Creating a table
#

#
#  First decide what the table will look like and write the
#  create table command
#
create_movie_data_table_command = '''
    CREATE TABLE Movies (
        id integer primary key,
        title text,
        actors text,
        plot text);
'''

try:
    db_connection.execute(create_movie_data_table_command)
except:
    "Table already exists"
    pass

#
#  Inserting data to the table.
#

insert_command = 'INSERT INTO Movies (title, actors, plot) VALUES ("Holy Grail", "Cleese, Palin, Chapman", "Knights search for the Holy Grail")'
db_connection.execute(insert_command)

#
#  A better way to do inserts is to use value subsitution in the command.
#  The question marks, (?, ?, ?), lets sqlite do the value subsitution.
#  Avoids problems with encoding and escaping strings. It is faster and safer.
#

title = "The Matrix"
actors = "Reeves, Fishburne, Moss"
plot = "A computer hacker goes on a wild trip."

values = (title, actors, plot)

db_connection.execute('INSERT INTO Movies (title, actors, plot) VALUES (?, ?, ?)', values)

#
# Commit to write the data to the database.
#
db_connection.commit()

#
# Searching the table. The command returns a cursor.
#
# A cursor is an database object which lets you loop through the rows.
#

cursor = db_connection.execute("SELECT * FROM Movies")

for row in cursor:
    print(row)

# Close the cursor when you're done or it will lock the table.
cursor.close()

#
#  Finding all the movies where one of the actors is Reeves.
#  The LIKE operator does pattern matching. The % means any characters.
#
cursor = db_connection.execute("SELECT title FROM Movies WHERE actors LIKE '%Reeves%' ")

for row in cursor:
    print(row)

#
#  Delete the table
#
db_connection.execute("DROP TABLE IF EXISTS Movies")
db_connection.commit()

#
# Close the table to release the database file.
#
db_connection.close()


print("Done")

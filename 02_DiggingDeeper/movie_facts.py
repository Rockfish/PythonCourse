"""
This module has a couple of functions
"""

def GetTheMovieData():
    """Reads the MontyPythonData.csv and returns
    a list of dictionaries with the movie data"""

    # Read the file
    content = open("MontyPythonData.csv").read()

    # Split the file into a list of lines
    lines = content.splitlines()

    # Split each line at the commas, which creates a list of items.
    # Add each list of items to a data list.
    # Creates a list of lists called data.

    templist = []   # empty list

    for l in lines:
        items = l.split(',')
        templist.append(items)

    data = []

    # The first line is the list of labels.
    labels = templist[0]

    # For line of data create a dictionary with values
    # using the labels from the first line as keys.
    for item in templist[1:]:
        row = {}
        for i in range(len(labels)):
            row[labels[i]] = item[i]
        data.append(row)

    return data

#
#  The code block below only runs when this file is run not when it is imported.
#  This is good why of testing your code. It is like a unit test.
#
if __name__ == "__main__":
    val = GetTheMovieData()

    for row in val:
        print(row)

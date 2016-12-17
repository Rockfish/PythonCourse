
# Read the file
content = open("MontyPythonData.csv").read()

# Split the file into a list of lines
lines = content.splitlines()

#
# Split each line at the commas, which creates a list of items.
# Add each list of items to a data list.
# Creates a list of lists called data.

data = []   # empty list

for l in lines:
    items = l.split(',')
    data.append(items)

# data is now a list of lists

#
# Print the data skipping the first item in the data list.
#

for items in data[1:]:
    message = "Name: {0} {1}    Favorite Color: {2}    Character: {3}".format(*items)
    print(message)

print("Done")
"""
Working with lists
"""
#
# Creating a list
# Square brackets around comma separated values makes a list.
#
colors = ["red", "blue", "yellow", "green", "white", "black"]

# length of the list
val = len(colors)
print(val)

# Lists start counting at 0.
val = colors[0]
print(val)

# Use negative numbers to index off the end of the list.
val = colors[-1]
print(val)

#
# Slicing a list
#

# Slice starting at the third item
val = colors[2:]
print(val)

# Slice starting at the third and end at the fourth.
# Notice that slicing does not inclue the fifth item.
# It excludes the last item on a index.
val = colors[2:5]
print(val)

# Slice from the back of the list.
val = colors[:-2]
print(val)

val = colors[1:-2]
print(val)

val = colors[-4:-2]
print(val)

#
# Using slicing to replace items in a list
#
colors[2:4] = ["pink", "brown"]
print(colors)

#
# Sorting
#
colors.sort()
print(colors)

#
# Reversing
#
colors.reverse()
print(colors)

#
# Count the number of times something is in the list
#
val = colors.count("black")
print(val)

#
# Find what postion something is at.
#
val = colors.index("red")
print(val)
#
# Popping items off a list. Removes the item form the list.
#

# Popping the first item.
val = colors.pop()

# Popping from a postion in the list.
val = colors.pop(2)

#
# Adding things to a list.
#
colors.append("grey")
print(colors)

#
# Combine lists
#
moreColors = colors + ["purple", "orange"]
print(moreColors)

#
# List of lists
# List can hold anything, including other lists
#
colorslist = [colors, ["purple", "orange"], ["cyan"]]
print(colorslist)

print("Done")



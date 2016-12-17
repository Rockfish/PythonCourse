'''
Loops let you walk through a sequence of items, such as items in a list
'''
#
# looping through a list
#
colors = ['black', 'blue', 'brown', 'green', 'purple', 'white', 'yellow']

for color in colors:
    print(color)

#
# Looping through a range of numbers
#

for num in range(5):
    print(num)         # Prints the numbers 0, 1, 2, 3, 4


# Range can have start values and end values.
# Stops right before the end value.

for num in range(10, 16):
    print(num)         # Print the numbers 10, 11, 12, 14, 15. Note stops at 15.

# Range can also have a step value

for num in range(20, 31, 2):
    print(num)         # Print the numbers 20, 22, 24, 26, 28, 30. Notes stops at 30.





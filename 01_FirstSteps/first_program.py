
# List of colors
colors = ['black', 'blue', 'brown', 'green', 'purple', 'white', 'yellow']

#
# Ask the user for input
#
answer = input("What is your favorite color? ")

#
# Print their answer
#
print("Your answer was: ", answer)

#
# Use a flag to tell if we have found the color.
#
foundColor = False

#
# Loop through all the colors.
# If the color equals the answer then we found the color in the list.
# Set foundColor flag to True so we know the color was found.
#
for color in colors:
    if color == answer:
        foundColor = True

#
# Check the foundColor flag and print the right message.
#
if foundColor:
    print("Your color is in the list.")
else:
    print("Can't find your color.")
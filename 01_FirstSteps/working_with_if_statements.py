"""
If statements test for true or false.
Any expression that is not False, not 0, or not an empty string is considered true.
"""

# Testing for True or False

value = True

if value:
    print("It's true.")

#
# Testing numbers
#

# 0 is the same as false

if 0:
    print("Hello")  # Does not print. The test is false when 0.

if 1:
    print("Hello")  # Does print. Any non-zero number is true.

#
# Testing strings
#

value = ""  # empty string

if value:
    print("empty string")  # Does not print. Empty strings are false.

value = "something"

if value:
    print("non-empty string.")  # Does print. Non-empty strings are true.

#
# Else statements run when the test is false.
#

value = False

if value:
    print("Hello")   # Does not print.
else:
    print("Bye")     # Does print since value is false


#
# elif statements mean if else. Used to keep testing values.
#

value = 3

if value == 1:
    print("One")
elif value == 2:
    print("Two")
elif value == 3:
    print("Three")  # This one prints since the value is 3
elif value == 4:
    print("Four")
else:
    print("Value is not 1, 2, 3, or 4.")

print("Done")


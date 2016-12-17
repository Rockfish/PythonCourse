"""
A function is a block of code the runs when it is called.

A function can take parameters and return values.

All the lines indented under the defintion are part of the function.
The definition ends with the first line that is not indent.
The indented part is called the function block.

Function only run when called.

Everything defined inside the function block stays in the block.

"""

#
#  Defining simple function with no parameters.
#

def myFunc():
    print("Hello")

#
#  Calling the function
#

myFunc()

#
#  Defining a function that takes a parameter.
#

def counter(count):
    for n in range(count):
        print(n)

counter(3)

#
#  Defining a larger function that takes several parameters.
#  Blank lines in a function are okay.
#  The data dictionary only exist inside the function.
#

def spam(name, color, count):

    data = {'name': name, 'color': color, 'count':count}

    print("Hi", name)
    print("Your color is", color)
    print("Here is a dictionary with your data:", data)


spam('John', 'green', 46)

#
#  Function return a dictionary
#

def moreSpam():
    data = {'name': 'Freddy', 'color': 'purple', 'count':57}
    return data

print(moreSpam())

#
#  Function can have document strings
#

def eggs(price):
    "This function calculates the price of a dozen eggs."
    print("The cost is", price * 12)

#  doc strings can be seen with the help function

help(eggs)

#
#  Functions are object too. So we can use them as values
#  and we can call them from other variables.
#

def spamspam():
    print("Do you want eggs and spam?")

val = spamspam

val()

#
#  Functions can be stored like all other objects.
#

listOfFunctions = [counter, spam, eggs, spamspam]

print("Done")



"""
Exceptions are when things go wrong. We can catch exceptions with try/except.

By catching the exceptions we can then handle it anyway we want.
"""

#
#  Dividing by zero causes an exception.
#
try:
    val = 345 / 0
except:
    print("Opps there was an error.")


#
#  Trying to open a file that doesn't exist causes an exception.
#

try:
    data = open('wrongname.txt').read()
except:
    print("Sorry the file does not exist.")

#
#  When an exception happens there Python create an exception object
#  with all the information about the exception.
#

try:
    d = {}
    print(d["missing"])
except Exception as ex:
    print(type(ex))    # The exception instance
    print(ex.args)     # arguments are stored in .args
    print(ex)          # Or they can be printed directly as a message.

#
#  We can create our own exception with any information we want.
#

try:
    raise Exception('spam', 'eggs')
except Exception as ex:
    print(ex)          # Print the exception arguments.

#
#  Raising or throwing exceptions is a useful why for one function
#  to tell another function what went wrong.
#  The caller can then catch the exception and read the exception message.
#

def divide(a, b):
    # Check the parameters before using them.
    if b == 0:
        raise Exception("Can't divide by zero.")
    return a / b

def call_divide():
    try:
        divide(23, 0)
    except Exception as ex:
        print(ex)          # Print the exception message

call_divide()




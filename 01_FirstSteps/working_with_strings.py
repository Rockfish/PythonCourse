#
#  Strings
#

# Use double quotes "" or single ''
# Multi line strings use either triple double quotes """ """ or triple signal quotes ''' '''

a = "Hello World"

b = 'Hello World'

c = """
First line.
Second line.
Third line.
"""

# Strings can have unicode characters
b = "Teknologjisë"
c = "Mirë Dita"  # Good day
name = 'Xhon Heç' # John Hatch

# Getting the length of a string
len(name)

val = a.split(" ")

print("Hello World!")


#
# Formating
#

val = '{0}, {1}, {2}'.format('a', 'b', 'c')
val = '{}, {}, {}'.format('a', 'b', 'c')  # 3.1+ only
val = '{2}, {1}, {0}'.format('a', 'b', 'c')
val = '{0}{1}{0}'.format('abra', 'cad')   # arguments' indices can be repeated

data = ["John", "9/16/14"]
val = "Hi {}, today is the {}.".format(*data)

val = 'Coordinates: {latitude}, {longitude}'.format(latitude='37.24N', longitude='-115.81W')

coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
val = 'Coordinates: {latitude}, {longitude}'.format(**coord)

#
# Encoding
#


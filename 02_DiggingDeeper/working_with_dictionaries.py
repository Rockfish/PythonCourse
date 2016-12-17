"""
Dictionaries are lists of key value pairs.

The key can be any object that doesn't change and the value can be any object.

The key and values have a colon ':' between them.

   { Key:Value, Key:Value, Key:Value}

"""

#
# Creating empty dictionaries
#

data = {}
data = dict()

#
#  Dictionary with three pairs using numbers as keys.
#
numbers = {1:'one', 2:'two', 3:'three'}

#
#  Dictionary with four pairs using strings as keys.
#

data = {'FirstName':'Graham',
        'LastName':'Chapman',
        'FavoriteColor': 'blue',
        'Character':'King Arthur'}

#
#  Getting things out of a dictionary.
#

val = data['FirstName']
val = data['LastName']

#
#  Using the get method in case the key is not in the dictionary.
#  If the key is not there then it returns null which tests as False.
#

val = data.get('BirthDate')

if not val:
    print("BirthDate is not one of the keys.")

#
#  Changing things in the dictionary
#

data['FavoriteColor'] = 'green'
data['Character'] = 'The French guy'

#
#  Dictionary with lists
#

data = {'colors': ['yellow', 'blue', 'red'],
        'cars':['Ford', 'Fiat', 'VW'],
        'planes':['747', 'A320', 'DC9'] }

#
#  Getting the key or getting the values
#

keys = data.keys()

values = data.values()

#
#  Looping through a dictionary
#

for key in data:
    print(data[key])


#
#  Looping through a dictionary by items.
#  Items returns two values each time.
#  The first one is the key, the second is the value.
#

for k, v in data.items():
    print(k, v)


#############################
print("Done")

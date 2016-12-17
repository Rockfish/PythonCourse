
actors = [{'Character': 'King Arthur', 'Favorite Color': 'blue', 'Last': 'Chapman', 'First': 'Graham'},
          {'Character': 'Sir Lancelot', 'Favorite Color': 'yellow', 'Last': 'Cleese', 'First': 'John'},
          {'Character': 'Sir Robin', 'Favorite Color': 'red', 'Last': 'Idle', 'First': 'Eric'},
          {'Character': 'Green Knight', 'Favorite Color': 'green', 'Last': 'Gilliam', 'First': 'Terry'},
          {'Character': 'Sir Bedevere', 'Favorite Color': 'purple', 'Last': 'Jones', 'First': 'Terry'},
          {'Character': 'Sir Galahad', 'Favorite Color': 'yellow', 'Last': 'Palin', 'First': 'Michael'}]

#
#  Tuples
#

t = ('John', 'Cleese', 'red')   # Packing a tuple
first, last, color = t          # Unpacking a tuple

#
#  Joining strings from a list or a tuple
#

colors = ['red', 'blue', 'green', 'yellow']
val = ", ".join(colors)

#
#  Building a list from values in a dictionary using a loop.
#

first_names = []

for data in actors:
    first_names.append(data['First'])

print(first_names)

#
#  Building a list using list comprehension.
#

last_names = [data['Last'] for data in actors]

print(last_names)


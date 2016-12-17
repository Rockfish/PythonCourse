
#
# Open a file, read, then close it.
# Good if you plan to read it again before closing it.
#
montyfile = open("MontyPythonData.csv")
data1 = montyfile.read()
montyfile.close()
print(data1)

#
# Open and read at the same time. File closes eventually.
# This is good for quick scripts.
#
data2 = open("MontyPythonData.csv").read()
print(data2)

#
# Open the file, read it, and have close automatically.
# This is the best pattern.
#
with open("MontyPythonData.csv") as f:
    data3 = f.read()

data3 = data3.splitlines()

for d in data3:
    print(d.split(','))



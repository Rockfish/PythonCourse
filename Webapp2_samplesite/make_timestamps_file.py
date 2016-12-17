"""
Creates timestamps.py with a dictionary of the timestamps 
for the file in the 'files' folder.
"""

import os
from stat import *
from datetime import datetime

current_dir = os.path.dirname(__file__)

def get_file_timestamp(name):
    root = os.path.join(current_dir, 'files')
    filename = os.path.join(root, name)
    filetimestamp = os.stat(filename).st_mtime
    date = datetime.fromtimestamp(filetimestamp)
    return date.strftime("%b %d, %Y - %I:%M %p")
    

def walk_files():
    updates = []
    for root, dirs, files in os.walk(os.path.join(current_dir, 'files')):
        for name in files:
            updates.append(dict(name=name, link=name, date=get_file_timestamp(name)))
    data = dict(updates=updates)
    fp = open('timestamps.py', 'w')
    fp.write("timestamps = %s" % data)
    fp.close()
    print("timestamps = %s" % data)


if __name__ == '__main__':
    walk_files()

    

import sys, urllib, os

def hook(*a):
    print a

for url in sys.argv[1:]:
    fn = os.path.basename(url)
    print url, "->", fn
    urllib.urlretrieve(url, fn, hook)

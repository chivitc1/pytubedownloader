from os import listdir, rename
from os.path import isfile, join
import re

mypath = '/home/chinv/Videos/streamlines/3-destination'
files = [ f for f in listdir(mypath) if isfile(join(mypath, f))]
# print(files);

def one_space_only(filename: str):
    return re.sub(r"\s+", ' ', filename)

for filename in files:
    newname = one_space_only(filename)
    print(newname)
    rename(join(mypath, filename), join(mypath, newname))



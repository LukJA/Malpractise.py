import os
import time
from alive_progress import alive_bar
import requests as rq
from bs4 import BeautifulSoup as bs

# TODO
# Generates an SQL database of the UK data to be queried by data processing applications


CWD = os.path.dirname(os.path.realpath(__file__)) + "/"
print("Working In {}".format(CWD))

def cleanup(filename):
    f = open(filename, "r")
    output = []
    openCode = ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9."]
    closeCode = ["Previous\n","Contents\n","Next\n"]
    copy = False

    for line in f.readlines():
        if line[:2] in openCode:
            copy = True
        elif line in closeCode:
            copy = False

        if copy and line != "\n":
            output.append(line)
            #print(line, end="")

    f.close()
    f = open(filename, "w")
    f.writelines(output)
    f.close()



## HTML Cleanup of Documents

# Get all cache directories
cachedDirs = [x[0] for x in os.walk(CWD)]
cachedDirs.remove(CWD)


for cDir in cachedDirs:
    for filename in os.listdir(cDir):
        if os.path.splitext(filename)[1] == '.htm':
            cleanup(cDir + "/" + filename)
        else:
            print("Avoided File: {}".format(filename))

print("Job Complete")
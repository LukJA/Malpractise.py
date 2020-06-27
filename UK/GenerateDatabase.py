import os
import time
from alive_progress import alive_bar
import requests as rq
from bs4 import BeautifulSoup as bs

cacheDir = "./Cache/"

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

for filename in os.listdir(cacheDir):
    if os.path.splitext(filename)[1] == '.htm':
        cleanup(cacheDir + filename)
    else:
        print("Avoided File: {}".format(filename))

cleanup(cacheDir + "abbott_diane.htm")
import os
import time
from alive_progress import alive_bar
import requests as rq
from bs4 import BeautifulSoup as bs

cacheDir = "./Cache/"

# POA
# We need to cache all the documents ready for analysis and to hopefully not annoy the commons

regAddr = "https://publications.parliament.uk/pa/cm/cmregmem/"
rootAddr = """https://www.parliament.uk/mps-lords-and-offices/standards-and-financial-interests/parliamentary-commissioner-for-standards/""" \
            """registers-of-interests/register-of-members-financial-interests/"""
rootPage = rq.get(rootAddr)
if not rootPage.ok:
    print("Request Failed, Code: {}".format(rootPage.status_code))
    exit(1);

# Get the link listings
rootListing = []
rootSoup = bs(rootPage.content, 'html.parser')
main = rootSoup.find(id="content")
for link in main.find_all("a"):
    if (link.get('href')):
        rootListing.append(link.get('href'))

# Pull the most recent page
subAddr = rootListing[1] # first link is the rules
subPage = rq.get(subAddr)
if not subPage.ok:
    print("Request Failed, Code: {}".format(subPage.status_code))
    exit(1)

# Isolate the most recent data root
pageSoup = bs(subPage.content, 'html.parser')
sub = pageSoup.find(id="maincontent")
table = sub.find_all("table")[0]
date = str(sub.find_all("p")[3].text)
HTMLVersion = table.find("a")

if not HTMLVersion.text == "HTML version":
    print("Content not HTML version: {}".format(HTMLVersion.content))
    exit(1)
HTMLLink = HTMLVersion.get('href')
subLink = HTMLLink.split("/")[0]

# check if we need to get a new version of the files
if os.path.isfile(cacheDir + date):
    print("No Refresh Required, Latest already here...")
    exit(0)
else:
    print("Updating logs...")
    ## clear the folder
    os.system("rm ./Cache/*")
    f = open(cacheDir + date, 'x')
    f.close()
    
## Collect all the HTML documents and save them to the Cache...
# Pull all the names and links..
nameAddr = regAddr + HTMLLink
namePage = rq.get(nameAddr)
nameSoup = bs(namePage.content, 'html.parser')
nameContent = nameSoup.find(id="mainTextBlock")
nameP = nameContent.find_all("p")[3:]

# assemble a names list
nameList = []
for p in nameP:
    name = p.find('a').text
    link = p.find('a').get('href')
    nameList.append((name, link))

# Create a list file
f = open(cacheDir + "nameList.txt", 'w')
for name in nameList:
    f.write("Name: " + name[0] + " , Link: " + name[1] + "\n")
f.write("Length: "+ str(len(nameList)))
f.close()

# pull all the documents down
print("Downloading...")
with alive_bar(len(nameList), bar = 'smooth') as bar:
    for name in nameList:
        localAddr = regAddr + subLink + "/" + name[1]
        personPage = rq.get(localAddr)
        personSoup = bs(personPage.content, 'html.parser')
        f = open(cacheDir + name[1], 'w')
        f.writelines(personSoup.text)
        f.close

        bar()      

print("Success!!")

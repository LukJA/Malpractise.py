import os
import requests as rq
from bs4 import BeautifulSoup as bs

cacheDir = "./Cache/"

# POA
# We need to cache all the documents ready for analysis and to hopefully not annoy the commons

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

# check if we need to get a new version of the files
if os.path.isfile(cacheDir + date):
    print("No Refresh Required, Latest already here...")
    exit(0)
else:
    print("Updating logs...")
    f = open(cacheDir + date, 'x')
    f.close()
    
print(date)
print(HTMLLink)
import requests as rq
from bs4 import BeautifulSoup as bs

# POA
# We need to cache all the documents ready for analysis and to hopefully not annoy the commons

rootAddr = """https://www.parliament.uk/mps-lords-and-offices/standards-and-financial-interests/parliamentary-commissioner-for-standards/""" \
            """registers-of-interests/register-of-members-financial-interests/"""
rootPage = rq.get(rootAddr)
if not rootPage.ok:
    print("Request Failed, Code: {}".format(rootPage.status_code))

# Get the link listings
rootListing = []
rootSoup = bs(rootPage.content, 'html.parser')
main = rootSoup.find(id="content")
for link in main.find_all("a"):
    if (link.get('href')):
        rootListing.append(link.get('href'))

print(rootListing)
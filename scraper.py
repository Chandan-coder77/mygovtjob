import requests
from bs4 import BeautifulSoup
import json

KEYWORDS = ["recruitment","vacancy","notification","advertisement","apply","post","job"]
IGNORED = ["post new job","mou","gig","zomato","swiggy","rapido","quickr","zepto"]

SITES = [
    "https://ssc.nic.in/",
    "https://upsc.gov.in/",
    "https://www.ncs.gov.in/",
    "https://indianrailways.gov.in/",
    "https://ibps.in/"
]

jobs=[]

def extract(url):
    try:
        html = requests.get(url,timeout=12).text
        soup = BeautifulSoup(html,"html.parser")

        for a in soup.find_all("a",href=True):
            text=a.text.strip().lower()

            if any(k in text for k in KEYWORDS) and not any(b in text for b in IGNORED):

                jobs.append({
                    "title": a.text.strip().title(),
                    "vacancies": "Check Notice",
                    "qualification": "Check",
                    "age": "Check",
                    "salary": "As per Govt Rule",
                    "last_date": "Check Website",
                    "state": "India",
                    "category": "Govt Job",
                    "apply_link": url if "http" not in a['href'] else a['href']
                })

    except Exception as e:
        print("Error:",url, e)

for s in SITES:
    extract(s)

# Remove duplicates based on title
unique=[]
titles=set()
for j in jobs:
    if j['title'] not in titles:
        unique.append(j)
        titles.add(j['title'])

with open("jobs.json","w") as f:
    json.dump(unique,f,indent=4)

print("Cleaned Jobs:",len(unique))

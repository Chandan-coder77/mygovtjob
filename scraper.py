import requests
from bs4 import BeautifulSoup
import json
import re

# AI Crawl Keywords
KEYWORDS = ["recruitment","notification","vacancy","advertisement","apply","exam","post","govt"]

# Websites to auto scan
SITES = [
    "https://ssc.nic.in/",
    "https://upsc.gov.in/",
    "https://indianrailways.gov.in/",
    "https://ibps.in/",
    "https://www.ncs.gov.in/"
]

jobs=[]

def extract_jobs(url):
    try:
        html = requests.get(url,timeout=12).text
        soup = BeautifulSoup(html,"html.parser")

        links = soup.find_all("a",href=True)

        for a in links:
            txt = a.text.strip().lower()

            if any(k in txt for k in KEYWORDS) and len(a.text.strip())>8:
                jobs.append({
                    "title": a.text.strip().title(),
                    "vacancies": "Check Notice",
                    "qualification": "Check",
                    "age": "Check",
                    "salary": "Govt Rules",
                    "last_date": "Check Site",
                    "state": "India",
                    "category": "Govt Job",
                    "apply_link": url + a['href'] if "http" not in a['href'] else a['href']
                })
    except:
        print("Error reading",url)


# Run crawler for each site
for site in SITES:
    extract_jobs(site)


# Save final data
with open("jobs.json","w") as f:
    json.dump(jobs,f,indent=4)

print("AUTO AI SCRAPER RUN ✔ Total jobs detected:",len(jobs))

import requests
from bs4 import BeautifulSoup
import json
from datetime import date

jobs=[]

# ------------ 1. SSC Scraper --------------
def ssc_scraper():
    url="https://ssc.nic.in/"
    r=requests.get(url,timeout=10)
    soup=BeautifulSoup(r.text,"html.parser")

    for item in soup.select(".latest-news a")[:5]:
        job={
            "title": item.get_text(strip=True),
            "vacancies": "Update Soon",
            "qualification": "10th/12th/Graduate",
            "age": "18+",
            "salary": "As per rules",
            "last_date": "Not Mentioned",
            "state": "All India",
            "category": "SSC",
            "apply_link": url
        }
        jobs.append(job)

# ------------ 2. UPSC Scraper --------------
def upsc_scraper():
    url="https://upsc.gov.in/"
    r=requests.get(url,timeout=10)
    soup=BeautifulSoup(r.text,"html.parser")

    for item in soup.select(".view-content a")[:5]:
        job={
            "title": item.get_text(strip=True),
            "vacancies": "Update Soon",
            "qualification": "Graduate",
            "age": "18+",
            "salary": "As per rules",
            "last_date": "Not Mentioned",
            "state": "All India",
            "category": "UPSC",
            "apply_link": url
        }
        jobs.append(job)

# ------------ 3. Railway Scraper --------------
def railway_scraper():
    url="https://indianrailways.gov.in/"
    r=requests.get(url,timeout=10)
    soup=BeautifulSoup(r.text,"html.parser")

    for item in soup.select("a")[:5]:
        text=item.get_text(strip=True)
        if "recruit" in text.lower() or "job" in text.lower():
            job={
                "title": text,
                "vacancies": "Update Soon",
                "qualification": "10th/12th/ITI",
                "age": "18-30",
                "salary": "As per rules",
                "last_date": "Not Mentioned",
                "state": "All India",
                "category": "Railway",
                "apply_link": url
            }
            jobs.append(job)

# Run scrapers
ssc_scraper()
upsc_scraper()
railway_scraper()

# Save to jobs.json
with open("jobs.json","w") as f:
    json.dump(jobs,f,indent=4)

print("Jobs Updated Successfully", date.today())

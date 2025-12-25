import requests
from bs4 import BeautifulSoup
import json
import datetime
import time

jobs=[]

def safe_request(url, retry=3, timeout=15):
    for _ in range(retry):
        try:
            return requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=timeout)
        except:
            time.sleep(3)
    return None

# ----------------- SSC Scraper -----------------
def ssc_scraper():
    print("Scraping SSC...")
    url="https://ssc.nic.in/"
    r=safe_request(url)
    if not r: return
    soup=BeautifulSoup(r.text,'html.parser')
    
    notices=soup.find_all("a")[:5]
    for n in notices:
        title=n.text.strip()
        if "Recruitment" in title or "Constable" in title or "GD" in title:
            jobs.append({
                "title":title,
                "vacancies":"Update Soon",
                "qualification":"Check Notice",
                "age":"18+",
                "salary":"--",
                "last_date":"--",
                "state":"All India",
                "category":"SSC",
                "apply_link":"https://ssc.nic.in/"
            })

# ----------------- UPSC Scraper -----------------
def upsc_scraper():
    print("Scraping UPSC...")
    url="https://upsc.gov.in/"
    r=safe_request(url)
    if not r: return
    soup=BeautifulSoup(r.text,'html.parser')

    links=soup.find_all("a")[:5]
    for n in links:
        title=n.text.strip()
        if "Recruitment" in title or "Exam" in title:
            jobs.append({
                "title":title,
                "vacancies":"--",
                "qualification":"Graduate",
                "age":"18+",
                "salary":"--",
                "last_date":"--",
                "state":"All India",
                "category":"UPSC",
                "apply_link":url
            })

# ----------------- Railway Scraper -----------------
def railway_scraper():
    print("Scraping Railway...")
    url="https://indianrailways.gov.in/"
    r=safe_request(url)
    if not r: return
    soup=BeautifulSoup(r.text,'html.parser')

    for n in soup.find_all("a")[:5]:
        title=n.text.strip()
        if "Recruitment" in title or "Apprentice" in title:
            jobs.append({
                "title": title,
                "vacancies": "--",
                "qualification": "10th/ITI",
                "age": "18+",
                "salary": "--",
                "last_date": "--",
                "state": "India",
                "category": "Railway",
                "apply_link": url
            })

# -------- RUN SCRAPER --------
ssc_scraper()
upsc_scraper()
railway_scraper()

# Save file
with open("jobs.json","w") as f:
    json.dump(jobs,f,indent=4)

print("Jobs updated:", len(jobs))

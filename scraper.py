import requests
from bs4 import BeautifulSoup
import json

jobs=[]

# ================= SSC Scraper ================= #
def ssc_scraper():
    url="https://ssc.nic.in/"
    r=requests.get(url,timeout=10)
    soup=BeautifulSoup(r.text,"html.parser")
    title="SSC Latest Notifications"
    job={
        "title":title,
        "vacancies":"Check Website",
        "qualification":"10th/12th/Graduate",
        "age":"18+",
        "salary":"As per rule",
        "last_date":"--",
        "state":"All India",
        "category":"SSC",
        "apply_link":url
    }
    jobs.append(job)

# ================= Railway Scraper ================= #
def railway_scraper():
    url="https://indianrailways.gov.in/"
    r=requests.get(url,timeout=10)
    soup=BeautifulSoup(r.text,"html.parser")
    title="Railway Recruitment Updates"
    job={
        "title":title,
        "vacancies":"Check Website",
        "qualification":"10th/12th/ITI",
        "age":"18-30",
        "salary":"As per rule",
        "last_date":"--",
        "state":"All India",
        "category":"Railway",
        "apply_link":url
    }
    jobs.append(job)

# ================= Future sites (Disabled for now) ================= #
# UPSC Scraper (timeout problem — disabled to avoid workflow fail)
# def upsc_scraper():
#     url="https://upsc.gov.in"
#     r=requests.get(url,timeout=10)
#     soup=BeautifulSoup(r.text,"html.parser")
#     title=soup.title.text.strip()
#     job={
#         "title":title,
#         "vacancies":"Not Available",
#         "qualification":"Graduate",
#         "age":"Varies",
#         "salary":"--",
#         "last_date":"Check website",
#         "state":"All India",
#         "category":"UPSC",
#         "apply_link":url
#     }
#     jobs.append(job)

# ========== Run scrapers ========== #
ssc_scraper()
railway_scraper()
# upsc_scraper()   # disable so no fail

# ========== Save output to jobs.json ========== #
with open("jobs.json","w") as file:
    json.dump(jobs,file,indent=4)

print("✔ jobs.json updated successfully!")

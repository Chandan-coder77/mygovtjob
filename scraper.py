import requests
from bs4 import BeautifulSoup
import json

jobs=[]


# ---------------- LIVE SOURCE 1 - NCS (REAL JOBS) ----------------
def fetch_ncs():
    try:
        url="https://www.ncs.gov.in/"
        soup=BeautifulSoup(requests.get(url,timeout=15).text,"html.parser")
        job=soup.select_one(".featured-job .job-title")  # Top job
        title=job.text.strip() if job else "NCS Govt Jobs"
        return{
            "title":title,
            "vacancies":"Available",
            "qualification":"Check Notice",
            "age":"Check",
            "salary":"As per post",
            "last_date":"Check Site",
            "state":"India",
            "category":"Central",
            "apply_link":url
        }
    except:
        return None


# ---------------- LIVE SOURCE 2 - Employment News ----------------
def fetch_emp_news():
    try:
        url="http://employmentnews.gov.in/"
        soup=BeautifulSoup(requests.get(url,timeout=15).text,"html.parser")
        title=soup.find("h3").text.strip()
        return{
            "title":title,
            "vacancies":"Update Live",
            "qualification":"As per Post",
            "age":"Check",
            "salary":"Govt Rules",
            "last_date":"Check Notice",
            "state":"India",
            "category":"Employment",
            "apply_link":url
        }
    except:
        return None


# ---------------- OLD STATIC SAFE BLOCK (Fallback) ----------------
jobs.append({
"title":"SSC Govt Jobs (Live fetch soon)",
"vacancies":"Update",
"qualification":"10th/12th/Grad",
"age":"18+",
"salary":"Rules",
"last_date":"Check",
"state":"India",
"category":"SSC",
"apply_link":"https://ssc.nic.in/"
})

jobs.append({
"title":"UPSC Govt Jobs (Auto fetch soon)",
"vacancies":"Update",
"qualification":"Graduate",
"age":"21+",
"salary":"Rules",
"last_date":"Check",
"state":"India",
"category":"UPSC",
"apply_link":"https://upsc.gov.in/"
})

jobs.append(fetch_ncs())
jobs.append(fetch_emp_news())

# Remove None if any
jobs=[j for j in jobs if j]


# Save JSON
with open("jobs.json","w") as f:
    json.dump(jobs,f,indent=4)

print("LIVE JOBS UPDATED 🚀")

import requests
from bs4 import BeautifulSoup
import json
import datetime

def safe_request(url):
    try:
        return requests.get(url, timeout=12)
    except:
        return None

jobs = []

###############################
# 1. SSC DEFAULT (temporary)
###############################
jobs.append({
    "title": "SSC Latest Notification",
    "vacancies": "Update Soon",
    "qualification": "10th/12th/Graduate",
    "age": "18+",
    "salary": "As per rules",
    "last_date": "Check Website",
    "state": "All India",
    "category": "SSC",
    "apply_link": "https://ssc.nic.in/"
})

###############################
# 2. UPSC Scraper
###############################
def upsc_scraper():
    url = "https://upsc.gov.in"
    r = safe_request(url)
    if r and r.status_code == 200:
        soup = BeautifulSoup(r.text,"html.parser")
        latest = soup.find("div",{"class":"view-content"})
        if latest:
            title = latest.text.strip()[:60] + "..."
            jobs.append({
                "title": "UPSC Latest – "+title,
                "vacancies": "Available on Website",
                "qualification": "Graduate",
                "age": "21+",
                "salary": "As per UPSC",
                "last_date": "Check Website",
                "state": "India",
                "category": "UPSC",
                "apply_link": url
            })
        else:
            fallback_upsc()
    else:
        fallback_upsc()

def fallback_upsc():
    jobs.append({
        "title": "UPSC Recruitment Coming Soon",
        "vacancies": "Soon",
        "qualification": "Graduate",
        "age": "21+",
        "salary": "Rules as per UPSC",
        "last_date": "Next Update",
        "state": "India",
        "category": "UPSC",
        "apply_link": "https://upsc.gov.in/"
    })

upsc_scraper()

###############################
# 3. Railway Scraper
###############################
def railway_scraper():
    url="https://indianrailways.gov.in"
    r=safe_request(url)
    if r and r.status_code==200:
        soup=BeautifulSoup(r.text,"html.parser")
        title="Railway New Vacancy Notice Available..."
        jobs.append({
            "title": title,
            "vacancies": "Check Site",
            "qualification": "10th/ITI/Diploma/Graduate",
            "age": "18+",
            "salary": "As per Railway Rules",
            "last_date": "See Website",
            "state": "All India",
            "category": "Railway",
            "apply_link": url
        })
    else:
        fallback_railway()

def fallback_railway():
    jobs.append({
        "title": "Indian Railway Upcoming Recruitment",
        "vacancies": "Update Soon",
        "qualification": "10th/ITI/Diploma/Graduate",
        "age": "18+",
        "salary": "As per Railway Rules",
        "last_date": "Check Website",
        "state": "All India",
        "category": "Railway",
        "apply_link": "https://indianrailways.gov.in/"
    })

railway_scraper()

###############################
# 4. Banking Default
###############################
jobs.append({
    "title": "Bank Jobs IBPS/SBI Recruitment",
    "vacancies": "Soon",
    "qualification": "Graduate",
    "age": "20+",
    "salary": "Bank Rules",
    "last_date": "Update Soon",
    "state": "India",
    "category": "Banking",
    "apply_link": "https://ibps.in/"
})

###############################
# Save JSON
###############################
with open("jobs.json","w") as f:
    json.dump(jobs,f,indent=4)

print("Jobs Updated ✔",len(jobs))

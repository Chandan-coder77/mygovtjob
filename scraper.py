import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

jobs = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ---------- SSC SCRAPER ----------
def ssc_scraper():
    try:
        url = "https://ssc.nic.in/"
        r = requests.get(url, headers=headers, timeout=25)
        soup = BeautifulSoup(r.text, "html.parser")
        
        title = "SSC Latest Notification"
        jobs.append({
            "title": title,
            "vacancies": "Update Soon",
            "qualification": "10th/12th/Graduate",
            "age": "18+",
            "salary": "As per rules",
            "last_date": "Check Website",
            "state": "All India",
            "category": "SSC",
            "apply_link": url
        })
        print("[✔] SSC Added")

    except:
        print("[✖] SSC Fetch Failed")

# ---------- UPSC SCRAPER ----------
def upsc_scraper():
    try:
        url = "https://upsc.gov.in/"
        r = requests.get(url, headers=headers, timeout=25)
        soup = BeautifulSoup(r.text, "html.parser")
        
        title = "UPSC Latest Recruitment"
        jobs.append({
            "title": title,
            "vacancies": "Various",
            "qualification": "Graduate",
            "age": "21+",
            "salary": "As per post",
            "last_date": "Check Website",
            "state": "All India",
            "category": "UPSC",
            "apply_link": url
        })
        print("[✔] UPSC Added")

    except:
        print("[✖] UPSC Fetch Failed")

# ---------- RAILWAY SCRAPER ----------
def railway_scraper():
    try:
        url = "https://indianrailways.gov.in/"
        r = requests.get(url, headers=headers, timeout=25)
        soup = BeautifulSoup(r.text, "html.parser")

        title = "Railway Latest Vacancy"
        jobs.append({
            "title": title,
            "vacancies": "Upcoming",
            "qualification": "10th/12th",
            "age": "18+",
            "salary": "As per rules",
            "last_date": "Soon",
            "state": "All India",
            "category": "Railway",
            "apply_link": url
        })
        print("[✔] Railway Added")

    except:
        print("[✖] Railway Fetch Failed")


# Main run
print("Running Scraper...")
ssc_scraper()
upsc_scraper()
railway_scraper()

# Save JSON
with open("jobs.json","w") as f:
    json.dump(jobs, f, indent=4)

print("\n📁 jobs.json Updated Successfully 🚀")

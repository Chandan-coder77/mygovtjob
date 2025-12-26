import requests
from bs4 import BeautifulSoup
import json

# URL sources
sources = {
    "SSC": "https://ssc.nic.in/",
    "UPSC": "https://upsc.gov.in/",
    "Railway": "https://indianrailways.gov.in/",
    "Banking": "https://ibps.in/"
}

jobs = []

# ---------------- SSC Scraping -----------------
try:
    ssc_html = requests.get(sources["SSC"]).text
    ssc = BeautifulSoup(ssc_html, "html.parser")
    notice = ssc.find("span", {"class": "blink"}) or "Update Soon"

    jobs.append({
        "title": "SSC Latest Notification",
        "vacancies": "Update Soon",
        "qualification": "10th/12th/Graduate",
        "age": "18+",
        "salary": "As per SSC rules",
        "last_date": "Check Website",
        "state": "All India",
        "category": "SSC",
        "apply_link": sources["SSC"]
    })
except:
    print("SSC source fetch fail ❌")

# ---------------- UPSC Static until live -----------------
jobs.append({
    "title": "UPSC Recruitment Coming Soon",
    "vacancies": "Soon",
    "qualification": "Graduate",
    "age": "21+",
    "salary": "As per UPSC",
    "last_date": "Next Update",
    "state": "India",
    "category": "UPSC",
    "apply_link": sources["UPSC"]
})

# ---------------- Railway Static -----------------
jobs.append({
    "title": "Railway Recruitment - Coming Soon",
    "vacancies": "Update Soon",
    "qualification": "10th/ITI/Graduate",
    "age": "18+",
    "salary": "As per rules",
    "last_date": "Check Website",
    "state": "All India",
    "category": "Railway",
    "apply_link": sources["Railway"]
})

# ---------------- Bank Static -----------------
jobs.append({
    "title": "Bank Jobs (IBPS/SBI) Updates",
    "vacancies": "Soon",
    "qualification": "Graduate",
    "age": "20+",
    "salary": "As per Bank rules",
    "last_date": "Update Soon",
    "state": "India",
    "category": "Banking",
    "apply_link": sources["Banking"]
})

# Save JSON Output
with open("jobs.json", "w") as file:
    json.dump(jobs, file, indent=4)

print("Jobs Updated Successfully 🚀")

import requests
from bs4 import BeautifulSoup
import json

jobs = []

# ---------- SSC JOBS ----------
try:
    url = "https://ssc.nic.in/"
    r = requests.get(url,timeout=10)
    soup = BeautifulSoup(r.text,"html.parser")

    latest = soup.find_all("li")[:3]   # Top 3 latest news

    for item in latest:
        jobs.append({
            "title": item.text.strip(),
            "vacancies": "Update Soon",
            "qualification": "10th/12th/Graduate",
            "age": "18+",
            "salary": "As per notice",
            "last_date": "Check Notification",
            "state": "All India",
            "category": "SSC",
            "apply_link": url
        })
except:
    print("SSC fetch failed")

# ---------- UPSC JOBS ----------
try:
    url = "https://upsc.gov.in/"
    r = requests.get(url,timeout=10)
    soup = BeautifulSoup(r.text,"html.parser")

    latest = soup.find_all("li")[:3]

    for item in latest:
        jobs.append({
            "title": item.text.strip(),
            "vacancies": "Update Soon",
            "qualification": "Graduate",
            "age": "21+",
            "salary": "As per notice",
            "last_date": "Check Notification",
            "state": "All India",
            "category": "UPSC",
            "apply_link": url
        })
except:
    print("UPSC fetch failed")

# ---------- RAILWAY JOBS ----------
try:
    url = "https://indianrailways.gov.in/"
    r = requests.get(url,timeout=10)
    soup = BeautifulSoup(r.text,"html.parser")

    latest = soup.find_all("a")[:3]

    for item in latest:
        jobs.append({
            "title": item.text.strip(),
            "vacancies": "Update Soon",
            "qualification": "10th/12th/ITI",
            "age": "18+",
            "salary": "As per notice",
            "last_date": "Check Notification",
            "state": "All India",
            "category": "Railway",
            "apply_link": url
        })
except:
    print("Railway fetch failed")


# Save to jobs.json
with open("jobs.json","w",encoding="utf-8") as f:
    json.dump(jobs,f,indent=4,ensure_ascii=False)

print("Auto Updated Successfully ✔")

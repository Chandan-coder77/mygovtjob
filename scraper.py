import requests
from bs4 import BeautifulSoup
import json

jobs = []

# ---------------- SSC Scraper ----------------
try:
    url = "https://ssc.nic.in/"
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.text, "html.parser")
    title = soup.title.string.strip()

    jobs.append({
        "title": title,
        "vacancies": "Live Soon",
        "qualification": "10th/12th/Graduate",
        "age": "18+",
        "salary": "As per rules",
        "last_date": "Check Website",
        "state": "India",
        "category": "SSC",
        "apply_link": url
    })
except:
    print("SSC fetch error")

# ---------------- UPSC Scraper ----------------
try:
    url = "https://upsc.gov.in/"
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.text, "html.parser")
    title = soup.title.string.strip()

    jobs.append({
        "title": title,
        "vacancies": "Live Soon",
        "qualification": "Graduate",
        "age": "21+",
        "salary": "As per UPSC",
        "last_date": "Check Website",
        "state": "India",
        "category": "UPSC",
        "apply_link": url
    })
except:
    print("UPSC fetch error")

# ---------------- NCS (Central Govt Jobs) ----------------
try:
    url = "https://www.ncs.gov.in/"
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.text, "html.parser")
    title = soup.title.string.strip()

    jobs.append({
        "title": title,
        "vacancies": "Available Soon",
        "qualification": "Check Notification",
        "age": "NA",
        "salary": "As per post",
        "last_date": "Check Website",
        "state": "India",
        "category": "Central Govt",
        "apply_link": url
    })
except:
    print("NCS fetch error")

# -------- Save Results to jobs.json --------
with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=4)

print("Updated Successfully ✔")

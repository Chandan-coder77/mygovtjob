import requests
from bs4 import BeautifulSoup
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

jobs = []

# ================= SSC Scraper =================
def ssc_scraper():
    try:
        url = "https://ssc.nic.in/"
        r = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")

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
        print("SSC Data Added")
    except Exception as e:
        print("SSC Failed:", e)


# ================= UPSC Scraper =================
def upsc_scraper():
    try:
        url = "https://upsc.gov.in/"
        r = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(r.text, "html.parser")

        jobs.append({
            "title": "UPSC Latest Notification",
            "vacancies": "Update Soon",
            "qualification": "Graduate",
            "age": "21+",
            "salary": "As per rules",
            "last_date": "Check Website",
            "state": "All India",
            "category": "UPSC",
            "apply_link": "https://upsc.gov.in/"
        })
        print("UPSC Data Added")
    except Exception as e:
        print("UPSC Failed:", e)


# ================= Railway Scraper =================
def railway_scraper():
    try:
        url = "https://indianrailways.gov.in/"
        r = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(r.text, "html.parser")

        jobs.append({
            "title": "Railway Latest Jobs",
            "vacancies": "Update Soon",
            "qualification": "10th/12th/ITI/Graduate",
            "age": "18+",
            "salary": "As per Rules",
            "last_date": "Check Website",
            "state": "All India",
            "category": "Railway",
            "apply_link": "https://indianrailways.gov.in/"
        })
        print("Railway Added")
    except Exception as e:
        print("Railway Failed:", e)


# ================= Run All =================
if __name__ == "__main__":
    print("Starting Scraper...")

    ssc_scraper()
    time.sleep(2)

    upsc_scraper()
    time.sleep(2)

    railway_scraper()

    with open("jobs.json", "w") as f:
        json.dump(jobs, f, indent=4)

    print("Jobs Updated Successfully!")

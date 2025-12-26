import requests
from bs4 import BeautifulSoup
import json

# ---------------- SSC Scraper ---------------- #

def fetch_ssc_jobs():
    url = "https://ssc.nic.in/"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        notice = soup.select_one(".notice-board a")   # Live Notice
        if notice:
            title = notice.text.strip()
        else:
            title = "SSC Latest Notification"

        return {
            "title": title,
            "vacancies": "Update Soon",
            "qualification": "10th/12th/Graduate",
            "age": "18+",
            "salary": "As per SSC rules",
            "last_date": "Check Website",
            "state": "All India",
            "category": "SSC",
            "apply_link": "https://ssc.nic.in/"
        }
    except:
        return {
            "title": "SSC Latest Notification",
            "vacancies": "Update Soon",
            "qualification": "10th/12th/Graduate",
            "age": "18+",
            "salary": "As per SSC rules",
            "last_date": "Check Website",
            "state": "All India",
            "category": "SSC",
            "apply_link": "https://ssc.nic.in/"
        }


# ---------------- UPSC ---------------- #
def fetch_upsc_jobs():
    return {
        "title": "UPSC Recruitment Coming Soon",
        "vacancies": "Soon",
        "qualification": "Graduate",
        "age": "21+",
        "salary": "As per UPSC",
        "last_date": "Next Update",
        "state": "India",
        "category": "UPSC",
        "apply_link": "https://upsc.gov.in/examinations/ActiveExams"
    }


# ---------------- Railway ---------------- #
def fetch_railway_jobs():
    return {
        "title": "Railway Recruitment - Coming Soon",
        "vacancies": "Update Soon",
        "qualification": "10th/ITI/Graduate",
        "age": "18+",
        "salary": "As per rules",
        "last_date": "Check Website",
        "state": "All India",
        "category": "Railway",
        "apply_link": "https://indianrailways.gov.in/"
    }


# ---------------- Banking ---------------- #
def fetch_bank_jobs():
    return {
        "title": "Bank Jobs (IBPS/SBI) Updates",
        "vacancies": "Soon",
        "qualification": "Graduate",
        "age": "20+",
        "salary": "As per Bank rules",
        "last_date": "Update Soon",
        "state": "India",
        "category": "Banking",
        "apply_link": "https://ibps.in/"
    }


# --------- Generate jobs.json --------- #

jobs = [
    fetch_ssc_jobs(),
    fetch_upsc_jobs(),
    fetch_railway_jobs(),
    fetch_bank_jobs()
]

with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=4)

print("Updated Successfully 🔥")

import requests
from bs4 import BeautifulSoup
import json, datetime

jobs = []

def add_job(title, vacancies, qualification, age, salary, last_date, state, category, apply_link):
    jobs.append({
        "title": title,
        "vacancies": vacancies,
        "qualification": qualification,
        "age": age,
        "salary": salary,
        "last_date": last_date,
        "state": state,
        "category": category,
        "apply_link": apply_link
    })

# ========== SSC LIVE SCRAPER ==========
def ssc_scraper():
    url = "https://ssc.nic.in/"
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        latest = soup.find("div", {"id": "latestnews"})
        if latest:
            title = latest.text.strip().split("\n")[0][:80]  # shorten
        else:
            title = "SSC Latest Notification"

        add_job(
            title=title,
            vacancies="Update Soon",
            qualification="10th/12th/Graduate",
            age="18+",
            salary="As per SSC rules",
            last_date="Check Website",
            state="All India",
            category="SSC",
            apply_link=url
        )
    except:
        # fallback static entry if scraping fails
        add_job(
            "SSC Latest Jobs", "Update Soon", "10th/12th/Graduate", "18+",
            "As per rules", "Check Website", "All India", "SSC", "https://ssc.nic.in/"
        )

# ========== UPSC STATIC TEMP (live after SSC works) ==========
def upsc():
    add_job(
        "UPSC Recruitment Coming Soon", "Soon", "Graduate", "21+",
        "As per UPSC", "Next Update", "India", "UPSC", "https://upsc.gov.in/"
    )

def railway():
    add_job(
        "Railway Recruitment - Coming Soon", "Update Soon", "10th/ITI/Graduate", "18+",
        "As per rules", "Check Website", "All India", "Railway", "https://indianrailways.gov.in/"
    )

def banking():
    add_job(
        "Bank Jobs (IBPS/SBI) Updates", "Soon", "Graduate", "20+",
        "As per Bank rules", "Update Soon", "India", "Banking", "https://ibps.in/"
    )


# RUN ALL
ssc_scraper()
upsc()
railway()
banking()

# save output
with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=4)

print("Jobs Updated Successfully", datetime.datetime.now())

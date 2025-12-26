import requests
from bs4 import BeautifulSoup
import json

# Master list for all jobs
jobs = []

# ------------------- ADD JOB FUNCTION -------------------
def add_job(title, vacancies, qualification, age, salary, last_date, state, category, link):
    jobs.append({
        "title": title,
        "vacancies": vacancies,
        "qualification": qualification,
        "age": age,
        "salary": salary,
        "last_date": last_date,
        "state": state,
        "category": category,
        "apply_link": link
    })


# ===================== 1. SSC Scraper =====================
def ssc_scraper():
    print("Fetching SSC...")
    url = "https://ssc.nic.in/"
    try:
        requests.get(url, timeout=15)
        add_job(
            "SSC Latest Notification",
            "Update Soon",
            "10th/12th/Graduate",
            "18+",
            "As per rules",
            "Check Website",
            "All India",
            "SSC",
            url
        )
        print("SSC Added ✔")
    except:
        print("SSC Failed ❌")


# ===================== 2. UPSC Scraper (Improved) =====================
def upsc_scraper():
    print("Fetching UPSC...")
    url = "https://upsc.gov.in/examinations/active-examinations"
    try:
        r = requests.get(url, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")

        for row in soup.select(".views-row")[:5]:
            try:
                title = row.find("a").text.strip()
                link = "https://upsc.gov.in" + row.find("a")["href"]

                add_job(
                    title,
                    "As per post",
                    "Graduate/PG",
                    "21+",
                    "As per rules",
                    "Check Notification",
                    "All India",
                    "UPSC",
                    link
                )
            except:
                pass

        print("UPSC Added ✔")
    except:
        print("UPSC Timeout/Fail ❌ (Backup Entry Added)")
        add_job("UPSC Recruitment Coming Soon", "Soon", "Graduate", "21+", "Rules as per UPSC", "Next Update", "India", "UPSC", "https://upsc.gov.in/")


# ===================== 3. Railway Scraper (Improved) =====================
def railway_scraper():
    print("Fetching Railway...")
    url = "https://www.rrbcdg.gov.in/"
    try:
        r = requests.get(url, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup.select("a")[:5]:
            text = tag.text.strip()
            if "recruit" in text.lower() or "job" in text.lower() or "notice" in text.lower():
                add_job(
                    text,
                    "Update Soon",
                    "10th/12th/ITI/Diploma",
                    "18+",
                    "As per rules",
                    "Check Site",
                    "All India",
                    "Railway",
                    url
                )

        print("Railway Added ✔")
    except:
        print("Railway Failed ❌ (Backup Entry Added)")
        add_job("Railway Recruitment", "Upcoming", "10th/ITI", "18+", "Govt Pay", "Soon", "India", "Railway", "https://www.rrbcdg.gov.in/")


# ===================== RUN ALL SCRAPERS =====================
ssc_scraper()
upsc_scraper()
railway_scraper()

# Save to JSON
with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=4)

print("\n✔ All Job Data Updated Successfully!")

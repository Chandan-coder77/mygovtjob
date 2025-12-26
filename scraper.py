import requests
from bs4 import BeautifulSoup
import json

# Output file
OUTPUT = "jobs.json"


# -------------------------- SSC SCRAPER --------------------------
def scrape_ssc():
    url = "https://ssc.nic.in/"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        notice = soup.find("span", {"id": "lblLatestNews"})  # Try latest section
        title = notice.text.strip() if notice else "SSC Latest Notification"

        return {
            "title": title,
            "vacancies": "Update Soon",
            "qualification": "10th/12th/Graduate",
            "age": "18+",
            "salary": "As per SSC rules",
            "last_date": "Check Website",
            "state": "All India",
            "category": "SSC",
            "apply_link": url
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
            "apply_link": url
        }



# -------------------------- UPSC SCRAPER --------------------------
def scrape_upsc():
    url = "https://upsc.gov.in/"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text,"html.parser")

        latest = soup.find("div", class_="views-field-title")
        title = latest.text.strip() if latest else "UPSC Recruitment Coming Soon"

        return {
            "title": title,
            "vacancies": "Soon",
            "qualification": "Graduate",
            "age": "21+",
            "salary": "As per UPSC",
            "last_date": "Next Update",
            "state": "India",
            "category": "UPSC",
            "apply_link": "https://upsc.gov.in/examinations/ActiveExams"
        }

    except:
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


# -------------------------- RAILWAY SCRAPER --------------------------
def scrape_railway():
    url = "https://indianrailways.gov.in/"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text,"html.parser")

        news = soup.find("a")  # Railway site has PDF links mostly
        title = news.text.strip() if news else "Railway Recruitment - Coming Soon"

        return {
            "title": title,
            "vacancies": "Update Soon",
            "qualification": "10th/ITI/Graduate",
            "age": "18+",
            "salary": "As per Railway rules",
            "last_date": "Check Website",
            "state": "All India",
            "category": "Railway",
            "apply_link": url
        }

    except:
        return {
            "title": "Railway Recruitment - Coming Soon",
            "vacancies": "Update Soon",
            "qualification": "10th/ITI/Graduate",
            "age": "18+",
            "salary": "As per Railway rules",
            "last_date": "Check Website",
            "state": "All India",
            "category": "Railway",
            "apply_link": url
        }


# -------------------------- BANK / IBPS SCRAPER --------------------------
def scrape_bank():
    url = "https://ibps.in/"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text,"html.parser")

        title_el = soup.find("marquee")
        title = title_el.text.strip() if title_el else "Bank Jobs (IBPS/SBI) Updates"

        return {
            "title": title,
            "vacancies": "Soon",
            "qualification": "Graduate",
            "age": "20+",
            "salary": "As per Bank rules",
            "last_date": "Update Soon",
            "state": "India",
            "category": "Banking",
            "apply_link": url
        }
    except:
        return {
            "title": "Bank Jobs (IBPS/SBI) Updates",
            "vacancies": "Soon",
            "qualification": "Graduate",
            "age": "20+",
            "salary": "As per Bank rules",
            "last_date": "Update Soon",
            "state": "India",
            "category": "Banking",
            "apply_link": url
        }



# -------------------------- MERGE + SAVE JSON --------------------------
jobs = [
    scrape_ssc(),
    scrape_upsc(),
    scrape_railway(),
    scrape_bank()
]

with open(OUTPUT, "w") as f:
    json.dump(jobs, f, indent=4)

print("Job Data Updated Successfully 🚀")

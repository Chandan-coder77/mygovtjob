import requests
from bs4 import BeautifulSoup
import json

jobs = []

# ----------------------- SSC -----------------------
def fetch_ssc():
    url = "https://ssc.nic.in/"
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        notice = soup.find("div", {"id":"kCarousel"})  # Latest Notification block

        title = notice.text.strip().split("\n")[0] if notice else "SSC Latest Jobs"
        
        jobs.append({
            "title": title,
            "vacancies": "Update Soon",
            "qualification": "10th/12th/Graduate",
            "age": "18+",
            "salary": "As per rules",
            "last_date": "Check Website",
            "state": "All India",
            "category": "SSC",
            "apply_link": "https://ssc.nic.in/"
        })
    except:
        pass


# ----------------------- UPSC -----------------------
def fetch_upsc():
    url = "https://upsc.gov.in/"
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.find("marquee").text.strip() if soup.find("marquee") else "UPSC Latest Notification"

        jobs.append({
            "title": title,
            "vacancies": "Update Soon",
            "qualification": "Graduate",
            "age": "21+",
            "salary": "As per rules",
            "last_date": "Check Website",
            "state": "All India",
            "category": "UPSC",
            "apply_link": url
        })
    except:
        pass


# ----------------------- Railway -----------------------
def fetch_railway():
    url = "https://indianrailways.gov.in/"
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        title = "Railway Recruitment Latest"
        jobs.append({
            "title": title,
            "vacancies": "Update Soon",
            "qualification": "10th/ITI/Diploma/Graduate",
            "age": "18-30",
            "salary": "₹21,700+",
            "last_date": "Official Notice Soon",
            "state": "All India",
            "category": "Railway",
            "apply_link": url
        })
    except:
        pass


# ------------ run scrapers -------------
fetch_ssc()
fetch_upsc()
fetch_railway()

# Save to jobs.json
with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=4)

print("Jobs Updated Successfully!")

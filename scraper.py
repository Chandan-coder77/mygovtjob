import requests
from bs4 import BeautifulSoup
import json

# ---------------- Source URLs ----------------
sources = {
    "SSC": "https://ssc.nic.in/",
    "UPSC": "https://upsc.gov.in/examinations/ActiveExams",
    "Railway": "https://indianrailways.gov.in/",
    "Banking": "https://ibps.in/"
}

jobs = []

# ---------------- SSC Static ----------------
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

# ---------------- LIVE UPSC SCRAPER ----------------
try:
    upsc_html = requests.get(sources["UPSC"], timeout=10).text
    soup = BeautifulSoup(upsc_html, "html.parser")

    exam_block = soup.find("table")  # UPSC active exam table
    exam_name = exam_block.find("a").text.strip() if exam_block else "UPSC New Notice Soon"
    exam_link = "https://upsc.gov.in" + exam_block.find("a")["href"] if exam_block else sources["UPSC"]

    jobs.append({
        "title": exam_name,
        "vacancies": "As per UPSC notice",
        "qualification": "Graduate",
        "age": "21+",
        "salary": "As per Rules",
        "last_date": "Check Notification",
        "state": "India",
        "category": "UPSC",
        "apply_link": exam_link
    })

except Exception as e:
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

# ---------------- RAILWAY Static ----------------
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

# ---------------- BANKING Static ----------------
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

# Save Output
with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=4)

print("🔥 Auto Job Update Completed Successfully")

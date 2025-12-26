import json, requests
from bs4 import BeautifulSoup

jobs = []

sources = {
    "SSC": "https://ssc.nic.in/",
    "UPSC": "https://upsc.gov.in/examinations/ActiveExams",
    "RAILWAY": "https://indianrailways.gov.in/",
    "BANK": "https://ibps.in/"
}


# ---------------- SSC Scraper ----------------
try:
    ssc_html = requests.get(sources["SSC"], timeout=15).text
    soup = BeautifulSoup(ssc_html, "html.parser")

    title = soup.find("title").text.strip() if soup.find("title") else "SSC Latest Notification"

    jobs.append({
        "title": title,
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



# ---------------- UPSC Live Scraper (New V2) ----------------
try:
    up_html = requests.get(sources["UPSC"], timeout=15).text
    soup2 = BeautifulSoup(up_html, "html.parser")

    exam = soup2.select_one("table a")   # पहला active exam title fetch
    if exam:
        exam_title = exam.text.strip()
        link = "https://upsc.gov.in" + exam.get("href")

        jobs.append({
            "title": exam_title,
            "vacancies": "As per notification",
            "qualification": "Graduate",
            "age": "21+",
            "salary": "As per UPSC rules",
            "last_date": "Check official website",
            "state": "India",
            "category": "UPSC",
            "apply_link": link
        })
    else:
        raise Exception("Exam not found")

except:
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



# ---------------- Railway fallback ----------------
jobs.append({
    "title": "Railway Recruitment - Coming Soon",
    "vacancies": "Update Soon",
    "qualification": "10th/ITI/Graduate",
    "age": "18+",
    "salary": "As per rules",
    "last_date": "Check Website",
    "state": "All India",
    "category": "Railway",
    "apply_link": sources["RAILWAY"]
})


# ---------------- BANK fallback ----------------
jobs.append({
    "title": "Bank Jobs (IBPS/SBI) Updates",
    "vacancies": "Soon",
    "qualification": "Graduate",
    "age": "20+",
    "salary": "As per Bank rules",
    "last_date": "Update Soon",
    "state": "India",
    "category": "Banking",
    "apply_link": sources["BANK"]
})


# ---------------- Save Output ----------------
with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=4)

print("jobs.json updated successfully!")

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os
from pdfminer.high_level import extract_text

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "jobs.json"

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_pdf_text(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        file = "temp.pdf"
        with open(file, "wb") as f:
            f.write(r.content)
        text = extract_text(file)
        os.remove(file)
        return clean_text(text)
    except:
        return ""

def deep_extract(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        tables = soup.find_all("table")
        text = soup.get_text(" ")

        qualification = salary = age = vacancy = last_date = ""

        # ---------- Scan Tables Smart ----------
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cols = [clean_text(i.get_text()) for i in row.find_all(["td","th"])]

                if len(cols) < 2: continue

                if "Qualification" in cols[0] or "Education" in cols[0]:
                    qualification = cols[1]
                if "Salary" in cols[0] or "Pay" in cols[0]:
                    salary = cols[1]
                if "Age" in cols[0]:
                    age = cols[1]
                if "Post" in cols[0] and re.search(r"\d", cols[1]):
                    vacancy = cols[1]
                if "Last Date" in cols[0] or "Last date" in cols[0]:
                    last_date = cols[1]

        # ---------- Backup Condition from Text (AI pattern mode) ----------
        if qualification == "":
            match = re.search(r'(Matric|10th|12th|Graduate|Bachelor|Diploma|ITI|Any Degree)', text, re.I)
            if match: qualification = match.group(1)

        if salary == "":
            match = re.search(r'₹\s?\d[\d,]+', text)
            if match: salary = match.group(0)

        if last_date == "":
            match = re.search(r'\d{2}/\d{2}/\d{4}', text)
            if match: last_date = match.group(0)

        if age == "":
            match = re.search(r'\d{2}\s?to\s?\d{2}|\d{2}-\d{2}', text)
            if match: age = match.group(0)

        # --------- PDF Link Detection ----------
        for link in soup.find_all("a"):
            href = link.get("href","")
            if href.endswith(".pdf"):
                pdf = extract_pdf_text(href if "http" in href else url+href)
                if qualification == "":
                    m = re.search(r'(Matric|10th|12th|Graduate|Diploma|ITI)', pdf, re.I)
                    if m: qualification = m.group(1)
                if salary == "":
                    m = re.search(r'₹\s?\d[\d,]+', pdf)
                    if m: salary = m.group(0)

        return {
            "qualification": qualification,
            "salary": salary,
            "age_limit": age,
            "vacancy": vacancy,
            "last_date": last_date
        }

    except:
        return {}

def is_valid_job(title):
    block = ["Admit Card","Result","Hall Ticket","Answer Key"]
    return not any(b in title for b in block)

def process():
    jobs = []
    if not os.path.exists(SOURCE_FILE):
        print("❌ sources.txt missing")
        return

    with open(SOURCE_FILE) as f:
        links = [x.strip() for x in f.readlines() if x.strip()]

    for url in links:
        print(f"🔍 Checking {url}")
        try:
            r = requests.get(url, headers=HEADERS,timeout=15)
            soup = BeautifulSoup(r.text,"html.parser")

            for a in soup.find_all("a"):
                link = a.get("href","")
                text = clean_text(a.get_text())

                if not is_valid_job(text): continue
                if "recruitment" not in text.lower() and "form" not in text.lower(): continue
                if not link.startswith("http"):
                    link = url.rstrip("/")+"/"+link.lstrip("/")

                print("📌 Job Found:",text)

                info = deep_extract(link)

                jobs.append({
                    "title": text,
                    "apply_link": link,
                    "qualification": info.get("qualification",""),
                    "salary": info.get("salary",""),
                    "age_limit": info.get("age_limit",""),
                    "vacancy": info.get("vacancy",""),
                    "last_date": info.get("last_date","")
                })

        except Exception as e:
            print("⚠ Error:",e)

        time.sleep(2)

    with open(OUTPUT_FILE,"w") as f:
        json.dump(jobs,f,indent=4)

    print("✅ Scraper Stage-9 Complete — Auto Extracted 🔥")

if __name__ == "__main__":
    process()

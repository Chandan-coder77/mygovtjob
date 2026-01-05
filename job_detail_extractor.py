# ==========================================
# 🧠 STAGE-A5.4.1
# JOB DETAIL EXTRACTOR (HTML + PDF)
# FIXED USER-AGENT VERSION
# ==========================================

import json
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

# =========================
# CONFIG
# =========================
INPUT_FILE = "jobs.json"
OUTPUT_FILE = "jobs.json"
TIMEOUT = 20

# ✅ EXACT USER-AGENT (AS YOU SAID)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}

# =========================
# REGEX PATTERNS
# =========================
DATE_REGEX = r"\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})\b"
VACANCY_REGEX = r"\b(\d{2,6})\s+(posts|vacancies|vacancy)\b"
AGE_REGEX = r"(\d{2})\s*(to|-)\s*(\d{2})\s*years"
SALARY_REGEX = r"(₹|rs\.?)\s?[\d,]+"

# =========================
# UTILS
# =========================
def safe_get(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code == 200 and len(r.text) > 500:
            return r.text
    except Exception:
        pass
    return None

def clean(text):
    return re.sub(r"\s+", " ", (text or "")).strip()

def valid_date(d):
    try:
        datetime.strptime(d, "%d/%m/%Y")
        return True
    except:
        return False

# =========================
# HTML EXTRACTION
# =========================
def extract_from_html(html):
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")

    result = {}

    # ---- Last Date ----
    dates = re.findall(DATE_REGEX, text)
    dates = [d.replace("-", "/") for d in dates if valid_date(d.replace("-", "/"))]
    if dates:
        result["last_date"] = dates[-1]

    # ---- Vacancy ----
    vac = re.search(VACANCY_REGEX, text, re.I)
    if vac:
        num = vac.group(1)
        if num.isdigit() and int(num) > 10:
            result["vacancy"] = num

    # ---- Age Limit ----
    age = re.search(AGE_REGEX, text, re.I)
    if age:
        result["age_limit"] = f"{age.group(1)}-{age.group(3)}"

    # ---- Salary ----
    sal = re.search(SALARY_REGEX, text, re.I)
    if sal:
        result["salary"] = sal.group(0)

    # ---- PDF Links ----
    pdfs = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(".pdf"):
            pdfs.append(href)

    result["pdf_links"] = pdfs
    return result

# =========================
# PDF EXTRACTION (LIMITED)
# =========================
def extract_from_pdf_links(pdf_links, base_url):
    try:
        from pdfminer.high_level import extract_text
    except:
        return {}

    for link in pdf_links[:2]:  # safety limit
        pdf_url = urljoin(base_url, link)
        try:
            text = extract_text(pdf_url)
            if not text:
                continue

            text = clean(text)
            result = {}

            dates = re.findall(DATE_REGEX, text)
            dates = [d.replace("-", "/") for d in dates if valid_date(d.replace("-", "/"))]
            if dates:
                result["last_date"] = dates[-1]

            vac = re.search(VACANCY_REGEX, text, re.I)
            if vac:
                num = vac.group(1)
                if num.isdigit() and int(num) > 10:
                    result["vacancy"] = num

            age = re.search(AGE_REGEX, text, re.I)
            if age:
                result["age_limit"] = f"{age.group(1)}-{age.group(3)}"

            sal = re.search(SALARY_REGEX, text, re.I)
            if sal:
                result["salary"] = sal.group(0)

            if result:
                return result

        except Exception:
            continue

    return {}

# =========================
# MAIN ENGINE
# =========================
def run():
    if not os.path.exists(INPUT_FILE):
        print("❌ jobs.json not found")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    enriched = 0

    for job in jobs:
        url = job.get("apply_link")
        if not url:
            continue

        html = safe_get(url)
        if not html:
            continue

        html_data = extract_from_html(html)
        pdf_data = {}

        if html_data.get("pdf_links"):
            pdf_data = extract_from_pdf_links(html_data["pdf_links"], url)

        # Priority: PDF > HTML > existing
        for key in ["last_date", "vacancy", "age_limit", "salary"]:
            if key in pdf_data:
                job[key] = pdf_data[key]
            elif key in html_data:
                job[key] = html_data[key]

        job["detail_checked"] = True
        job["detail_checked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        enriched += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)

    print("✅ STAGE-A5.4.1 COMPLETE")
    print(f"📄 Jobs scanned   : {len(jobs)}")
    print(f"🧠 Jobs enriched : {enriched}")

# =========================
if __name__ == "__main__":
    run()

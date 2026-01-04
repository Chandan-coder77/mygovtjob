# ==============================
# 🤖 AI CORRECTOR SMART UPDATE (V2 - HARD SAFE MODE)
# ==============================

import os
import re
import json
import requests
from bs4 import BeautifulSoup
from value_extractor import extract_values

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

PDF_TMP = "temp_pdf.txt"
PDF_FILE = "temp.pdf"
JOBS_FILE = "jobs.json"

# -----------------------------------------
# PDF DOWNLOAD + TEXT EXTRACT (SAFE)
# -----------------------------------------
def extract_pdf_text(url):
    if not url or not isinstance(url, str):
        return ""

    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        with open(PDF_FILE, "wb") as f:
            f.write(r.content)

        os.system(f"pdf2txt.py {PDF_FILE} > {PDF_TMP}")

        if os.path.exists(PDF_TMP):
            with open(PDF_TMP, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().lower().replace("\n", " ")

    except:
        return ""

    return ""

# -----------------------------------------
# Deep Scrape (HTML + 2nd Link + PDF)
# -----------------------------------------
def deep_scrape(url, depth=0):
    if not url or not isinstance(url, str) or depth > 2:
        return ""

    try:
        r = requests.get(url, headers=HEADERS, timeout=25)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ", strip=True).lower()

        # If text too small → try 2nd link
        if len(text) < 200:
            for a in soup.select("a[href]")[:5]:
                link = a.get("href")
                if link and link.startswith("http"):
                    return deep_scrape(link, depth + 1)

        # Scan PDFs
        for p in soup.select("a[href$='.pdf']")[:3]:
            pdf_text = extract_pdf_text(p.get("href"))
            if len(pdf_text) > 200:
                text += " " + pdf_text

        return text

    except:
        return ""

# -----------------------------------------
# AI FIX LOGIC (HARD SAFE)
# -----------------------------------------
def fix_job(job):
    # 🔥 HARD TYPE CHECK
    if not isinstance(job, dict):
        return job

    url = job.get("apply_link")
    page_text = deep_scrape(url)

    if not page_text:
        return job

    # QUALIFICATION
    if not job.get("qualification"):
        if "10th" in page_text or "matric" in page_text:
            job["qualification"] = "10th"
        elif "12th" in page_text or "intermediate" in page_text:
            job["qualification"] = "12th"
        elif "iti" in page_text:
            job["qualification"] = "ITI"
        elif "diploma" in page_text:
            job["qualification"] = "Diploma"
        elif "engineer" in page_text or "b.tech" in page_text:
            job["qualification"] = "Engineering"
        elif "graduate" in page_text or "bachelor" in page_text:
            job["qualification"] = "Graduate"
        elif "post graduate" in page_text or "master" in page_text:
            job["qualification"] = "Post Graduate"

    # SALARY
    if not job.get("salary"):
        s = re.findall(r"₹\s?\d[\d,]{3,8}", page_text)
        if s:
            job["salary"] = s[0]

    # AGE LIMIT
    if not job.get("age_limit"):
        a = re.findall(r"\b\d{1,2}\s?-\s?\d{1,2}\b", page_text)
        if a:
            job["age_limit"] = a[0]

    # VACANCY
    if not job.get("vacancy"):
        v = re.findall(r"vacanc(?:y|ies)\s*[:\-]?\s*(\d{1,6})", page_text)
        if v:
            job["vacancy"] = v[0]

    # LAST DATE
    if not job.get("last_date"):
        d = re.findall(r"\d{1,2}/\d{1,2}/\d{4}", page_text)
        if d:
            job["last_date"] = d[-1]

    # Final normalize
    try:
        job = extract_values(job)
    except:
        pass

    return job

# ===================================================
# MAIN PROCESS (HARD SAFE)
# ===================================================
def main():
    if not os.path.exists(JOBS_FILE):
        print("❌ jobs.json missing")
        return

    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except:
            print("❌ jobs.json invalid")
            return

    updated = []

    for job in data:
        try:
            updated.append(fix_job(job))
        except:
            updated.append(job)

    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=4, ensure_ascii=False)

    print("\n✅ AI Corrector V2 SAFE COMPLETE")
    print("📌 HTML + PDF + 2nd level links scanned")
    print("📌 No crash guarantee\n")

# ==============================
if __name__ == "__main__":
    main()

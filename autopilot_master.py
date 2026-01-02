import os
import json
import time
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 🔥 PDF reader import (Stage-A2)
from pdf_reader import extract_from_pdf, find_pdf_links

# ==============================
# 🔥 Stage-A1 + A2 Autopilot Master Engine
# ==============================

JOBS_FILE = "jobs.json"
LOG_FILE = "autopilot_log.txt"

# ✅ Strong Browser-like Headers (IMPORTANT)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

# ==============================
# Utility Functions
# ==============================

def log(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")


def load_jobs():
    if not os.path.exists(JOBS_FILE):
        return []
    try:
        with open(JOBS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_jobs(data):
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ==============================
# 🔍 Smart Field Extractor (HTML + PDF)
# ==============================
def extract_details_from_page(url):
    result = {
        "salary": "",
        "qualification": "",
        "age_limit": "",
        "vacancy": "",
        "last_date": ""
    }

    try:
        response = requests.get(url, headers=HEADERS, timeout=25)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # ==============================
        # 🔥 Stage-A2 → PDF Priority Scan
        # ==============================
        pdf_links = find_pdf_links(html)
        if pdf_links:
            log(f"📄 PDF found → {pdf_links[0]}")
            pdf_data = extract_from_pdf(pdf_links[0])
            return pdf_data

        # ==============================
        # HTML Text Fallback
        # ==============================
        text = soup.get_text(" ", strip=True).lower()

        result["salary"] = extract_value(
            text, ["₹", "salary", "pay scale", "pay level"]
        )

        result["qualification"] = extract_value(
            text,
            [
                "qualification", "education", "10th", "12th",
                "iti", "diploma", "graduate", "b.sc",
                "b.tech", "engineering"
            ]
        )

        result["age_limit"] = extract_age(text)
        result["last_date"] = extract_date(text)
        result["vacancy"] = extract_vacancy(text)

    except Exception as e:
        log(f"[ERROR] {url} -> {e}")

    return result


# ==============================
# Extraction Helpers
# ==============================

def extract_value(text, keywords):
    for key in keywords:
        if key in text:
            idx = text.index(key)
            chunk = text[idx: idx + 100]
            return " ".join(chunk.split()[:10])
    return ""


def extract_date(text):
    dates = re.findall(r"\b\d{1,2}/\d{1,2}/\d{4}\b", text)
    return dates[0] if dates else ""


def extract_age(text):
    age = re.findall(r"\b\d{2}\s?-\s?\d{2}\b", text)
    return age[0].replace(" ", "") if age else ""


def extract_vacancy(text):
    v = re.findall(r"vacanc(?:y|ies)\s*[:\-]?\s*(\d{1,5})", text)
    if v:
        return v[0]
    nums = re.findall(r"\b\d{2,5}\b", text)
    return nums[0] if nums else ""


# ==============================
# 🚀 Autopilot Engine Runner
# ==============================
def autopilot_run():
    log("=== 🚀 Autopilot Engine Started ===")

    jobs = load_jobs()
    updated_jobs = []

    for job in jobs:
        url = job.get("apply_link")
        log(f"🔍 Scanning → {job.get('title')}")

        data = extract_details_from_page(url)

        # Smart merge logic (blank-only fill)
        for key in ["salary", "qualification", "age_limit", "vacancy", "last_date"]:
            if not job.get(key) and data.get(key):
                job[key] = data[key]

        updated_jobs.append(job)
        time.sleep(2)  # anti-block delay

    save_jobs(updated_jobs)
    log("=== ✅ Autopilot Engine Completed ===")


# ==============================
# Direct Run
# ==============================
if __name__ == "__main__":
    autopilot_run()

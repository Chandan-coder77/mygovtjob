import os
import json
import time
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 🔥 Stage-A2 PDF reader
from pdf_reader import extract_from_pdf, find_pdf_links

# 🔥 Stage-A3 Navigator brain
from navigator_a3 import (
    crawl_with_depth,
    extract_best_text,
    select_best_text
)

# ==============================
# CONFIG
# ==============================
JOBS_FILE = "jobs.json"
LOG_FILE = "autopilot_log.txt"

# ✅ Strong Browser-like headers
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

# ==============================
# Utility
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
# 🔍 CORE EXTRACTOR (HTML + PDF + MULTI-PAGE)
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
        # ==============================
        # MAIN PAGE LOAD
        # ==============================
        response = requests.get(url, headers=HEADERS, timeout=25)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # ==============================
        # Stage-A2 → PDF Priority
        # ==============================
        pdf_links = find_pdf_links(html)
        if pdf_links:
            log(f"📄 PDF found → {pdf_links[0]}")
            pdf_data = extract_from_pdf(pdf_links[0])
            if pdf_data:
                log("✅ Data extracted from PDF")
                return pdf_data

        # ==============================
        # Stage-A3 → Multi-Page Crawl
        # ==============================
        log("🔁 Stage-A3: crawling internal pages…")
        pages = crawl_with_depth(url, depth=2)

        texts = extract_best_text(pages)
        best_text, score = select_best_text(texts)

        if score > 0:
            log(f"🧠 Best data selected (confidence={score})")
            combined_text = best_text.lower()
        else:
            log("⚠️ Fallback to main page text")
            combined_text = soup.get_text(" ", strip=True).lower()

        # ==============================
        # FINAL EXTRACTION
        # ==============================
        result["salary"] = extract_value(
            combined_text,
            ["₹", "salary", "pay scale", "pay level", "per month"]
        )

        result["qualification"] = extract_value(
            combined_text,
            [
                "qualification", "education", "10th", "12th",
                "iti", "diploma", "graduate", "b.sc",
                "b.tech", "engineering", "degree"
            ]
        )

        result["age_limit"] = extract_age(combined_text)
        result["last_date"] = extract_date(combined_text)
        result["vacancy"] = extract_vacancy(combined_text)

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
            chunk = text[idx: idx + 120]
            return " ".join(chunk.split()[:12])
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
# 🚀 AUTOPILOT RUNNER
# ==============================
def autopilot_run():
    log("=== 🚀 Autopilot Engine Started (A1 + A2 + A3 FINAL) ===")

    jobs = load_jobs()
    updated_jobs = []

    for job in jobs:
        url = job.get("apply_link")
        title = job.get("title", "")
        log(f"🔍 Scanning → {title}")

        data = extract_details_from_page(url)

        # 🔥 Smart merge (only fill blanks)
        for key in ["salary", "qualification", "age_limit", "vacancy", "last_date"]:
            if not job.get(key) and data.get(key):
                job[key] = data[key]

        updated_jobs.append(job)
        time.sleep(2)  # anti-block safety

    save_jobs(updated_jobs)
    log("=== ✅ Autopilot Engine Completed ===")


# ==============================
# DIRECT RUN
# ==============================
if __name__ == "__main__":
    autopilot_run()

# ==============================
# 🚀 AUTOPILOT MASTER (SAFE MODE)
# ==============================

import os
import json
import time
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from pdf_reader import extract_from_pdf, find_pdf_links
from navigator_a3 import crawl_with_depth, extract_best_text, select_best_text
from confidence_engine import evaluate_job, CONFIDENCE_THRESHOLD
from global_optimizer import optimize_jobs

# ==============================
# CONFIG
# ==============================
JOBS_FILE = "jobs.json"
LOG_FILE = "autopilot_log.txt"

MAX_JOBS_PER_RUN = 50        # 🔥 MAIN FIX
MAX_JOB_TIME = 35            # ⏱ per job seconds

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

CRAWLED_CACHE = set()

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
def extract_details_from_page(url):
    start = time.time()

    result = {
        "salary": "",
        "qualification": "",
        "age_limit": "",
        "vacancy": "",
        "last_date": "",
        "_source": "HTML"
    }

    if url in CRAWLED_CACHE:
        return result

    CRAWLED_CACHE.add(url)

    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")

        # ⏱ TIME GUARD
        if time.time() - start > MAX_JOB_TIME:
            return result

        pages = crawl_with_depth(url, depth=2)
        texts = extract_best_text(pages)
        best_text, score = select_best_text(texts)

        combined = best_text.lower() if score > 0 else soup.get_text(" ", strip=True).lower()

        result["salary"] = extract_value(combined, ["₹", "salary", "pay"])
        result["qualification"] = extract_value(combined, ["qualification", "education", "degree", "iti"])
        result["age_limit"] = extract_age(combined)
        result["last_date"] = extract_date(combined)
        result["vacancy"] = extract_vacancy(combined)

    except:
        pass

    return result

# ==============================
def extract_value(text, keys):
    for k in keys:
        if k in text:
            i = text.index(k)
            return " ".join(text[i:i+120].split()[:12])
    return ""

def extract_date(text):
    d = re.findall(r"\d{1,2}/\d{1,2}/\d{4}", text)
    return d[0] if d else ""

def extract_age(text):
    a = re.findall(r"\d{2}\s?-\s?\d{2}", text)
    return a[0] if a else ""

def extract_vacancy(text):
    v = re.findall(r"vacanc(?:y|ies)\s*[:\-]?\s*(\d{1,5})", text)
    return v[0] if v else ""

# ==============================
def autopilot_run():
    log("=== 🚀 Autopilot Engine Started (SAFE MODE) ===")

    jobs = load_jobs()[:MAX_JOBS_PER_RUN]
    accepted = []

    for job in jobs:
        log(f"🔍 {job.get('title')}")

        data = extract_details_from_page(job.get("apply_link"))
        for k in ["salary", "qualification", "age_limit", "vacancy", "last_date"]:
            if not job.get(k) and data.get(k):
                job[k] = data[k]

        job = evaluate_job(job, source=data.get("_source", "HTML"))

        if job["accepted"]:
            accepted.append(job)
            log(f"✅ ACCEPTED {job['final_confidence']}")
        else:
            log(f"❌ REJECTED {job['final_confidence']}")

    final = optimize_jobs(accepted)
    save_jobs(final)

    log("=== ✅ Autopilot Engine Completed (A4.2 CONFIRMED) ===")

# ==============================
if __name__ == "__main__":
    autopilot_run()

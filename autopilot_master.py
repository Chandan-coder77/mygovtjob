import os
import json
import time
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 🔥 Stage-A2
from pdf_reader import extract_from_pdf, find_pdf_links

# 🔥 Stage-A3
from navigator_a3 import (
    crawl_with_depth,
    extract_best_text,
    select_best_text
)

# 🔥 Stage-A4
from confidence_engine import evaluate_job, CONFIDENCE_THRESHOLD

# 🔥 Stage-A4.2 Global Optimizer (NEW)
from global_optimizer import optimize_jobs

# ==============================
# CONFIG
# ==============================
JOBS_FILE = "jobs.json"
LOG_FILE = "autopilot_log.txt"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

CRAWLED_CACHE = set()   # 🔥 A4.1 cache

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
# 🔍 CORE EXTRACTOR (A4.1 OPTIMIZED)
# ==============================
def extract_details_from_page(url):
    result = {
        "salary": "",
        "qualification": "",
        "age_limit": "",
        "vacancy": "",
        "last_date": "",
        "_source": "HTML"
    }

    # 🔥 CACHE CHECK
    if url in CRAWLED_CACHE:
        log("⚡ Skipped (cached URL)")
        return result

    CRAWLED_CACHE.add(url)

    try:
        response = requests.get(url, headers=HEADERS, timeout=25)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # ==============================
        # PDF PRIORITY
        # ==============================
        pdf_links = find_pdf_links(html)
        if pdf_links:
            pdf_url = pdf_links[0]
            log(f"📄 PDF detected → {pdf_url}")

            pdf_data = extract_from_pdf(pdf_url)
            if pdf_data:
                pdf_data["_source"] = "PDF"

                temp_job = evaluate_job(pdf_data, source="PDF")
                log(f"🧠 confidence={temp_job['final_confidence']} | source=PDF")

                if temp_job["final_confidence"] >= CONFIDENCE_THRESHOLD:
                    log("⚡ Early STOP (PDF high confidence)")
                    return pdf_data
                else:
                    log("↩ PDF low confidence, fallback to HTML")

        # ==============================
        # MULTI PAGE CRAWL
        # ==============================
        log("🔁 Stage-A3 crawling pages")
        pages = crawl_with_depth(url, depth=2)

        texts = extract_best_text(pages)
        best_text, score = select_best_text(texts)

        if score > 0:
            combined_text = best_text.lower()
            result["_source"] = "HTML"
        else:
            combined_text = soup.get_text(" ", strip=True).lower()

        # ==============================
        # EXTRACTION
        # ==============================
        result["salary"] = extract_value(
            combined_text, ["₹", "salary", "pay scale", "pay level"]
        )

        result["qualification"] = extract_value(
            combined_text,
            ["qualification", "education", "10th", "12th",
             "iti", "diploma", "graduate", "degree"]
        )

        result["age_limit"] = extract_age(combined_text)
        result["last_date"] = extract_date(combined_text)
        result["vacancy"] = extract_vacancy(combined_text)

    except Exception as e:
        log(f"[ERROR] {url} -> {e}")

    return result


# ==============================
# Helpers
# ==============================
def extract_value(text, keywords):
    for k in keywords:
        if k in text:
            i = text.index(k)
            return " ".join(text[i:i+120].split()[:12])
    return ""


def extract_date(text):
    d = re.findall(r"\b\d{1,2}/\d{1,2}/\d{4}\b", text)
    return d[0] if d else ""


def extract_age(text):
    a = re.findall(r"\b\d{2}\s?-\s?\d{2}\b", text)
    return a[0].replace(" ", "") if a else ""


def extract_vacancy(text):
    v = re.findall(r"vacanc(?:y|ies)\s*[:\-]?\s*(\d{1,5})", text)
    if v:
        return v[0]
    nums = re.findall(r"\b\d{2,5}\b", text)
    return nums[0] if nums else ""


# ==============================
# 🚀 AUTOPILOT RUNNER (A4.1 + A4.2)
# ==============================
def autopilot_run():
    log("=== 🚀 Autopilot Engine Started (A4.1 + Global Optimizer) ===")

    jobs = load_jobs()
    collected_jobs = []

    for job in jobs:
        log(f"🔍 Scanning → {job.get('title')}")

        data = extract_details_from_page(job.get("apply_link"))

        # merge blanks
        for k in ["salary", "qualification", "age_limit", "vacancy", "last_date"]:
            if not job.get(k) and data.get(k):
                job[k] = data[k]

        source = data.get("_source", "HTML")
        job = evaluate_job(job, source=source)

        if job["accepted"]:
            log(f"✅ ACCEPTED | confidence={job['final_confidence']} | source={source}")
            collected_jobs.append(job)
        else:
            log(f"❌ REJECTED | confidence={job['final_confidence']}")

        time.sleep(1.5)

    # 🔥 GLOBAL OPTIMIZATION (A4.2)
    final_jobs = optimize_jobs(collected_jobs)

    save_jobs(final_jobs)
    log("=== ✅ Autopilot Engine Completed (A4.1 + A4.2) ===")


if __name__ == "__main__":
    autopilot_run()

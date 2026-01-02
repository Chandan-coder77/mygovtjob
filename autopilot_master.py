import os
import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ==============================
# 🔥 Stage-A1 Full Autopilot Master Engine
# ==============================

JOBS_FILE = "jobs.json"
LOG_FILE = "autopilot_log.txt"

# ==============================
# Utility Functions
# ==============================

def log(msg):
    print(msg)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")


def load_jobs():
    if not os.path.exists(JOBS_FILE):
        return []
    try:
        with open(JOBS_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_jobs(data):
    with open(JOBS_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ==============================
# 🔍 Smart Field Extractor V1 (Basic)
# ==============================
def extract_details_from_page(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(url, headers=headers, timeout=15).text
        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text(" ", strip=True).lower()

        salary = extract_value(text, ["salary", "pay", "₹"])
        qualification = extract_value(text, ["qualification", "education", "degree", "10th", "12th", "graduation", "diploma"])
        age = extract_value(text, ["age", "years", "upper age"])
        last_date = extract_date(text)
        vacancy = extract_numbers(text)

        return {
            "salary": salary,
            "qualification": qualification,
            "age_limit": age,
            "vacancy": vacancy,
            "last_date": last_date
        }

    except Exception as e:
        log(f"[Error scraping details] {url} -> {e}")
        return {}


def extract_value(text, keywords):
    for key in keywords:
        if key in text:
            part = text[text.index(key):text.index(key) + 70]
            return " ".join(part.split()[:7])
    return ""


def extract_date(text):
    import re
    dates = re.findall(r"\d{1,2}/\d{1,2}/\d{4}", text)
    return dates[0] if dates else ""


def extract_numbers(text):
    import re
    nums = re.findall(r"\d{2,5}", text)
    return nums[0] if nums else ""


# ==============================
# 🚀 Autopilot Engine
# ==============================
def autopilot_run():
    log("=== Autopilot Engine Started ===")

    jobs = load_jobs()
    updated_jobs = []

    for job in jobs:
        url = job.get("apply_link")
        log(f"Scanning: {job.get('title')}")

        data = extract_details_from_page(url)

        # intelligent update logic
        for key in ["salary", "qualification", "age_limit", "vacancy", "last_date"]:
            if (not job.get(key)) or len(str(job.get(key))) < 2:
                if data.get(key):
                    job[key] = data[key]

        updated_jobs.append(job)
        time.sleep(2)  # prevent blocking

    save_jobs(updated_jobs)
    log("=== Autopilot Engine Complete ===")


# ==============================
# Run Directly
# ==============================
if __name__ == "__main__":
    autopilot_run()

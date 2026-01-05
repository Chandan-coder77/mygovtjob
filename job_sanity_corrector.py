# ==============================
# 🧠 STAGE-A5.3
# JOB SANITY + PDF INTELLIGENCE ENGINE
# ==============================

import json
import os
import re
from datetime import datetime

INPUT_FILE = "jobs.json"
OUTPUT_FILE = "jobs.json"

CURRENT_YEAR = datetime.now().year

# ------------------------------
# PDF CLASSIFICATION
# ------------------------------
RECRUITMENT_PDF_HINTS = [
    "cen", "employment notice", "advertisement",
    "recruitment", "notification", "vacancy"
]

REJECT_PDF_HINTS = [
    "panel", "result", "cutoff", "cut-off",
    "merit", "zone", "allocation",
    "faq", "instruction", "answer key",
    "selection list"
]

# ------------------------------
# TITLE REJECTION KEYWORDS
# ------------------------------
REJECT_TITLE_KEYWORDS = [
    "panel", "result", "cutoff", "cut-off",
    "merit list", "zone allotment",
    "faq", "answer key", "instruction",
    "selection list"
]

# ------------------------------
def is_valid_date(date_str):
    if not date_str:
        return False

    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", date_str)
    if not m:
        return False

    d, mth, y = map(int, m.groups())

    if y < CURRENT_YEAR or y > CURRENT_YEAR + 3:
        return False
    if mth < 1 or mth > 12:
        return False
    if d < 1 or d > 31:
        return False

    return True

# ------------------------------
def classify_pdf(title, link):
    t = title.lower()
    l = link.lower()

    for bad in REJECT_PDF_HINTS:
        if bad in t or bad in l:
            return "REJECT"

    for good in RECRUITMENT_PDF_HINTS:
        if good in t or good in l:
            return "RECRUITMENT"

    return "UNKNOWN"

# ------------------------------
def clean_vacancy(v):
    if not v:
        return ""

    if v.isdigit():
        iv = int(v)
        if 10 <= iv <= 100000:
            return v
        else:
            return ""

    return ""

# ------------------------------
def sanitize_job(job):
    title = job.get("title", "").lower()
    link = job.get("apply_link", "").lower()

    # ❌ Reject by title intent
    for bad in REJECT_TITLE_KEYWORDS:
        if bad in title:
            return None

    # 📄 PDF logic
    if link.endswith(".pdf"):
        pdf_type = classify_pdf(title, link)
        if pdf_type != "RECRUITMENT":
            return None

    # 📅 Date sanity
    if not is_valid_date(job.get("last_date", "")):
        job["last_date"] = ""

    # 🔢 Vacancy sanity
    job["vacancy"] = clean_vacancy(job.get("vacancy", ""))

    job["sanity_checked"] = True
    job["sanity_checked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return job

# ------------------------------
def run_sanity_engine():
    if not os.path.exists(INPUT_FILE):
        print("❌ jobs.json not found")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    cleaned = []
    rejected = 0

    for job in jobs:
        fixed = sanitize_job(job)
        if fixed:
            cleaned.append(fixed)
        else:
            rejected += 1

    # 🛡 FAILSAFE: never empty output
    if not cleaned and jobs:
        cleaned = jobs[:3]
        print("⚠️ FAILSAFE ACTIVATED: minimal jobs retained")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)

    print("✅ STAGE-A5.3 COMPLETE")
    print(f"📌 Final Jobs : {len(cleaned)}")
    print(f"🗑 Rejected   : {rejected}")
    print("🧠 Sanity + PDF Intelligence Applied")

# ------------------------------
if __name__ == "__main__":
    run_sanity_engine()

# ==============================
# 🧠 STAGE-A5.2.2
# JOB INTENT INTELLIGENCE FILTER
# ==============================

import json
import re
import os
from datetime import datetime

INPUT_FILE = "jobs.json"
OUTPUT_FILE = "jobs.json"

# ------------------------------
# KEYWORDS
# ------------------------------
JOB_KEYWORDS = [
    "recruitment", "vacancy", "vacancies", "posts", "hiring",
    "assistant", "officer", "engineer", "clerk", "constable",
    "manager", "technician", "apprentice", "trainee",
    "group a", "group b", "group c"
]

REJECT_KEYWORDS = [
    "exam", "test", "cet", "cuet", "jee", "neet",
    "admission", "syllabus", "answer key", "result",
    "cutoff", "cut-off", "merit list",
    "notification status", "status",
    "apply online", "apply here"
]

PDF_JOB_HINTS = ["cen", "advertisement", "employment notice"]

# ------------------------------
def is_valid_job(job):
    title = job.get("title", "").lower()
    link = job.get("apply_link", "").lower()

    # ❌ Reject obvious non-jobs
    for bad in REJECT_KEYWORDS:
        if bad in title:
            return False

    # ❌ Reject exams / admissions
    if re.search(r"\b(cet|cuet|exam|admission)\b", title):
        return False

    # ❌ Reject empty / generic titles
    if len(title.split()) <= 2:
        return False

    # ✅ Accept PDF recruitment notices
    if link.endswith(".pdf"):
        if any(h in title for h in PDF_JOB_HINTS):
            return True

    # ✅ Accept if job keywords present
    if any(k in title for k in JOB_KEYWORDS):
        return True

    # ✅ Accept if vacancy number looks real (not year)
    v = job.get("vacancy", "")
    if v.isdigit():
        if int(v) > 10 and int(v) < 100000:
            return True

    return False

# ------------------------------
def normalize_job(job):
    # Fix year mistaken as vacancy
    v = job.get("vacancy", "")
    if v.isdigit() and len(v) == 4:
        job["vacancy"] = ""

    # Fix impossible dates
    d = job.get("last_date", "")
    if not re.match(r"\d{2}/\d{2}/\d{4}", d):
        job["last_date"] = ""

    return job

# ------------------------------
def run_filter():
    if not os.path.exists(INPUT_FILE):
        print("❌ jobs.json not found")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    filtered = []
    rejected = 0

    for job in data:
        job = normalize_job(job)

        if is_valid_job(job):
            job["intent_status"] = "JOB_CONFIRMED"
            filtered.append(job)
        else:
            rejected += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=4, ensure_ascii=False)

    print("✅ STAGE-A5.2.2 COMPLETE")
    print(f"📌 Accepted Jobs : {len(filtered)}")
    print(f"🗑 Rejected Items: {rejected}")
    print("🧠 Job Intent Intelligence Applied")

# ------------------------------
if __name__ == "__main__":
    run_filter()

# ==========================================================
# 🧠 STAGE-A5.2.2 (ADVANCED)
# JOB INTENT INTELLIGENCE FILTER – PRODUCTION VERSION
# ==========================================================

import json
import re
import os
from datetime import datetime
from urllib.parse import urlparse

INPUT_FILE = "jobs.json"
OUTPUT_FILE = "jobs.json"

# ----------------------------------------------------------
# TRUST & CONTEXT
# ----------------------------------------------------------
TRUSTED_DOMAINS = [
    ".gov.in",
    ".nic.in",
    "freejobalert.com",
    "rrb",
    "opsc",
    "ossc",
    "osssc"
]

# ----------------------------------------------------------
# JOB SIGNAL KEYWORDS
# ----------------------------------------------------------
JOB_KEYWORDS = [
    "recruitment", "vacancy", "vacancies", "posts",
    "assistant", "officer", "engineer", "clerk",
    "constable", "manager", "technician",
    "apprentice", "trainee", "foreman",
    "group a", "group b", "group c",
    "junior", "senior", "grade"
]

# ----------------------------------------------------------
# HARD REJECT KEYWORDS (NON-JOBS)
# ----------------------------------------------------------
REJECT_KEYWORDS = [
    "exam", "test", "cet", "cuet", "jee", "neet",
    "admission", "syllabus", "answer key",
    "result", "cutoff", "cut-off",
    "merit list", "hall ticket",
    "notification status", "status",
    "apply online", "apply here",
    "schedule", "time table"
]

# ----------------------------------------------------------
# PDF STRONG SIGNALS
# ----------------------------------------------------------
PDF_JOB_HINTS = [
    "advertisement",
    "employment notice",
    "cen",
    "recruitment notice",
    "detailed notification"
]

# ----------------------------------------------------------
# ROLE / STRUCTURE PATTERNS
# ----------------------------------------------------------
ROLE_PATTERNS = [
    r"\b\d+\s+posts?\b",
    r"\bposts?\s+of\b",
    r"\bpay level\b",
    r"\bpay scale\b",
    r"\blevel-\d+\b",
    r"\bgrade pay\b"
]

# ==========================================================
def is_trusted_source(link: str) -> bool:
    return any(t in link for t in TRUSTED_DOMAINS)

# ==========================================================
def normalize_job(job: dict) -> dict:
    # Fix vacancy mistaken as year
    v = job.get("vacancy", "")
    if v.isdigit() and len(v) == 4:
        job["vacancy"] = ""

    # Fix impossible dates
    d = job.get("last_date", "")
    if not re.match(r"\d{2}/\d{2}/\d{4}", d):
        job["last_date"] = ""

    return job

# ==========================================================
def is_valid_job(job: dict) -> tuple:
    title = job.get("title", "").lower()
    link = job.get("apply_link", "").lower()

    # ---------- HARD REJECT ----------
    for bad in REJECT_KEYWORDS:
        if bad in title:
            return False, "HARD_REJECT"

    if len(title.split()) <= 2:
        return False, "TOO_GENERIC"

    # ---------- PDF STRONG ACCEPT ----------
    if link.endswith(".pdf"):
        return True, "PDF_RECRUITMENT"

    # ---------- ROLE PATTERN ACCEPT ----------
    for pat in ROLE_PATTERNS:
        if re.search(pat, title):
            return True, "ROLE_PATTERN"

    # ---------- KEYWORD ACCEPT ----------
    for kw in JOB_KEYWORDS:
        if kw in title:
            return True, "JOB_KEYWORD"

    # ---------- VACANCY NUMBER ACCEPT ----------
    v = job.get("vacancy", "")
    if v.isdigit():
        n = int(v)
        if 5 <= n <= 100000:
            return True, "VACANCY_COUNT"

    # ---------- TRUSTED DOMAIN SOFT ACCEPT ----------
    if is_trusted_source(link):
        return True, "TRUSTED_SOURCE_SOFT"

    return False, "NO_JOB_SIGNAL"

# ==========================================================
def confidence_score(reason: str) -> int:
    score_map = {
        "PDF_RECRUITMENT": 95,
        "ROLE_PATTERN": 85,
        "VACANCY_COUNT": 80,
        "JOB_KEYWORD": 75,
        "TRUSTED_SOURCE_SOFT": 60
    }
    return score_map.get(reason, 0)

# ==========================================================
def run_filter():
    if not os.path.exists(INPUT_FILE):
        print("❌ jobs.json not found")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    accepted = []
    rejected = 0

    for job in data:
        job = normalize_job(job)
        valid, reason = is_valid_job(job)

        if valid:
            job["intent_status"] = "JOB_CONFIRMED" if confidence_score(reason) >= 75 else "JOB_POSSIBLE"
            job["confidence_score"] = confidence_score(reason)
            job["intent_reason"] = reason
            job["intent_checked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            accepted.append(job)
        else:
            rejected += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(accepted, f, indent=4, ensure_ascii=False)

    print("✅ STAGE-A5.2.2 ADVANCED COMPLETE")
    print(f"📌 Accepted Jobs : {len(accepted)}")
    print(f"🗑 Rejected Items: {rejected}")
    print("🧠 Job Intent Intelligence (Advanced) Applied")

# ==========================================================
if __name__ == "__main__":
    run_filter()

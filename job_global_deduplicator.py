# ==========================================================
# 🧠 STAGE-A5.5
# GLOBAL JOB DEDUPLICATOR & PRIORITY MERGER
# ==========================================================

import json
import os
import re
from datetime import datetime

INPUT_FILE = "jobs.json"
OUTPUT_FILE = "jobs.json"
PDF_BUCKET_FILE = "jobs_pdf.json"

TODAY = datetime.now().date()

# -----------------------------
# UTILS
# -----------------------------
def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def clean_text(t):
    return re.sub(r"\s+", " ", (t or "")).strip().lower()

def parse_date(d):
    try:
        return datetime.strptime(d, "%d/%m/%Y").date()
    except:
        return None

def is_expired(job):
    d = parse_date(job.get("last_date", ""))
    if not d:
        return False
    return d < TODAY

# -----------------------------
# FIELD SANITY
# -----------------------------
def sanitize_vacancy(v):
    if not v or not v.isdigit():
        return ""
    if len(v) == 4:          # looks like year
        return ""
    n = int(v)
    if n < 5 or n > 500000:
        return ""
    return v

# -----------------------------
# PRIORITY SCORE
# -----------------------------
def priority_score(job):
    score = 0

    if job.get("detail_checked"):
        score += 50
    if job.get("field_sanity") == "FIXED":
        score += 20
    if job.get("vacancy"):
        score += 15
    if job.get("salary"):
        score += 10
    if job.get("last_date"):
        score += 10
    if job.get("confidence_score", 0) > 80:
        score += 10

    link = job.get("apply_link", "").lower()
    if ".pdf" in link:
        score -= 10
    if any(x in link for x in [".gov.in", ".nic.in"]):
        score += 10

    return score

# -----------------------------
# DUPLICATE KEY
# -----------------------------
def dedup_key(job):
    title = clean_text(job.get("title", ""))
    title = re.sub(r"\b(online form|recruitment|apply online|notification)\b", "", title)
    title = re.sub(r"\d{4}", "", title)  # remove year noise
    title = title.strip()

    domain = ""
    link = job.get("apply_link", "")
    if "//" in link:
        domain = link.split("//")[-1].split("/")[0]

    return f"{title[:80]}::{domain}"

# -----------------------------
# MAIN ENGINE
# -----------------------------
def run_deduplicator():
    print("🚀 STAGE-A5.5 GLOBAL DEDUPLICATOR STARTED")

    jobs = load_json(INPUT_FILE, [])
    if not jobs:
        print("❌ jobs.json empty — aborting safely")
        return

    grouped = {}
    pdf_bucket = []

    # Normalize fields
    for job in jobs:
        job["vacancy"] = sanitize_vacancy(job.get("vacancy", ""))
        key = dedup_key(job)
        grouped.setdefault(key, []).append(job)

    final_jobs = []

    for key, group in grouped.items():
        # Separate PDFs
        pdfs = [j for j in group if ".pdf" in (j.get("apply_link", "").lower())]
        non_pdfs = [j for j in group if j not in pdfs]

        if pdfs:
            for p in pdfs:
                p["bucket"] = "PDF_NOTICE"
            pdf_bucket.extend(pdfs)

        if not non_pdfs:
            continue

        # Choose best job by priority
        best = sorted(non_pdfs, key=priority_score, reverse=True)[0]

        # Drop expired jobs (except PDFs)
        if is_expired(best):
            continue

        best["deduplicated"] = True
        best["deduplicated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        final_jobs.append(best)

    # Fail-safe
    if not final_jobs:
        print("⚠️ FINAL JOBS EMPTY → FAILSAFE ACTIVATED")
        final_jobs = jobs[:10]

    save_json(OUTPUT_FILE, final_jobs)

    if pdf_bucket:
        save_json(PDF_BUCKET_FILE, pdf_bucket)

    print(f"✅ FINAL JOBS: {len(final_jobs)}")
    print(f"📄 PDF NOTICES: {len(pdf_bucket)}")
    print("🧠 STAGE-A5.5 COMPLETE — USER READY DATASET")

# -----------------------------
if __name__ == "__main__":
    run_deduplicator()

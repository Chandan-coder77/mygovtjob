# =========================================
# STAGE-A6 : JOB VALIDITY GATE (FINAL FIXED)
# RULE:
# - ACTIVE jobs only
# - Expired last_date → REMOVE
# - Very old year + no last_date → REMOVE
# =========================================

import json
import os
from datetime import datetime

INPUT_FILE = "jobs.json"
OUTPUT_FILE = "jobs.json"

CURRENT_YEAR = datetime.now().year

DATE_FORMATS = [
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y-%m-%d"
]

# -------------------------
def parse_date(date_str):
    if not date_str:
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except:
            continue
    return None

# -------------------------
def extract_year_from_title(title):
    for y in range(2000, CURRENT_YEAR + 1):
        if str(y) in title:
            return y
    return None

# -------------------------
def is_invalid_job(job):
    title = job.get("title", "")
    last_date_raw = job.get("last_date", "").strip()

    # 1️⃣ If last_date exists → check expiry
    if last_date_raw:
        parsed = parse_date(last_date_raw)
        if parsed and parsed < datetime.now().date():
            return True  # expired
        return False  # valid future date

    # 2️⃣ No last_date → check year from title
    title_year = extract_year_from_title(title)

    if title_year and title_year <= CURRENT_YEAR - 3:
        # Example: 2021 or older in 2026
        return True

    return False  # otherwise keep

# -------------------------
def run_validity_gate():
    if not os.path.exists(INPUT_FILE):
        print("❌ jobs.json not found")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    kept = []
    removed = 0

    for job in jobs:
        if is_invalid_job(job):
            removed += 1
            continue

        job["validity_checked"] = True
        job["validity_checked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        kept.append(job)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(kept, f, indent=4, ensure_ascii=False)

    print("✅ JOB VALIDITY GATE APPLIED")
    print(f"🟢 Active jobs kept : {len(kept)}")
    print(f"🔴 Invalid jobs removed : {removed}")

# -------------------------
if __name__ == "__main__":
    run_validity_gate()

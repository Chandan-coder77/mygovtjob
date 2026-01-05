# ==========================================================
# 🔷 STAGE-A5.4.3
# SMART FIELD SANITY v2
# Cleans impossible / misleading job fields
# ==========================================================

import json
import re
from datetime import datetime

INPUT_FILE = "jobs.json"
OUTPUT_FILE = "jobs.json"

CURRENT_YEAR = datetime.now().year
MIN_YEAR = CURRENT_YEAR - 1
MAX_YEAR = CURRENT_YEAR + 2

# ----------------------------------------------------------
# UTIL HELPERS
# ----------------------------------------------------------
def is_year(value):
    try:
        v = int(value)
        return 2000 <= v <= 2100
    except:
        return False

def is_valid_date(d):
    try:
        day, month, year = map(int, d.split("/"))
        if year < CURRENT_YEAR:
            return False
        datetime(year, month, day)
        return True
    except:
        return False

def clean_salary(s):
    if not s:
        return ""
    nums = re.findall(r"\d+", s.replace(",", ""))
    if not nums:
        return ""
    val = int(nums[0])
    if 5000 <= val <= 300000:
        return f"₹{val}"
    return ""

def clean_age(a):
    if not a:
        return ""
    m = re.findall(r"\d+", a)
    if len(m) >= 2:
        lo, hi = int(m[0]), int(m[1])
        if 18 <= lo < hi <= 60:
            return f"{lo}-{hi}"
    return ""

def clean_vacancy(v):
    if not v:
        return ""
    if v.isdigit():
        iv = int(v)
        # ❌ year mistaken as vacancy
        if 2000 <= iv <= 2100:
            return ""
        # ✅ realistic vacancy range
        if 1 <= iv <= 100000:
            return str(iv)
    return ""

# ----------------------------------------------------------
# MAIN SANITY ENGINE
# ----------------------------------------------------------
def run_sanity():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            jobs = json.load(f)
    except:
        print("❌ jobs.json not readable")
        return

    cleaned = []
    fixed_count = 0

    for job in jobs:
        changed = False

        # ---- Vacancy fix
        new_v = clean_vacancy(job.get("vacancy", ""))
        if new_v != job.get("vacancy", ""):
            job["vacancy"] = new_v
            changed = True

        # ---- Date fix
        d = job.get("last_date", "")
        if d and not is_valid_date(d):
            job["last_date"] = ""
            changed = True

        # ---- Salary fix
        new_s = clean_salary(job.get("salary", ""))
        if new_s != job.get("salary", ""):
            job["salary"] = new_s
            changed = True

        # ---- Age fix
        new_a = clean_age(job.get("age_limit", ""))
        if new_a != job.get("age_limit", ""):
            job["age_limit"] = new_a
            changed = True

        if changed:
            fixed_count += 1
            job["field_sanity"] = "FIXED"
            job["field_sanity_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cleaned.append(job)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)

    print("✅ STAGE-A5.4.3 COMPLETE")
    print(f"🛠 Jobs fixed: {fixed_count}")
    print(f"📦 Total jobs: {len(cleaned)}")
    print("🧠 Smart Field Sanity v2 applied")

# ----------------------------------------------------------
if __name__ == "__main__":
    run_sanity()

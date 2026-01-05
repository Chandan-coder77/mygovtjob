# ==============================
# Stage-A6.1 : Job Validity Gate
# ==============================
# Removes:
# - Click here / Apply link pages
# - Portal homepages
# - Recruitment agencies
# - Old archive notifications
# - Non-job informational pages
#
# Keeps only REAL recruitment jobs
# ==============================

import json
import re
from datetime import datetime

INPUT_FILE = "jobs.json"
OUTPUT_FILE = "jobs.json"   # overwrite safely

CURRENT_YEAR = datetime.now().year

# ------------------------------
# Hard reject keywords (TITLE)
# ------------------------------
REJECT_TITLE_KEYWORDS = [
    "click here",
    "apply here",
    "homepage",
    "recruitment board",
    "recruitment agency",
    "public disclosure",
    "list of",
    "portal",
    "dashboard",
    "home page",
    "login",
    "registration"
]

# ------------------------------
# Hard reject domains
# ------------------------------
REJECT_DOMAINS = [
    "rrbapply.gov.in",
    "recruitmentrrb.in",
    "ncs.gov.in",
    "emigrate.gov.in"
]

# ------------------------------
# Valid job signal keywords
# ------------------------------
JOB_SIGNAL_KEYWORDS = [
    "recruitment",
    "vacancy",
    "online form",
    "apply online",
    "posts",
    "notification",
    "exam",
    "constable",
    "officer",
    "assistant",
    "engineer",
    "teacher",
    "apprentice"
]

# ------------------------------
# Utility functions
# ------------------------------
def contains_any(text, keywords):
    text = text.lower()
    return any(k in text for k in keywords)

def extract_years(text):
    return re.findall(r"(20\d{2})", text)

def is_old_year(years):
    for y in years:
        if int(y) < CURRENT_YEAR:
            return True
    return False

def valid_job(job):
    title = (job.get("title") or "").lower()
    link = (job.get("apply_link") or "").lower()

    # 1️⃣ Reject obvious junk titles
    if contains_any(title, REJECT_TITLE_KEYWORDS):
        return False

    # 2️⃣ Reject known portal / agency domains
    for d in REJECT_DOMAINS:
        if d in link:
            return False

    # 3️⃣ Reject if NO job signal present
    combined_text = title + " " + link
    if not contains_any(combined_text, JOB_SIGNAL_KEYWORDS):
        return False

    # 4️⃣ Reject OLD archive years
    years = extract_years(title + " " + link)
    if years and is_old_year(years):
        return False

    return True

# ------------------------------
# Main execution
# ------------------------------
def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            jobs = json.load(f)
    except Exception as e:
        print("❌ Failed to load jobs.json:", e)
        return

    cleaned = []
    removed = 0

    for job in jobs:
        if valid_job(job):
            job["validity_checked"] = True
            job["validity_checked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cleaned.append(job)
        else:
            removed += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)

    print("✅ A6.1 Job Validity Gate Completed")
    print(f"🟢 Kept jobs   : {len(cleaned)}")
    print(f"🔴 Removed    : {removed}")

if __name__ == "__main__":
    main()

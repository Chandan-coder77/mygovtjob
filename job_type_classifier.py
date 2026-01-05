# ==========================================
# 🧠 STAGE-A6.1
# JOB TYPE & NATURE CLASSIFIER
# ==========================================

import json
import os
import re
from datetime import datetime

# =========================
# FILE CONFIG
# =========================
INPUT_FILE = "jobs.json"

OUT_ACTIVE = "jobs_active.json"
OUT_ARCHIVED = "jobs_archived.json"
OUT_PORTAL = "jobs_portal.json"
OUT_BLOG = "jobs_blog.json"
OUT_REJECTED = "jobs_rejected.json"

CURRENT_YEAR = datetime.now().year

# =========================
# SIGNAL DEFINITIONS
# =========================

PORTAL_KEYWORDS = [
    "click here", "apply here", "login",
    "portal", "dashboard", "registration"
]

PORTAL_DOMAINS = [
    "rrbapply.gov.in",
    "recruitmentrrb.in"
]

BLOG_DOMAINS = [
    "odishajobs.in",
    "blogspot",
    "wordpress"
]

JOB_KEYWORDS = [
    "recruitment", "vacancy", "vacancies",
    "posts", "appointment", "online form",
    "offline form"
]

REJECT_KEYWORDS = [
    "faq", "corrigendum", "panel",
    "result", "answer key", "cutoff",
    "merit list", "syllabus", "exam"
]

# =========================
# UTILS
# =========================

def load_jobs():
    if not os.path.exists(INPUT_FILE):
        print("❌ jobs.json not found")
        return []
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def clean(text):
    return (text or "").lower().strip()

def extract_year(text):
    years = re.findall(r"(20\d{2})", text)
    return [int(y) for y in years]

def is_expired(last_date):
    try:
        d = datetime.strptime(last_date, "%d/%m/%Y")
        return d < datetime.now()
    except:
        return False

# =========================
# CLASSIFICATION ENGINE
# =========================

def classify(job):
    title = clean(job.get("title"))
    link = clean(job.get("apply_link", ""))
    last_date = job.get("last_date", "")

    # ❌ HARD REJECT
    if any(bad in title for bad in REJECT_KEYWORDS):
        return "REJECTED"

    # 🌐 PORTAL ONLY
    if any(k in title for k in PORTAL_KEYWORDS):
        return "PORTAL"
    if any(d in link for d in PORTAL_DOMAINS):
        return "PORTAL"

    # 📰 BLOG / REPOST
    if any(b in link for b in BLOG_DOMAINS):
        return "BLOG"

    # 📦 ARCHIVED (YEAR BASED)
    years = extract_year(title)
    if years and max(years) < CURRENT_YEAR - 1:
        return "ARCHIVED"

    # 📦 ARCHIVED (DATE BASED)
    if last_date and is_expired(last_date):
        return "ARCHIVED"

    # ✅ ACTIVE JOB
    signals = 0
    if any(k in title for k in JOB_KEYWORDS):
        signals += 1
    if job.get("vacancy"):
        signals += 1
    if job.get("salary"):
        signals += 1
    if job.get("age_limit"):
        signals += 1

    if signals >= 2:
        return "ACTIVE"

    # ❌ DEFAULT
    return "REJECTED"

# =========================
# MAIN RUNNER
# =========================

def run():
    jobs = load_jobs()

    active = []
    archived = []
    portal = []
    blog = []
    rejected = []

    for job in jobs:
        category = classify(job)
        job["job_type"] = category
        job["classified_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if category == "ACTIVE":
            active.append(job)
        elif category == "ARCHIVED":
            archived.append(job)
        elif category == "PORTAL":
            portal.append(job)
        elif category == "BLOG":
            blog.append(job)
        else:
            rejected.append(job)

    save(OUT_ACTIVE, active)
    save(OUT_ARCHIVED, archived)
    save(OUT_PORTAL, portal)
    save(OUT_BLOG, blog)
    save(OUT_REJECTED, rejected)

    print("✅ STAGE-A6.1 COMPLETE")
    print(f"🟢 Active Jobs   : {len(active)}")
    print(f"📦 Archived Jobs : {len(archived)}")
    print(f"🌐 Portals       : {len(portal)}")
    print(f"📰 Blogs         : {len(blog)}")
    print(f"❌ Rejected      : {len(rejected)}")

# =========================
if __name__ == "__main__":
    run()

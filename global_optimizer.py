# ==============================
# 🌍 Stage-A4.2 Global Optimizer
# ==============================

import re
from datetime import datetime

YEAR_PATTERN = re.compile(r"^20\d{2}$")


# ------------------------------
# Utility
# ------------------------------
def is_year(value):
    if not value:
        return False
    return bool(YEAR_PATTERN.match(str(value).strip()))


def normalize_title(title):
    return re.sub(r"\s+", " ", title.lower()).strip()


# ------------------------------
# 1️⃣ Year vs Vacancy Fix
# ------------------------------
def fix_year_vacancy(job):
    vacancy = job.get("vacancy", "")
    if is_year(vacancy):
        job["vacancy"] = ""
        job["year_detected"] = vacancy
        job["vacancy_fixed"] = True
    else:
        job["vacancy_fixed"] = False
    return job


# ------------------------------
# 2️⃣ Confidence History
# ------------------------------
def update_confidence_history(job):
    history = job.get("confidence_history", [])
    history.append({
        "time": datetime.now().isoformat(),
        "confidence": job.get("final_confidence", 0)
    })
    job["confidence_history"] = history
    return job


# ------------------------------
# 3️⃣ Duplicate Job Merge
# ------------------------------
def merge_duplicates(jobs):
    merged = {}
    for job in jobs:
        key = (
            normalize_title(job.get("title", "")),
            job.get("apply_link", "")
        )

        if key not in merged:
            merged[key] = job
        else:
            # keep higher confidence
            old = merged[key]
            if job.get("final_confidence", 0) > old.get("final_confidence", 0):
                merged[key] = job

    return list(merged.values())


# ------------------------------
# 4️⃣ URL Cache Filter
# ------------------------------
def apply_url_cache(jobs):
    seen = set()
    filtered = []

    for job in jobs:
        url = job.get("apply_link")
        if url and url not in seen:
            seen.add(url)
            filtered.append(job)

    return filtered


# ------------------------------
# 🔥 MAIN OPTIMIZER
# ------------------------------
def optimize_jobs(jobs):
    optimized = []

    for job in jobs:
        job = fix_year_vacancy(job)
        job = update_confidence_history(job)
        optimized.append(job)

    optimized = merge_duplicates(optimized)
    optimized = apply_url_cache(optimized)

    return optimized

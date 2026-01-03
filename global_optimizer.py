# ==============================
# 🌍 Stage-A4.2 Global Data Intelligence Layer (FINAL)
# ==============================

import re
import hashlib
from datetime import datetime
from confidence_engine import CONFIDENCE_THRESHOLD

YEAR_PATTERN = re.compile(r"^20\d{2}$")

# ------------------------------
# Utility
# ------------------------------
def normalize(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\(.*?\)|\[.*?\]", "", text)  # remove brackets
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def is_year(value):
    if not value:
        return False
    return bool(YEAR_PATTERN.match(str(value).strip()))


def job_fingerprint(job):
    """
    Strong duplicate identifier
    """
    base = normalize(job.get("title", "")) + "|" + normalize(job.get("apply_link", ""))
    return hashlib.md5(base.encode()).hexdigest()


# ------------------------------
# 1️⃣ Year vs Vacancy Global Fix
# ------------------------------
def fix_year_vacancy(job):
    vacancy = str(job.get("vacancy", "")).strip()

    if is_year(vacancy):
        job["vacancy"] = ""
        job["vacancy_fixed"] = True
        job["vacancy_fix_reason"] = "year_detected"
    else:
        job["vacancy_fixed"] = False

    return job


# ------------------------------
# 2️⃣ Confidence History Memory
# ------------------------------
def update_confidence_history(job):
    history = job.get("confidence_history", [])

    history.append({
        "time": datetime.now().isoformat(),
        "confidence": job.get("final_confidence", 0),
        "source": job.get("confidence_source", "HTML")
    })

    job["confidence_history"] = history
    return job


# ------------------------------
# 3️⃣ Smart Field Merge
# ------------------------------
def merge_job_fields(old, new):
    """
    Field-wise merge (best value wins)
    """
    for field in ["salary", "qualification", "age_limit", "vacancy", "last_date"]:
        if not old.get(field) and new.get(field):
            old[field] = new[field]

    # keep highest confidence
    old["final_confidence"] = max(
        old.get("final_confidence", 0),
        new.get("final_confidence", 0)
    )

    return old


# ------------------------------
# 4️⃣ Duplicate Job Merge (Smart)
# ------------------------------
def merge_duplicates(jobs):
    registry = {}

    for job in jobs:
        fid = job_fingerprint(job)

        if fid not in registry:
            registry[fid] = job
        else:
            registry[fid] = merge_job_fields(registry[fid], job)

    return list(registry.values())


# ------------------------------
# 5️⃣ URL Cache Filter
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
# 🔥 MAIN OPTIMIZER (Stage-A4.2)
# ------------------------------
def optimize_jobs(jobs):
    """
    Input: accepted jobs from A4.1
    Output: clean, deduplicated, corrected jobs.json
    """

    optimized = []

    for job in jobs:
        job = fix_year_vacancy(job)
        job = update_confidence_history(job)
        optimized.append(job)

    optimized = merge_duplicates(optimized)
    optimized = apply_url_cache(optimized)

    # final confidence filter
    final_jobs = []
    for job in optimized:
        if job.get("final_confidence", 0) >= CONFIDENCE_THRESHOLD:
            job["optimized_at"] = datetime.now().isoformat()
            final_jobs.append(job)

    return final_jobs

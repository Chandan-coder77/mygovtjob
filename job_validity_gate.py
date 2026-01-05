import json
import os
from datetime import datetime

JOBS_FILE = "jobs.json"

def load_jobs():
    if not os.path.exists(JOBS_FILE):
        return []
    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_jobs(jobs):
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=4)

def classify_job_visibility(job):
    """
    IMPORTANT RULE:
    ❌ Never delete
    ❌ Never hide
    ✅ Only TAG + NOTE
    """

    title = (job.get("title") or "").lower()
    link = (job.get("apply_link") or "").lower()

    visibility = "SHOW"          # default: always show
    nature = "ACTIVE_JOB"        # default nature
    note = ""

    # -------- Portal / Info pages --------
    if any(x in title for x in [
        "click here",
        "apply here",
        "official website",
        "portal",
        "home page",
        "act, rules",
        "notification"
    ]):
        nature = "PORTAL_PAGE"
        note = "Official portal / information page"

    # -------- Very old year detection (only label) --------
    if any(y in title for y in ["2018", "2019", "2020", "2021"]):
        nature = "ARCHIVED_JOB"
        note = "Old recruitment reference (archived)"

    # -------- Missing critical data (still show) --------
    if not job.get("last_date"):
        note = note or "Last date not mentioned yet"

    if not job.get("vacancy"):
        note = note or "Vacancy details not mentioned"

    # -------- Apply link sanity --------
    if link.endswith(".pdf"):
        nature = nature if nature != "ACTIVE_JOB" else "PDF_NOTIFICATION"
        note = note or "Details available in PDF"

    # -------- Attach fields --------
    job["job_visibility"] = visibility              # ALWAYS SHOW
    job["job_nature"] = nature
    job["validity_checked"] = True
    job["validity_checked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if note:
        job["job_note"] = note

    return job

def main():
    jobs = load_jobs()
    if not jobs:
        print("No jobs found for validity gate.")
        return

    updated_jobs = []
    for job in jobs:
        updated_jobs.append(classify_job_visibility(job))

    save_jobs(updated_jobs)
    print(f"Job Validity Gate applied safely on {len(updated_jobs)} jobs.")

if __name__ == "__main__":
    main()

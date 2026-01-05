# ============================================
# 🧠 STAGE-A5.2.1 — JOB INTELLIGENCE FILTER
# ============================================

import json, re
from datetime import datetime

INPUT_FILE = "jobs.json"
FINAL_FILE = "jobs_final.json"
REJECT_FILE = "jobs_rejected.json"
PENDING_FILE = "jobs_pending.json"

CURRENT_YEAR = datetime.now().year

# --------------------------------------------
# KEYWORD RULES
# --------------------------------------------
JOB_POSITIVE = [
    "recruitment", "online form", "vacancy",
    "apply online", "posts", "various posts",
    "cen", "employment notice"
]

JOB_NEGATIVE = [
    "notification", "latest", "upcoming",
    "exam", "cet", "entrance", "test",
    "result", "cutoff", "answer key",
    "admit card", "syllabus",
    "panel", "schedule", "timetable",
    "agm", "shareholder", "tender",
    "eoi", "expression of interest",
    "faq", "indicative", "corrigendum"
]

PDF_NEGATIVE = [
    "panel", "result", "schedule",
    "faq", "indicative", "corrigendum"
]

PDF_POSITIVE = [
    "recruitment", "cen", "vacancy", "apply"
]

# --------------------------------------------
# HELPERS
# --------------------------------------------
def text_has_any(text, words):
    text = text.lower()
    return any(w in text for w in words)

def valid_date(date_str):
    if not date_str or not isinstance(date_str, str):
        return False
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", date_str)
    if not m:
        return False
    d, mth, y = map(int, m.groups())
    if d < 1 or d > 31: return False
    if mth < 1 or mth > 12: return False
    if y < CURRENT_YEAR - 1: return False
    if y > CURRENT_YEAR + 2: return False
    return True

def confidence_score(job):
    score = 0
    title = job.get("title", "").lower()
    link = job.get("apply_link", "").lower()

    if text_has_any(title, JOB_POSITIVE): score += 25
    if job.get("vacancy"): score += 30
    if job.get("salary"): score += 15
    if valid_date(job.get("last_date")): score += 10

    if text_has_any(title, JOB_NEGATIVE): score -= 50
    if link.endswith(".pdf") and text_has_any(link, PDF_NEGATIVE): score -= 40
    if link.endswith(".pdf") and text_has_any(link, PDF_POSITIVE): score += 40

    return score

# --------------------------------------------
# MAIN PROCESS
# --------------------------------------------
def run():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    final_jobs = []
    rejected = []
    pending = []

    for job in jobs:
        title = job.get("title", "").lower()
        link = job.get("apply_link", "").lower()

        score = confidence_score(job)
        job["confidence_score"] = score

        # HARD REJECT CONDITIONS
        if text_has_any(title, JOB_NEGATIVE):
            job["reject_reason"] = "NOT_A_RECRUITMENT"
            rejected.append(job)
            continue

        if job.get("last_date") and not valid_date(job["last_date"]):
            job["reject_reason"] = "INVALID_DATE"
            rejected.append(job)
            continue

        # ACCEPT / PENDING
        if score >= 40:
            job["status"] = "FINAL_ACCEPTED"
            final_jobs.append(job)
        elif 20 <= score < 40:
            job["status"] = "PENDING_REVIEW"
            pending.append(job)
        else:
            job["reject_reason"] = "LOW_CONFIDENCE"
            rejected.append(job)

    # ----------------------------------------
    # SAVE OUTPUTS
    # ----------------------------------------
    with open(FINAL_FILE, "w", encoding="utf-8") as f:
        json.dump(final_jobs, f, indent=4, ensure_ascii=False)

    with open(REJECT_FILE, "w", encoding="utf-8") as f:
        json.dump(rejected, f, indent=4, ensure_ascii=False)

    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump(pending, f, indent=4, ensure_ascii=False)

    print("\n🧠 STAGE-A5.2.1 COMPLETE")
    print(f"✅ FINAL JOBS     : {len(final_jobs)}")
    print(f"⏳ PENDING JOBS   : {len(pending)}")
    print(f"❌ REJECTED JOBS  : {len(rejected)}\n")

# --------------------------------------------
if __name__ == "__main__":
    run()

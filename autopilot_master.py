# ==========================================================
# 🧠 AUTOPILOT MASTER
# STAGE-A5.2 (CONFIDENCE + INTENT INTEGRATION)
# ==========================================================

import json
import os
import re
import subprocess
from datetime import datetime

# =========================
# FILES
# =========================
RAW_FILE = "jobs_raw.json"          # Stage-A5.1 output
INTENT_FILE = "jobs.json"           # After job_intent_filter.py
PENDING_FILE = "jobs_pending.json"
FINAL_FILE = "jobs.json"

# =========================
# THRESHOLDS
# =========================
MIN_FINAL_CONFIDENCE = 40
FALLBACK_PROMOTION_PERCENT = 0.25   # 25% safety net

# =========================
# BLOCK KEYWORDS (HARD)
# =========================
BLOCK_KEYWORDS = [
    "result", "cutoff", "answer key", "admit card",
    "syllabus", "exam", "panel", "agm",
    "annual report", "shareholder", "dividend",
    "eoi", "expression of interest", "mou", "tender"
]

STRONG_JOB_KEYWORDS = [
    "recruitment", "online form", "vacancy",
    "posts", "appointment", "apply"
]

# =========================
# UTILS
# =========================
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

# =========================
# CONFIDENCE ENGINE
# =========================
def calculate_confidence(job):
    score = 0
    title = clean_text(job.get("title"))
    link = clean_text(job.get("apply_link"))

    # HARD BLOCK
    if any(b in title for b in BLOCK_KEYWORDS):
        return -100

    # STRONG JOB SIGNALS
    if any(k in title for k in STRONG_JOB_KEYWORDS):
        score += 25

    # PDF BOOST
    if link.endswith(".pdf"):
        score += 40

    # FIELD SIGNALS
    if job.get("vacancy"):
        score += 30
    if job.get("last_date"):
        score += 20
    if job.get("salary"):
        score += 10
    if job.get("qualification"):
        score += 10

    # GOVT DOMAIN BOOST
    if any(x in link for x in [".gov.in", ".nic.in"]):
        score += 10

    # INTENT FILTER BOOST
    if job.get("intent_status") == "JOB_CONFIRMED":
        score += 30
    elif job.get("intent_status") == "JOB_POSSIBLE":
        score += 15

    return score

# =========================
# AUTOPILOT RUN
# =========================
def run_autopilot():
    print("=== 🚀 Autopilot Engine Started (Stage-A5.2 FULL MODE) ===")

    # --------------------------------------------------
    # STEP 1: LOAD RAW JOBS
    # --------------------------------------------------
    raw_jobs = load_json(RAW_FILE, [])
    if not raw_jobs:
        print("❌ jobs_raw.json missing/empty — aborting safely")
        return

    print(f"📥 RAW jobs loaded: {len(raw_jobs)}")

    # --------------------------------------------------
    # STEP 2: WRITE RAW → jobs.json for intent filter
    # --------------------------------------------------
    save_json(INTENT_FILE, raw_jobs)

    # --------------------------------------------------
    # STEP 3: RUN JOB INTENT FILTER (A5.2.2)
    # --------------------------------------------------
    print("🧠 Running Job Intent Intelligence Filter (A5.2.2)...")
    try:
        subprocess.run(["python", "job_intent_filter.py"], check=True)
    except Exception as e:
        print(f"⚠️ Intent filter failed: {e}")

    intent_jobs = load_json(INTENT_FILE, [])
    if not intent_jobs:
        print("⚠️ Intent filter returned 0 jobs — fallback to RAW")
        intent_jobs = raw_jobs

    print(f"🧩 Jobs after intent filter: {len(intent_jobs)}")

    # --------------------------------------------------
    # STEP 4: CONFIDENCE EVALUATION
    # --------------------------------------------------
    final_jobs = []
    pending_jobs = []

    for job in intent_jobs:
        conf = calculate_confidence(job)
        job["confidence"] = conf
        job["evaluated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if conf < 0:
            job["status"] = "BLOCKED"
            continue

        if conf >= MIN_FINAL_CONFIDENCE:
            job["status"] = "FINAL"
            final_jobs.append(job)
        else:
            job["status"] = "PENDING"
            pending_jobs.append(job)

    # --------------------------------------------------
    # FAIL SAFE: NEVER ZERO FINAL JOB
    # --------------------------------------------------
    if not final_jobs and pending_jobs:
        promote_count = max(1, int(len(pending_jobs) * FALLBACK_PROMOTION_PERCENT))
        pending_jobs.sort(key=lambda x: x.get("confidence", 0), reverse=True)

        fallback = pending_jobs[:promote_count]
        for j in fallback:
            j["status"] = "FINAL_FALLBACK"
            final_jobs.append(j)

        pending_jobs = pending_jobs[promote_count:]
        print(f"⚠️ FINAL empty → promoted {len(final_jobs)} jobs from PENDING")

    # --------------------------------------------------
    # SAVE OUTPUTS
    # --------------------------------------------------
    save_json(PENDING_FILE, {
        "stage": "A5.2",
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_pending": len(pending_jobs),
        "jobs": pending_jobs
    })

    save_json(FINAL_FILE, final_jobs)

    print("✅ AUTOPILOT COMPLETE")
    print(f"📌 FINAL jobs: {len(final_jobs)}")
    print(f"🕒 PENDING jobs: {len(pending_jobs)}")
    print("🛡 Zero-job protection ACTIVE")

# =========================
if __name__ == "__main__":
    run_autopilot()

import json, os, re
from datetime import datetime

# =========================
# CONFIG
# =========================
RAW_FILE = "jobs_raw.json"        # Stage-A5.1 output
PENDING_FILE = "jobs_pending.json"
FINAL_FILE = "jobs.json"

MIN_FINAL_CONFIDENCE = 40         # Promotion threshold
FALLBACK_PROMOTION_PERCENT = 0.2  # 20% fallback if FINAL empty

BLOCK_KEYWORDS = [
    "result", "cutoff", "answer key", "admit card",
    "syllabus", "exam", "panel", "agm",
    "annual report", "shareholder", "dividend",
    "eoi", "expression of interest", "mou", "tender"
]

STRONG_JOB_KEYWORDS = [
    "recruitment", "online form", "vacancy",
    "apply", "posts", "appointment"
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
# CONFIDENCE ENGINE (A5.2)
# =========================
def calculate_confidence(job):
    score = 0
    title = clean_text(job.get("title", ""))
    link = clean_text(job.get("apply_link", ""))

    # Hard block
    if any(b in title for b in BLOCK_KEYWORDS):
        return -100

    # Strong job signals
    if any(k in title for k in STRONG_JOB_KEYWORDS):
        score += 20

    # PDF boost
    if ".pdf" in link:
        score += 40

    # Field-based scoring
    if job.get("vacancy"):
        score += 30
    if job.get("last_date"):
        score += 20
    if job.get("salary"):
        score += 10
    if job.get("qualification"):
        score += 10

    # Govt domain boost
    if any(x in link for x in [".gov.in", ".nic.in"]):
        score += 10

    return score

# =========================
# AUTOPILOT A5.2
# =========================
def run_autopilot():
    print("=== 🚀 Autopilot Engine Started (Stage-A5.2 SAFE MODE) ===")

    raw_jobs = load_json(RAW_FILE, [])
    if not raw_jobs:
        print("❌ jobs_raw.json empty or missing — aborting safely")
        return

    final_jobs = []
    pending_jobs = []

    for job in raw_jobs:
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

    # =========================
    # FAIL-SAFE: NEVER ZERO JOB
    # =========================
    if not final_jobs and pending_jobs:
        promote_count = max(1, int(len(pending_jobs) * FALLBACK_PROMOTION_PERCENT))
        pending_jobs.sort(key=lambda x: x.get("confidence", 0), reverse=True)

        fallback = pending_jobs[:promote_count]
        for j in fallback:
            j["status"] = "FINAL_FALLBACK"
            final_jobs.append(j)

        pending_jobs = pending_jobs[promote_count:]
        print(f"⚠️ FINAL empty → promoted {len(final_jobs)} from PENDING (failsafe)")

    # =========================
    # WRITE OUTPUTS
    # =========================
    save_json(PENDING_FILE, {
        "stage": "A5.2",
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_pending": len(pending_jobs),
        "jobs": pending_jobs
    })

    save_json(FINAL_FILE, final_jobs)

    print(f"✅ FINAL jobs saved: {len(final_jobs)}")
    print(f"🕒 Pending jobs saved: {len(pending_jobs)}")
    print("🧠 Stage-A5.2 COMPLETE — Zero-job protection ACTIVE")

# =========================
if __name__ == "__main__":
    run_autopilot()

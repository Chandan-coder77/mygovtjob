import json
from value_extractor import extract_values    # Extract structured values
from validator import validate_job            # Validate & fix formats safely

# ==================================================
# JSON Load / Save Helpers
# ==================================================
def load_json(file, default):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ==================================================
# Load AI Memory (SAFE)
# ==================================================
memory = load_json("ai_memory.json", {})

qualification = set(memory.get("qualification_patterns", []))
salary = set(memory.get("salary_patterns", []))
age = set(memory.get("age_patterns", []))
lastdate = set(memory.get("lastdate_patterns", []))
vacancy = set(memory.get("vacancy_patterns", []))
learn_count = memory.get("learn_count", 0)

# ==================================================
# Load Jobs
# ==================================================
jobs = load_json("jobs.json", [])

if not jobs:
    print("⚠️ No jobs found — AI Training skipped safely.")
    exit(0)

print("\n🧠 AI Trainer (SAFE MODE) Started...\n")

# ==================================================
# Core Learning Loop (NO DELETION)
# ==================================================
for job in jobs:

    if not isinstance(job, dict):
        continue

    # 🔒 ONLY READ + FIX FORMAT (no removal)
    job = extract_values(job)
    job = validate_job(job)

    # ===== Learning patterns =====
    if job.get("qualification"):
        qualification.add(str(job["qualification"]).lower())

    if job.get("salary"):
        salary.add(str(job["salary"]).lower())

    if job.get("age_limit"):
        age.add(str(job["age_limit"]))

    if job.get("vacancy"):
        vacancy.add(str(job["vacancy"]))

    if job.get("last_date"):
        lastdate.add(str(job["last_date"]))

# ==================================================
# Memory Save
# ==================================================
learn_count += 1

memory_update = {
    "qualification_patterns": sorted(qualification),
    "salary_patterns": sorted(salary),
    "age_patterns": sorted(age),
    "lastdate_patterns": sorted(lastdate),
    "vacancy_patterns": sorted(vacancy),
    "learn_count": learn_count
}

save_json("ai_memory.json", memory_update)

print("✅ AI Memory Updated Successfully!")
print(f"📈 Learn Count: {learn_count}")
print("🔐 SAFE MODE: No job deleted, no confidence filtering")
print("🚀 Pipeline Stable — Ready for next stages")

import json
from smart_cleaner import clean_job           # Clean unwanted chars
from value_extractor import extract_values    # Extract structured values
from validator import validate_job            # 🔥 Validate & Fix incorrect fields

# ================= JSON Load/Save =================
def load_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ================= Load AI Memory =================
memory = load_json("ai_memory.json")

qualification = set(memory.get("qualification_patterns", []))
salary = set(memory.get("salary_patterns", []))
age = set(memory.get("age_patterns", []))
lastdate = set(memory.get("lastdate_patterns", []))
vacancy = set(memory.get("vacancy_patterns", []))
learn_count = memory.get("learn_count", 0)

# ================= Load scraped jobs =================
jobs = load_json("jobs.json")

if not jobs:
    print("❌ No jobs found — Training Skipped.")
    exit()

print("\n🔍 AI Training Started...\n")

# ================= Core AI Engine (Extractor + Cleaner + Validator) =================
for job in jobs:

    if not isinstance(job, dict):
        continue

    job = clean_job(job)           # Clean messy text
    job = extract_values(job)      # Extract values (Age, Salary, etc.)
    job = validate_job(job)        # 🔥 Correct invalid or wrong format data

    # === Learning memory update ===
    if job.get("qualification"):
        qualification.add(job["qualification"].lower())

    if job.get("salary"):
        salary.add(str(job["salary"]).lower())

    if job.get("age_limit"):
        age.add(str(job["age_limit"]))

    if job.get("vacancy"):
        vacancy.add(str(job["vacancy"]))

    if job.get("last_date"):
        lastdate.add(str(job["last_date"]))

# =============== Memory Optimization ===============
qualification = sorted(qualification)
salary = sorted(salary)
age = sorted(age)
lastdate = sorted(lastdate)
vacancy = sorted(vacancy)
learn_count += 1

memory_update = {
    "qualification_patterns": qualification,
    "salary_patterns": salary,
    "age_patterns": age,
    "lastdate_patterns": lastdate,
    "vacancy_patterns": vacancy,
    "learn_count": learn_count
}

save_json("ai_memory.json", memory_update)

print("\n🚀 AI Memory Updated Successfully!")
print(f"📈 Learn Count: {learn_count}")
print("🧠 AI Brain V3 Active — Cleaner + Extractor + Validator Online🔥")
print("Next stage → Auto Correction & Multi-Page Scraper Upgrade 🚀")

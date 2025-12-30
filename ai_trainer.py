import json
from smart_cleaner import clean_job   # 🔥 Smart Memory Cleaner Integrated

# ---------------- JSON Load/Save ----------------
def load_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ---------------- Load AI Memory ----------------
memory = load_json("ai_memory.json")

qualification = set(memory.get("qualification_patterns", []))
salary = set(memory.get("salary_patterns", []))
age = set(memory.get("age_patterns", []))
lastdate = set(memory.get("lastdate_patterns", []))
vacancy = set(memory.get("vacancy_patterns", []))
learn_count = memory.get("learn_count", 0)

# ---------------- Load scraped jobs ----------------
jobs = load_json("jobs.json")

if not jobs:
    print("❌ No jobs found — training skipped.")
    exit()

print("\n🔍 AI Training Started...")

# ---------------- Training Engine (Auto Merge + Cleaner) ----------------
for job in jobs:

    # Convert string jobs into safe dict
    if not isinstance(job, dict):
        continue

    job = clean_job(job)  # 🔥 Main Upgrade — memory cleaned & normalized

    # Qualification learn
    if job.get("qualification") and len(job["qualification"]) < 50:
        qualification.add(job["qualification"].lower())

    # Salary Learn
    if job.get("salary"):
        salary.add(str(job["salary"]).lower())

    # Age Learn
    if job.get("age_limit"):
        age.add(str(job["age_limit"]))

    # Vacancy Learn
    if job.get("vacancy"):
        vacancy.add(str(job["vacancy"]))

    # Last Date Learn
    if job.get("last_date"):
        lastdate.add(str(job["last_date"]))

# ---------------- Memory Clean + Optimize ----------------
qualification = sorted(qualification)
salary = sorted(salary)
age = sorted(age)
lastdate = sorted(lastdate)
vacancy = sorted(vacancy)

learn_count += 1  # AI Experience Upgrade

# ---------------- Save AI Brain ----------------
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
print(f"📈 Total Learn Count: {learn_count}")
print("🧠 Smart Cleaner Active — Memory evolving automatically!")

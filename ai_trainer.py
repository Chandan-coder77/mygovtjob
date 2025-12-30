import json
from smart_cleaner import clean_job                     # 🔥 Smart Cleaner Integrated
from value_extractor import (                           # 🔥 Value Extractor V3
    extract_salary, extract_age, extract_vacancy,
    extract_last_date, extract_qualification
)

# ---------------- JSON Load & Save ----------------
def load_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ---------------- Load Existing AI Memory ----------------
memory = load_json("ai_memory.json")

qualification = set(memory.get("qualification_patterns", []))
salary        = set(memory.get("salary_patterns", []))
age           = set(memory.get("age_patterns", []))
lastdate      = set(memory.get("lastdate_patterns", []))
vacancy       = set(memory.get("vacancy_patterns", []))
learn_count   = memory.get("learn_count", 0)


# ---------------- Load Scraped JOBS Data ----------------
jobs = load_json("jobs.json")

if not jobs:
    print("❌ No jobs found — Training Skipped!")
    exit()

print("\n🔍 AI Training Started...\n")


# ---------------- Training (Auto-Merge + Smart Extract) ----------------
for job in jobs:

    if not isinstance(job, dict):
        continue

    # 1) Clean Unwanted Words
    job = clean_job(job)

    # 2) Value Extract & Normalize
    job["qualification"] = extract_qualification(job.get("qualification", ""))
    job["salary"]        = extract_salary(job.get("salary", ""))
    job["age_limit"]     = extract_age(job.get("age_limit", ""))
    job["vacancy"]       = extract_vacancy(job.get("vacancy", ""))
    job["last_date"]     = extract_last_date(job.get("last_date", ""))

    # 3) Train Memory Patterns
    if job["qualification"]: qualification.add(job["qualification"])
    if job["salary"]:        salary.add(job["salary"])
    if job["age_limit"]:     age.add(job["age_limit"])
    if job["vacancy"]:       vacancy.add(job["vacancy"])
    if job["last_date"]:     lastdate.add(job["last_date"])


# ---------------- Optimize & Update AI Brain ----------------
qualification = sorted(qualification)
salary        = sorted(salary)
age           = sorted(age)
lastdate      = sorted(lastdate)
vacancy       = sorted(vacancy)

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
print(f"📈 Total Learn Count: {learn_count}")
print("🤖 Value Extractor + Smart Cleaner Active — Auto Brain Growing!\n")

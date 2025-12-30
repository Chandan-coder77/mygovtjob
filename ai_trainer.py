import json

def load_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ---------------- AI Memory Load ----------------
memory = load_json("ai_memory.json")

qualification = set(memory.get("qualification_patterns", []))
salary = set(memory.get("salary_patterns", []))
age = set(memory.get("age_patterns", []))
lastdate = set(memory.get("lastdate_patterns", []))
vacancy = set(memory.get("vacancy_patterns", []))
learn_count = memory.get("learn_count", 0)

# ---------------- Jobs Scraped Load ----------------
jobs = load_json("jobs.json")

# If empty skip safely
if not jobs:
    print("No jobs detected — Training Skipped.")
    exit()

print("\n🔍 Training Started...")

# Smart learn from scraped patterns
for job in jobs:
    if isinstance(job, dict):

        # Qualification learning
        if "qualification" in job and len(job["qualification"]) < 50:
            qualification.add(job["qualification"].lower())

        # Salary learning
        if "salary" in job:
            salary.add(job["salary"].lower())

        # Age limit
        if "age_limit" in job:
            age.add(job["age_limit"])

        # Vacancy
        if "vacancy" in job:
            vacancy.add(str(job["vacancy"]))

        # Last date
        if "last_date" in job:
            lastdate.add(job["last_date"])

# Auto duplicate removal + sorting for clean memory
qualification = sorted(set(qualification))
salary = sorted(set(salary))
age = sorted(set(age))
lastdate = sorted(set(lastdate))
vacancy = sorted(set(vacancy))

# Auto learn count increase
learn_count += 1

# ---------------- Save Updated Memory ----------------
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

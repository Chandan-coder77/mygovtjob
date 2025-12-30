import json
import os

# ---- Load Memory ----
if not os.path.exists("ai_memory.json"):
    print("❗ ai_memory.json not found, creating new memory file...")
    memory = {
        "qualification_patterns": [],
        "salary_patterns": [],
        "age_patterns": [],
        "lastdate_patterns": [],
        "vacancy_patterns": [],
        "learn_count": 0
    }
else:
    memory = json.load(open("ai_memory.json"))

# ---- Auto-Merge / Auto-Learn Engine ----
def merge_patterns(key, new_list):
    added = 0
    for item in new_list:
        if item not in memory[key]:
            memory[key].append(item)
            added += 1
    memory["learn_count"] += added
    return added

# ---- Load scraped jobs ----
if os.path.exists("jobs.json"):
    data = json.load(open("jobs.json"))
else:
    print("⚠ jobs.json missing — scraping must run first.")
    exit()

combined_salary = []
combined_qualification = []
combined_age = []
combined_lastdate = []
combined_vacancy = []

for job in data:
    if "salary" in job and job["salary"] not in combined_salary:
        combined_salary.append(job["salary"])

    if "qualification" in job and job["qualification"] not in combined_qualification:
        combined_qualification.append(job["qualification"])

    if "age_limit" in job and job["age_limit"] not in combined_age:
        combined_age.append(job["age_limit"])

    if "last_date" in job and job["last_date"] not in combined_lastdate:
        combined_lastdate.append(job["last_date"])

    if "vacancies" in job and job["vacancies"] not in combined_vacancy:
        combined_vacancy.append(job["vacancies"])

# ----- Merge into memory -----
a = merge_patterns("salary_patterns", combined_salary)
b = merge_patterns("qualification_patterns", combined_qualification)
c = merge_patterns("age_patterns", combined_age)
d = merge_patterns("lastdate_patterns", combined_lastdate)
e = merge_patterns("vacancy_patterns", combined_vacancy)

json.dump(memory, open("ai_memory.json", "w"), indent=4)

print("\n🧠 AI Memory Updated Successfully!")
print(f"📌 New Learnings Added → Salary:{a} | Qualification:{b} | Age:{c} | Last-Date:{d} | Vacancy:{e}")
print(f"🔥 Total Learn Count: {memory['learn_count']}")

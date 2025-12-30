import json
from smart_cleaner_v2 import clean_job       # 🔥 Mode C Upgrade
from value_extractor import extract_values   # 🧠 Smart extraction engine

# JSON loader
def load_json(file):
    try:
        with open(file,"r",encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# JSON saver
def save_json(file,data):
    with open(file,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

# ---------------- LOAD MEMORY ----------------
memory = load_json("ai_memory.json")

qualification = set(memory.get("qualification_patterns",[]))
salary        = set(memory.get("salary_patterns",[]))
age           = set(memory.get("age_patterns",[]))
lastdate      = set(memory.get("lastdate_patterns",[]))
vacancy       = set(memory.get("vacancy_patterns",[]))
learn_count   = memory.get("learn_count",0)


# -------------- LOAD SCRAPED JOBS --------------
jobs = load_json("jobs.json")
if not jobs:
    print("❌ No scraped jobs — Training skipped")
    exit()

print("\n🧠 Mode-C Training Started...")

for job in jobs:
    if not isinstance(job,dict):
        continue

    job = clean_job(job)                 # 💠 Clean invalid patterns
    data = extract_values(job)           # 💠 Extract refined values

    # progressive pattern growing
    if data.get("qualification"): qualification.add(data["qualification"])
    if data.get("salary"):        salary.add(data["salary"])
    if data.get("age_limit"):     age.add(data["age_limit"])
    if data.get("last_date"):     lastdate.add(data["last_date"])
    if data.get("vacancy"):       vacancy.add(data["vacancy"])


# -------------- AUTO SORT + CLEAN MEMORY --------------
qualification = sorted({x for x in qualification if len(x)<50})
salary        = sorted({x for x in salary if "click" not in x})
age           = sorted(age)
lastdate      = sorted(lastdate)
vacancy       = sorted(vacancy)

learn_count += 1

# -------------- SAVE MEMORY --------------
updated_memory = {
    "qualification_patterns": qualification,
    "salary_patterns": salary,
    "age_patterns": age,
    "lastdate_patterns": lastdate,
    "vacancy_patterns": vacancy,
    "learn_count": learn_count
}

save_json("ai_memory.json",updated_memory)

print("🚀 AI Memory Updated Successfully!")
print(f"📈 Learn Count → {learn_count}")
print("🧠 Mode-C Activated: Smart Learn + Auto Cleanup Live")

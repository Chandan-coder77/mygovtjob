import json, re, os

MEMORY_FILE = "ai_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {
            "qualification_patterns": [],
            "salary_patterns": [],
            "age_patterns": [],
            "lastdate_patterns": [],
            "vacancy_patterns": [],
            "learn_count": 0
        }
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=4)

def learn_pattern(mem, key, value):
    value = value.strip().lower()
    if value and value not in mem[key]:
        mem[key].append(value)
        mem["learn_count"] += 1

def extract_and_learn(html):
    mem = load_memory()

    # ---- AUTO PATTERN EXTRACTION ----
    qualifications = re.findall(r"(10th|12th|graduate|b\.?a|b\.?sc|btech|mba|iti|diploma)", html, re.I)
    salaries = re.findall(r"rs\.?\s?\d+[,0-9]*", html, re.I)
    ages = re.findall(r"\d{2}\s?-\s?\d{2}", html)
    last_dates = re.findall(r"\d{1,2}\/\d{1,2}\/\d{4}", html)
    vacancies = re.findall(r"\d{2,4}", html)

    for q in qualifications: learn_pattern(mem,"qualification_patterns",q)
    for s in salaries: learn_pattern(mem,"salary_patterns",s)
    for a in ages: learn_pattern(mem,"age_patterns",a)
    for d in last_dates: learn_pattern(mem,"lastdate_patterns",d)
    for v in vacancies: learn_pattern(mem,"vacancy_patterns",v)

    save_memory(mem)
    return mem["learn_count"]

def extract_ai(html):
    learn_count = extract_and_learn(html)
    return {"ai_memory_updated": True, "learned_total": learn_count}

import json, re, shutil
from datetime import datetime

# ================= Backup System =================
def backup_memory():
    try:
        shutil.copy("ai_memory.json", "ai_memory_backup.json")
        print("💾 Backup created: ai_memory_backup.json")
    except:
        print("⚠ Backup skipped (file missing)")


# ============== Load JSON Safe ==============
def load_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


# ============== Cleaning Rules ==============
def unique_clean(items, rule=lambda x: True):
    clean = set()
    for i in items:
        s = str(i).strip().replace(" ", "").replace("_", "")
        if s and rule(s):
            clean.add(s)
    return sorted(clean)


# Pattern Validators
is_salary = lambda x: bool(re.match(r"^₹?\d{4,7}$", x.replace(",", ""))) or "lpa" in x.lower()

is_age = lambda x: bool(re.match(r"^\d{1,2}-\d{1,2}$", x)) and 15 <= int(x.split("-")[0]) <= 40

is_vac = lambda x: x.isdigit() and 1 <= int(x) <= 5000

def is_date(x):
    try:
        datetime.strptime(x, "%d/%m/%Y")
        return True
    except:
        return False


# ============== Main Cleaning Engine ==============
def clean_memory():
    data = load_json("ai_memory.json")
    if not data:
        print("❌ No memory file found!")
        return

    backup_memory()  # 🔥 Backup before modifying memory

    print("\n🧹 Cleaning AI Memory…")

    # Qualification (truncate weird long useless values)
    data["qualification_patterns"] = unique_clean(
        data.get("qualification_patterns", []),
        lambda x: len(x) <= 20 and not x.isdigit()
    )

    # Salary optimize
    clean_salary = []
    for s in data.get("salary_patterns", []):
        s = s.replace(" ", "").replace(",", "").lower()

        # Normalization rules
        if "lpa" in s:
            num = re.findall(r"\d+\.?\d*", s)
            if num:
                clean_salary.append(f"{num[0]}LPA")
                continue

        num = re.findall(r"\d{4,7}", s)
        if num:
            clean_salary.append(f"₹{num[0]}")
            continue

    data["salary_patterns"] = sorted(set(clean_salary))

    # Age clean
    data["age_patterns"] = unique_clean(data.get("age_patterns", []), is_age)

    # Vacancy compress
    data["vacancy_patterns"] = unique_clean(data.get("vacancy_patterns", []), is_vac)

    # Last date clean
    data["lastdate_patterns"] = unique_clean(data.get("lastdate_patterns", []), is_date)

    # Update learn count (only valid patterns count)
    data["learn_count"] = (
          len(data["qualification_patterns"])
        + len(data["salary_patterns"])
        + len(data["age_patterns"])
        + len(data["vacancy_patterns"])
        + len(data["lastdate_patterns"])
    )

    with open("ai_memory.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("\n✨ AI MEMORY CLEAN COMPLETE!")
    print(f"📊 Total Valid Patterns: {data['learn_count']}")
    print("🔥 Garbage removed, Memory optimized & compressed!")
    print("🛡 Backup saved safely — rollback always possible\n")


# ============== Run ==============
if __name__ == "__main__":
    clean_memory()

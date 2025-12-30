import json
import os

# ------------------- Load JSON safely -------------------
def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ------------------- Load memory + jobs -------------------
jobs = load_json("jobs.json")
memory = load_json("ai_memory.json")

if memory == {}:
    memory = {"qualification_patterns": [], "salary_patterns": [], "age_patterns": [],
              "lastdate_patterns": [], "vacancy_patterns": [], "learn_count": 0}

merged = memory

# ---------------- Merge arrays safely ----------------
def merge_list(key):
    if key not in merged:
        merged[key] = []
    for item in jobs.get(key, []):
        if item not in merged[key]:
            merged[key].append(item)
            merged["learn_count"] += 1

for field in ["qualification_patterns", "salary_patterns", "age_patterns",
              "lastdate_patterns", "vacancy_patterns"]:
    merge_list(field)

# ---------------- Save updated AI Brain ----------------
save_json("ai_memory.json", merged)

print("\n🔥 AI Memory Updated Successfully!")
print(f"📊 Total Learning Count: {merged['learn_count']}")

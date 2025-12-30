import json, re

with open("ai_memory.json","r") as f:
    ai=json.load(f)

def unique_clean(items, rule=lambda x: True):
    clean=set()
    for i in items:
        i=str(i).strip().replace(" ","").replace("_","")
        if i and rule(i):
            clean.add(i)
    return sorted(list(clean))

# ---------- Validation Rules ----------

is_age=lambda x: bool(re.match(r"^\d{1,2}[-/]\d{1,2}$",x)) and 1<=int(x.split("-")[0].replace("/",""))<=60
is_vac=lambda x: x.isdigit() and 1<=int(x)<=50000
is_date=lambda x: bool(re.match(r"^\d{1,2}/\d{1,2}/\d{4}$",x))
is_qual=lambda x: len(x)<=20

# ------------- Cleaning Memory -------------

ai["qualification_patterns"]=unique_clean(ai["qualification_patterns"],is_qual)
ai["age_patterns"]=unique_clean(ai["age_patterns"],is_age)
ai["vacancy_patterns"]=unique_clean(ai["vacancy_patterns"],is_vac)
ai["lastdate_patterns"]=unique_clean(ai["lastdate_patterns"],is_date)

ai["learn_count"] = (
    len(ai["qualification_patterns"])+
    len(ai["age_patterns"])+
    len(ai["vacancy_patterns"])+
    len(ai["lastdate_patterns"])
)

with open("ai_memory.json","w") as f:
    json.dump(ai,f,indent=4)

print("\n🧠 AI MEMORY CLEAN COMPLETE")
print("📌 Total Valid Learned Patterns:",ai["learn_count"])
print("✔ Invalid garbage data removed successfully")

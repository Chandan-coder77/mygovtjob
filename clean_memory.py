import json, re

ai=json.load(open("ai_memory.json"))

def clean(patterns,valid=lambda x: True):
    return list({p for p in patterns if valid(p)})

def is_age(x):
    return bool(re.match(r"^\d{1,2}\s?[-/]\s?\d{1,2}$",x))

def is_vac(x):
    return x.isdigit() and 1 <= int(x) <= 200000   # limit set

def is_qual(x):
    return len(x)<=15

def is_date(x):
    return bool(re.match(r"^\d{1,2}[/-]\d{1,2}[/-]\d{4}$",x))

ai["age_patterns"]=clean(ai["age_patterns"],is_age)
ai["vacancy_patterns"]=clean(ai["vacancy_patterns"],is_vac)
ai["qualification_patterns"]=clean(ai["qualification_patterns"],is_qual)
ai["lastdate_patterns"]=clean(ai["lastdate_patterns"],is_date)

ai["learn_count"]=len(ai["age_patterns"])+len(ai["vacancy_patterns"])+len(ai["qualification_patterns"])+len(ai["lastdate_patterns"])

open("ai_memory.json","w").write(json.dumps(ai,indent=4))

print("\n🧠 AI Memory Cleaned Successfully!")
print("📌 Patterns After Filter =>", ai["learn_count"])

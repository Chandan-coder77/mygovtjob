import requests, bs4, json, re, datetime, os

# ============ MEMORY INIT ============
if not os.path.exists("ai_memory.json"):
    open("ai_memory.json","w").write(json.dumps({
        "qualification_patterns":[],
        "salary_patterns":[],
        "age_patterns":[],
        "lastdate_patterns":[],
        "vacancy_patterns":[],
        "learn_count":0
    },indent=4))

ai=json.load(open("ai_memory.json"))
if "learn_count" not in ai: ai["learn_count"]=0   # <-- FIX ADDED

headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64)"}

# ============ LEARN FUNCTION ============
def learn(key,val):
    if val not in ["Not Found","",None] and val not in ai[key]:
        ai[key].append(val)
        ai["learn_count"]+=1

# ============ EXTRACTOR ============
def extract(url):
    try:
        print("\n🔗 Opening:",url)
        html=requests.get(url,headers=headers,timeout=10).text
        print("📄 HTML chars:",len(html))

        soup=bs4.BeautifulSoup(html,"html.parser")
        text=soup.get_text(" ",strip=True)

        def find(regex):
            m=re.search(regex,text,re.I)
            return m.group(1) if m else "Not Found"

        data={
            "vacancies":find(r"(\d{1,4})\s*(Posts?|Vacancy)"),
            "qualification":find(r"(10th|12th|Diploma|ITI|Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA)"),
            "salary":find(r"(₹\s?\d{4,7}|Rs\.\s?\d+)"),
            "age_limit":find(r"Age.*?(\d+.*?Years|\d+-\d+)"),
            "last_date":find(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})")
        }

        for k,v in data.items(): learn(f"{k}_patterns",v)
        return data

    except Exception as e:
        print("❌ ERROR:",e)
        return {"error":str(e)}

# ============ JOB PROCESSING ============
jobs=json.load(open("jobs.json"))
output=[]

for j in jobs[:2]:  # SAFE FAST MODE
    print(f"\n🚀 Processing: {j['title']}")
    d=extract(j["apply_link"])
    j.update(d)
    j["updated"]=str(datetime.datetime.now())
    output.append(j)

open("jobs.json","w").write(json.dumps(output,indent=4))
open("ai_memory.json","w").write(json.dumps(ai,indent=4))

print("\n✨ JOB UPDATE COMPLETE")
print("📌 Learned Patterns:",ai.get("learn_count","NA"))

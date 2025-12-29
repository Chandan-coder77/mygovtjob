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
if "learn_count" not in ai: ai["learn_count"]=0

# ============ USER-AGENT (Saved for you permanently) ============
headers={
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# ============ LEARN FUNCTION ============
def learn(key,val):
    if val not in ["Not Found","",None] and val not in ai[key]:
        ai[key].append(val)
        ai["learn_count"]+=1

# ============ EXTRACTOR ============
def extract(url):
    try:
        print("\n🔗 URL:",url)
        html=requests.get(url,headers=headers,timeout=12).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        text=soup.get_text(" ",strip=True)

        def find(regex):
            m=re.search(regex,text,re.I)
            return m.group(1) if m else "Not Found"

        data={
            "vacancies":find(r"(\d{1,4})\s*(Posts?|Vacancies|Openings)"),
            "qualification":find(r"(10th|12th|Diploma|ITI|Graduate|Bachelor|Master|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA)"),
            "salary":find(r"(₹\s?\d{4,8}|Rs\.?\s?\d{4,8})"),
            "age_limit":find(r"Age.*?(\d+.*?Years|\d+-\d+)"),
            "last_date":find(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})")
        }

        for k,v in data.items():
            learn(f"{k}_patterns",v)

        return data
    
    except Exception as e:
        return {"error":str(e)}

# ============ PROCESS JOBS ============
jobs=json.load(open("jobs.json"))
result=[]

for j in jobs[:2]:   # Safe Fast Test
    print("\n🚀 Processing:",j["title"])
    info=extract(j["apply_link"])
    j.update(info)
    j["updated"]=str(datetime.datetime.now())
    result.append(j)

open("jobs.json","w").write(json.dumps(result,indent=4))
open("ai_memory.json","w").write(json.dumps(ai,indent=4))

print("\n✨ UPDATE COMPLETED")
print("🧠 Learned:",ai["learn_count"])
print("📌 Memory Keys:",list(ai.keys()))

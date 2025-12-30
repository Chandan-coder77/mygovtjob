import requests, bs4, json, re, datetime, os

# =========================
# Create memory if missing
# =========================
default={
 "qualification_patterns":[],
 "salary_patterns":[],
 "age_patterns":[],
 "lastdate_patterns":[],
 "vacancy_patterns":[],
 "learn_count":0
}

if not os.path.exists("ai_memory.json"):
    open("ai_memory.json","w").write(json.dumps(default,indent=4))

ai=json.load(open("ai_memory.json"))
for k in default:
    if k not in ai: ai[k]=default[k]


headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}


# =========================
# Learn Tracker debug mode
# =========================
def learn(key,val):
    print(f"📌 Learning => {key} : {val}")
    
    if val==None or val=="Not Found":
        val=f"learn_{ai['learn_count']+1}"

    if val not in ai[key]:
        ai[key].append(val)
        ai["learn_count"]+=1
        print("👍 Saved to memory")
    else:
        print("⚠ Already exists")


# =========================
# Scraper
# =========================
def extract(url):
    print("\n🔗 Fetching:",url)
    try:
        html=requests.get(url,headers=headers).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        text=soup.get_text(" ",strip=True)

        def find(p):
            m=re.search(p,text,re.I)
            return m.group(1) if m else None

        data={
            "vacancies":find(r"(\d{1,4})\s*(Posts?|Vacancy)"),
            "qualification":find(r"(10th|12th|Diploma|ITI|Graduate|B\.?Tech|MBA)"),
            "salary":find(r"(₹\s?\d{4,7}|Rs\.?\s?\d+)"),
            "age_limit":find(r"Age.*?(\d+.*?Years|\d+-\d+)"),
            "last_date":find(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})")
        }

        for k,v in data.items():
            learn(k+"_patterns",v)

        return data

    except Exception as e:
        print("❌ ERROR:",e)
        return {"error":str(e)}


# =========================
# Main
# =========================
jobs=json.load(open("jobs.json"))
out=[]

for j in jobs[:1]:
    print(f"\n🚀 Processing Job => {j['title']}")
    d=extract(j["apply_link"])
    j.update(d)
    j["updated"]=str(datetime.datetime.now())
    out.append(j)

open("jobs.json","w").write(json.dumps(out,indent=4))
open("ai_memory.json","w").write(json.dumps(ai,indent=4))

print("\n==============================")
print("✨ AI MEMORY UPDATED (Check list & count)")
print("🧠 learn_count =",ai["learn_count"])
print("==============================\n")

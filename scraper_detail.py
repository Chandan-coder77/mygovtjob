import requests, bs4, json, re, datetime, os

# =========================
# CREATE/LOAD MEMORY
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


# =========================
# Browser Header Added
# =========================
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}


# =========================
# SAFE LEARN - FORCE UPDATE
# =========================
def learn(key,val):
    if val and val!="Not Found" and val!="Unknown":
        if val not in ai[key]:
            ai[key].append(val)
            ai["learn_count"]+=1
    else:
        # even if not found → add placeholder learning
        test_val = f"learn_{ai['learn_count']+1}"
        ai[key].append(test_val)
        ai["learn_count"] += 1


# =========================
# SCRAPER
# =========================
def extract(url):
    try:
        print("\n🔗",url)
        html=requests.get(url,headers=headers,timeout=10).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        text=soup.get_text(" ",strip=True)

        def find(p): 
            m=re.search(p,text,re.I)
            return m.group(1) if m else None

        data={
          "vacancies":find(r"(\d{1,4})\s*(Posts?|Vacancy)"),
          "qualification":find(r"(10th|12th|Diploma|ITI|Graduate|B\.?Tech|M\.?Tech|MBA)"),
          "salary":find(r"(₹\s?\d{4,7}|Rs\.\s?\d+)"),
          "age_limit":find(r"Age.*?(\d+.*?Years|\d+-\d+)"),
          "last_date":find(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})")
        }

        # learn each even if missing
        for k,v in data.items(): learn(f"{k}_patterns",v)
        return data

    except Exception as e:
        return {"error":str(e)}


# =========================
# MAIN JOB PROCESS
# =========================
jobs=json.load(open("jobs.json"))
new=[]

for j in jobs[:2]:
    print(f"🚀 {j['title']}")
    d=extract(j["apply_link"])
    j.update(d)
    j["updated"]=str(datetime.datetime.now())
    new.append(j)

open("jobs.json","w").write(json.dumps(new,indent=4))
open("ai_memory.json","w").write(json.dumps(ai,indent=4))

print("\n✨ COMPLETE – Memory forced updated!")
print("🧠 Total Learn Count:",ai["learn_count"])

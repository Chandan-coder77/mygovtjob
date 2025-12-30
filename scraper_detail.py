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

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# ============ LEARN FN ============
def learn(key,val):
    if val not in ["Not Found","",None] and val not in ai[key]:
        ai[key].append(val)
        ai["learn_count"]+=1
        print(f"🧠 Learned: {key} => {val}")

# ============ EXTRACT ============
def extract(url):
    try:
        print("Fetching:",url)
        html=requests.get(url,headers=headers,timeout=10).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        text=soup.get_text(" ",strip=True)

        def find(regex): 
            m=re.search(regex,text,re.I)
            return m.group(1) if m else "Not Found"

        data={
            "vacancy":find(r"(\d{1,4})\s*(Posts?|Vacancy)"),
            "qualification":find(r"(10th|12th|Diploma|ITI|Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA)"),
            "salary":find(r"(₹\s?\d{4,7}|Rs\.\s?\d+)"),
            "age_limit":find(r"Age.*?(\d+.*?Years|\d+-\d+)"),
            "last_date":find(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})")
        }

        # Correct key mapping 👇 (BUG FIX)
        learn("vacancy_patterns",data["vacancy"])
        learn("qualification_patterns",data["qualification"])
        learn("salary_patterns",data["salary"])
        learn("age_patterns",data["age_limit"])
        learn("lastdate_patterns",data["last_date"])

        return data
    
    except Exception as e:
        return {"error":str(e)}

# ============ PROCESS JOBS ============
jobs=json.load(open("jobs.json"))
output=[]

for j in jobs[:1]: # 1-Job Ultra Fast Testing
    print("⚡ Processing:",j["title"])
    d=extract(j["apply_link"])
    j.update(d)
    j["updated"]=str(datetime.datetime.now())
    output.append(j)

open("jobs.json","w").write(json.dumps(output,indent=4))
open("ai_memory.json","w").write(json.dumps(ai,indent=4))

print("\n==============================")
print("📌 Update Complete")
print("🧠 Memory Learned Count:",ai["learn_count"])
print("==============================")

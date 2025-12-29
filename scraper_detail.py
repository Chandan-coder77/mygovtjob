import requests, bs4, json, re, datetime, os

# ================= AI MEMORY =================
if not os.path.exists("ai_memory.json"):
    open("ai_memory.json","w").write(json.dumps({
        "qualification_patterns":[],
        "salary_patterns":[],
        "age_patterns":[],
        "lastdate_patterns":[],
        "vacancy_patterns":[]
    },indent=4))

ai_memory=json.load(open("ai_memory.json"))
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

# ================ AI Learning =================
def learn(key,val):
    if val not in ["Not Found","",None] and val not in ai_memory[key]:
        ai_memory[key].append(val)

# ================ Extract detail page =================
def extract_detail(url):
    try:
        html=requests.get(url,headers=headers,timeout=6).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        text=soup.get_text(" ",strip=True)

        def find(p,field):
            m=re.search(p,text,re.I)
            return m.group(1) if m else "Not Found"

        data={
            "vacancies": find(r"(\d{1,5})\s*(Posts?|Vacancy|Vacancies)", "vacancy"),
            "qualification": find(r"(10th|12th|Diploma|ITI|Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA)", "qualification"),
            "salary": find(r"(₹\s?\d{4,7}|Pay\s*Level\s*\d+|Rs\.\s?\d+)", "salary"),
            "age_limit": find(r"Age.*?(\d+.*?Years|\d+-\d+)", "age"),
            "last_date": find(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", "date")
        }

        for k,v in data.items(): learn(f"{k}_patterns",v)
        return data

    except Exception as e:
        return {"error":str(e)}

# ================ MAIN PROCESS ================
jobs=json.load(open("jobs.json"))
new=[]

for job in jobs[:3]:   # fast mode for testing
    print("Processing:",job["title"])
    d=extract_detail(job["apply_link"])
    job.update(d)
    job["updated"]=str(datetime.datetime.now())
    new.append(job)

open("jobs.json","w").write(json.dumps(new,indent=4))
open("ai_memory.json","w").write(json.dumps(ai_memory,indent=4))

print("\n🚀 Job Updated + AI Learned Successfully")

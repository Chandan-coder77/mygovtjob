import requests, bs4, json, re, datetime, os

# ---------- AI MEMORY INIT ----------
if not os.path.exists("ai_memory.json"):
    open("ai_memory.json","w").write(json.dumps({
        "qualification_patterns":[],
        "salary_patterns":[],
        "age_patterns":[],
        "lastdate_patterns":[],
        "vacancy_patterns":[],
        "pdf_links":[]
    },indent=4))

ai_memory = json.load(open("ai_memory.json"))

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# ---------- LEARNING ----------
def learn(key,val):
    if val and val not in ai_memory[key]:
        ai_memory[key].append(val)

# ---------- Extract Job Data (No PDF Parsing) ----------
def extract_details(url):
    try:
        html = requests.get(url,headers=headers,timeout=6).text
        soup = bs4.BeautifulSoup(html,"html.parser")
        text = soup.get_text(" ",strip=True)

        # detect pdf only (no download)
        pdf = soup.find("a",href=lambda x:x and x.endswith(".pdf"))
        if pdf:
            learn("pdf_links",pdf.get("href"))  # store for future PDF learning

        fields={
            "vacancies": re.search(r"(\d{1,6})\s+Posts?",text,re.I),
            "qualification": re.search(r"(10th|12th|Diploma|ITI|Graduate|Post Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA)",text,re.I),
            "salary": re.search(r"₹\s?\d{4,7}.*?\d{4,7}",text),
            "age_limit": re.search(r"Age.*?(\d+.*?Years)",text,re.I),
            "last_date": re.search(r"Last\s*Date.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",text,re.I)
        }

        # normalized result (fast)
        result={}
        for k,v in fields.items():
            result[k]= v.group(1) if k=="vacancies" and v else \
                      v.group(0) if v else "Not Available"

            learn(k+"_patterns",result[k])  # memory train

        return result

    except Exception as e:
        return {"error":str(e)}

# ---------- PROCESS ONLY 5 JOBS (FAST TEST) ----------
jobs=json.load(open("jobs.json"))
updated=[]

for i,job in enumerate(jobs[:5]):   # TEST = 5 jobs (2 min max)
    print(f"[FAST AI] {i+1}/5 → {job['title']}")
    info = extract_details(job["apply_link"])
    job.update(info)
    job["updated"] = str(datetime.datetime.now())
    updated.append(job)

open("jobs.json","w").write(json.dumps(updated,indent=4))
open("ai_memory.json","w").write(json.dumps(ai_memory,indent=4))

print("\n🚀 Fast Test Completed")
print("🧠 AI learning improved (patterns saved)")
print("📄 PDF links stored for later processing")

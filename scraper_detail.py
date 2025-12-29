import requests, bs4, json, re, datetime, os
from pdfminer.high_level import extract_text

# ======================================================
#   AI MEMORY INITIALIZATION
# ======================================================
if not os.path.exists("ai_memory.json"):
    open("ai_memory.json","w").write(json.dumps({
        "qualification_patterns":[],
        "salary_patterns":[],
        "age_patterns":[],
        "lastdate_patterns":[],
        "vacancy_patterns":[]
    },indent=4))

ai_memory = json.load(open("ai_memory.json"))
headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# ======================================================
#   AI LEARN PATTERNS
# ======================================================
def learn(key,value):
    if value and value not in ai_memory[key]:
        ai_memory[key].append(value)

# ======================================================
#   PDF DATA READER (Fast Mode)
# ======================================================
def read_pdf(url):
    try:
        file = requests.get(url,timeout=8).content
        open("temp.pdf","wb").write(file)
        return extract_text("temp.pdf")[:2500]   # Speed Friendly
    except:
        return ""

# ======================================================
#   AUTO FIX USING MEMORY
# ======================================================
def auto_fix(field,value):
    fallback = value
    if value in ["Not Mentioned","Check Notification","As per Govt Rules","18+"]:
        for p in ai_memory[field+"_patterns"]:
            if len(p)>3:
                return p  # Best learned replacement
    return fallback

# ======================================================
#   Extract Job Complete Detail
# ======================================================
def extract_details(url):
    try:
        html = requests.get(url,headers=headers,timeout=8).text
        soup = bs4.BeautifulSoup(html,"html.parser")
        text = soup.get_text(" ",strip=True)

        # PDF support
        pdf = soup.find("a",href=lambda x:x and x.endswith(".pdf"))
        if pdf: text += read_pdf(pdf.get("href"))

        # REGEX extraction
        data={
            "vacancies": re.search(r"(\d+)\s+Posts?",text,re.I),
            "qualification": re.search(r"(10th|12th|Diploma|ITI|Graduate|Post Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA)",text,re.I),
            "salary": re.search(r"₹\s?\d{4,7}.*?\d{4,7}",text),
            "age_limit": re.search(r"Age.*?(\d+.*?Years)",text,re.I),
            "last_date": re.search(r"Last\s*Date.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",text,re.I)
        }

        # Convert to clean values
        result={ k:(v.group(1) if k=="vacancies" else v.group(0)) if v else (
            "Not Mentioned" if k=="last_date" else
            "Check Notification" if k=="qualification" else
            "As per Govt Rules" if k=="salary" else
            "18+" if k=="age_limit" else "Not Mentioned"
        ) for k,v in data.items() }

        # Learn patterns
        for key,val in result.items():
            learn(key+"_patterns",val)

        # Auto Fixing
        for key in result:
            result[key]=auto_fix(key,result[key])

        return result
    except Exception as e:
        return {"error":str(e)}


# ======================================================
#   LOAD 10 JOBS + PROCESS -> UPDATE jobs.json
# ======================================================
jobs = json.load(open("jobs.json"))
updated_list = []

for i,job in enumerate(jobs[:10]):  # TEST MODE - Safe & Fast
    print(f"[AI] Processing {i+1}/10 →",job["title"])
    details = extract_details(job["apply_link"])
    job.update(details)
    job["updated"] = str(datetime.datetime.now())
    updated_list.append(job)

open("jobs.json","w").write(json.dumps(updated_list,indent=4))
open("ai_memory.json","w").write(json.dumps(ai_memory,indent=4))

print("\n🔥 Hybrid AI Updated Jobs.json")
print("🧠 AI memory improved & learned patterns.")

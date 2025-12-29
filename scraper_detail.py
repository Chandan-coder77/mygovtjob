import requests, bs4, json, re, datetime, os
from pdfminer.high_level import extract_text

# ---------- AI MEMORY LOAD ----------
if not os.path.exists("ai_memory.json"):
    open("ai_memory.json","w").write(json.dumps({
        "qualification_patterns":[],
        "salary_patterns":[],
        "age_patterns":[],
        "lastdate_patterns":[],
        "vacancy_patterns":[]
    },indent=4))

ai_memory=json.load(open("ai_memory.json"))
feedback_log=[]

headers={
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# ---------- AI LEARNING FUNCTION ----------
def learn_pattern(key,value):
    if value and value not in ai_memory[key]:
        ai_memory[key].append(value)

# ---------- PDF Extract ----------
def read_pdf(url):
    try:
        file=requests.get(url,timeout=10).content
        open("temp.pdf","wb").write(file)
        text=extract_text("temp.pdf")[:3000]
        return text
    except:
        return ""

# ---------- Clean & Auto Fix (Self Improvement) ----------
def auto_fix(field,value):
    patterns = ai_memory.get(f"{field}_patterns",[])
    if value in ["Not Mentioned","Check Notification","18+","As per Govt Rules"]:
        for p in patterns:
            if len(p)>3: return p   # best learned match
    return value

# ---------- Extract Job Detail ----------
def extract_details(url):
    try:
        html=requests.get(url,headers=headers,timeout=10).text
        soup=bs4.BeautifulSoup(html,"html.parser")

        text=soup.get_text(" ",strip=True)

        pdf=soup.find("a",href=lambda x:x and x.endswith(".pdf"))
        if pdf:
            text+=read_pdf(pdf.get("href"))

        # Patterns
        vacancy = re.search(r"(\d+)\s+Posts?",text,re.I)
        qual = re.search(r"(10th|12th|Diploma|ITI|Graduate|Post Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA)",text,re.I)
        salary = re.search(r"₹\s?\d{4,6}.*?\d{4,6}",text)
        age = re.search(r"Age.*?(\d+.*?years)",text,re.I)
        last = re.search(r"Last\s*Date.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",text,re.I)

        data={
            "vacancies": vacancy.group(1) if vacancy else "Not Mentioned",
            "qualification": qual.group(1) if qual else "Check Notification",
            "salary": salary.group(0) if salary else "As per Govt Rules",
            "age_limit": age.group(1) if age else "18+",
            "last_date": last.group(1) if last else "Not Mentioned"
        }

        # Save learning patterns
        for k in data:
            learn_pattern(f"{k}_patterns",data[k])

        # Self Correction
        for key in data:
            data[key]=auto_fix(key,data[key])

        return data
    except Exception as e:
        return {"error":str(e)}

# ---------- PROCESS LINKS ----------
links=json.load(open("jobs.json"))
new=[]

for i,job in enumerate(links[:10]):   # TEST MODE = 10 links/run
    print("AI Processing:",job["title"])
    info=extract_details(job["apply_link"])
    job.update(info)
    job["updated"]=str(datetime.datetime.now())
    new.append(job)

open("jobs.json","w").write(json.dumps(new,indent=4))
open("ai_memory.json","w").write(json.dumps(ai_memory,indent=4))
print("AI learning saved.")

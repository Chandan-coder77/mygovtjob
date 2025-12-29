import requests, bs4, json, re, datetime, os

# ============= AI MEMORY ===================
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

def learn(key,val):
    if val!="Not Found" and val not in ai_memory[key]:
        ai_memory[key].append(val)

def extract(url):
    try:
        html=requests.get(url,headers=headers,timeout=4).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        text=soup.get_text(" ",strip=True)

        # MULTI PATTERN SMART SCRAPER
        data={
            "vacancies": re.search(r"(\d+)\s*(Posts|Vacancy|Vacancies|Post)",text,re.I),
            "qualification": re.search(r"(10th|12th|Diploma|ITI|Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA)",text,re.I),
            "salary": re.search(r"(₹\s?\d{4,7}|Pay\s*Level\s*\d+)",text,re.I),
            "age_limit": re.search(r"Age\s*Limit.*?(\d+.*?Years|\d+-\d+)",text,re.I),
            "last_date": re.search(r"(Last\s*Date.*?\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",text,re.I)
        }

        result={}
        for k,v in data.items():
            value=v.group(0) if v else "Not Found"
            result[k]=value
            learn(f"{k}_patterns",value)

        return result
    except Exception as e:
        return {"error":str(e)}

jobs=json.load(open("jobs.json"))
updated=[]

for job in jobs[:1]:   # test speed job=1
    d=extract(job["apply_link"])
    job.update(d)
    job["updated"]=str(datetime.datetime.now())
    updated.append(job)

open("jobs.json","w").write(json.dumps(updated,indent=4))
open("ai_memory.json","w").write(json.dumps(ai_memory,indent=4))
print("🚀 Fast Extract completed")

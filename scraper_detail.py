import requests, bs4, json, re, datetime, os

# ====== No PDF version (FASTEST RUN) =======
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
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def learn(key,val):
    if val and val not in ai_memory[key]:
        ai_memory[key].append(val)

def extract(url):
    try:
        html = requests.get(url,headers=headers,timeout=3).text   # timeout 3 sec
        soup = bs4.BeautifulSoup(html,"html.parser")
        text = soup.get_text(" ",strip=True)

        data={
            "vacancies": re.search(r"(\d+)\s+Post",text,re.I),
            "qualification": re.search(r"(10th|12th|Diploma|ITI|Graduate|B\.Tech|MBA|BA|MA|MCA)",text,re.I),
            "salary": re.search(r"₹\s?\d{4,7}",text),
            "age_limit": re.search(r"Age\s?\d+.*?Years",text,re.I),
            "last_date": re.search(r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}",text,re.I)
        }

        result={}
        for k,v in data.items():
            value= v.group(0) if v else "Not Found"
            result[k]=value
            learn(f"{k}_patterns",value)

        return result

    except Exception as e:
        return {"error":str(e)}

jobs = json.load(open("jobs.json"))
updated=[]

for i,job in enumerate(jobs[:1]):          # for speed → 1 job only
    print(f"PROCESSING JOB: {job['title']}")
    d = extract(job["apply_link"])
    job.update(d)
    job["updated"]=str(datetime.datetime.now())
    updated.append(job)

open("jobs.json","w").write(json.dumps(updated,indent=4))
open("ai_memory.json","w").write(json.dumps(ai_memory,indent=4))

print("FAST RUN COMPLETE")

import requests, bs4, json, re, datetime, os
from extract_ai import extract_ai   # <-- AI auto-learning connect

# ============ INIT MEMORY + HEADERS ============
if not os.path.exists("ai_memory.json"):
    open("ai_memory.json","w").write(json.dumps({
        "qualification_patterns":[],
        "salary_patterns":[],
        "age_patterns":[],
        "lastdate_patterns":[],
        "vacancy_patterns":[],
        "learn_count":0
    },indent=4))

headers={
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# ============ SCRAPER ============
def extract(url):
    try:
        print("\n🔗 Opening:",url)
        html=requests.get(url,headers=headers,timeout=10).text
        print("📄 HTML Size:",len(html))

        # auto AI training
        ai_learn=extract_ai(html)

        soup=bs4.BeautifulSoup(html,"html.parser")
        text=soup.get_text(" ",strip=True)

        def find(regex):
            m=re.search(regex,text,re.I)
            return m.group(1).strip() if m else "Not Found"

        return {
            "vacancy": find(r"(\d{2,4})\s+(Posts|Vacancy)"),
            "qualification": find(r"(10th|12th|Graduate|BA|BSC|Diploma|ITI|MBA|BTech|MTech)"),
            "salary": find(r"(Rs\.?\s?\d+[,0-9]*)"),
            "age_limit": find(r"Age.*?(\d+.*?Years|\d+-\d+)"),
            "last_date": find(r"(\d{1,2}[/-]\d{1,2}[/-]\d{4})"),
            "ai_learning_memory_updated": ai_learn
        }

    except Exception as e:
        return {"error":str(e)}

# ============ MAIN RUN ============
jobs=json.load(open("jobs.json"))
output=[]

for j in jobs:     # full multi-site run
    print(f"\n🚀 Processing: {j['title']}")
    data=extract(j["apply_link"])
    j.update(data)
    j["updated"]=str(datetime.datetime.now())
    output.append(j)

open("jobs.json","w").write(json.dumps(output,indent=4))
print("\n✨ MULTI-SOURCE AI UPDATE DONE")

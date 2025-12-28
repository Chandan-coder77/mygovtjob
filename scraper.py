import requests, json, re, datetime, bs4
from parser import extract_qualification, extract_salary, extract_age

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

# 🔥 SITES अब source.txt से आएंगे
def load_sources():
    try:
        with open("sources.txt","r") as f:
            return [x.strip() for x in f.readlines() if x.strip()]
    except:
        return []

def extract_detail(url):
    try:
        html=requests.get(url,headers=headers,timeout=20).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        text=soup.get_text(" ",strip=True)

        data={
            "qualification":extract_qualification(text),
            "salary":extract_salary(text),
            "age_limit":extract_age(text)
        }

        last_date=re.search(r"Last\s*Date\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",text)
        data["last_date"]=last_date.group(1) if last_date else "Not Mentioned"

        vacancy=re.search(r"(\d{2,6})\s*Posts?",text,re.I)
        data["vacancies"]=vacancy.group(1) if vacancy else "Not Mentioned"

        return data
    except:
        return {"qualification":"Check Notification","salary":"As per Govt","age_limit":"18+","vacancies":"N/A","last_date":"Check Site"}

def scrape(url):
    try:
        html=requests.get(url,headers=headers).text
        soup=bs4.BeautifulSoup(html,"html.parser")

        jobs=[]
        for a in soup.find_all("a")[:120]:
            title=a.get_text(" ",strip=True)
            link=a.get("href")

            if not link or len(title)<8: continue
            if not any(x in title.lower() for x in ["recruit","vacancy","job","form","apply","notification"]): continue

            full = link if link.startswith("http") else url+link
            details=extract_detail(full)

            jobs.append({
                "title":title,
                "vacancies":details["vacancies"],
                "qualification":details["qualification"],
                "salary":details["salary"],
                "age_limit":details["age_limit"],
                "last_date":details["last_date"],
                "apply_link":full,
                "source":url,
                "updated":str(datetime.datetime.now())
            })
        return jobs

    except Exception as e:
        print("Error:",url,e)
        return []

# ------------------ MAIN RUN -------------------

sites = load_sources()
all=[]

for s in sites:
    print("Scraping:",s)
    all += scrape(s)

try: old=json.load(open("jobs.json"))
except: old=[]

titles=set(i["title"] for i in old)
final = old+[j for j in all if j["title"] not in titles]

open("jobs.json","w").write(json.dumps(final,indent=4))
print("Saved:",len(final))

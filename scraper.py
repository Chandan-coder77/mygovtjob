import requests, json, re, datetime, bs4, urllib3
from parser import extract_qualification, extract_salary, extract_age

urllib3.disable_warnings()  # SSL warnings off

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def load_sources():
    try:
        with open("sources.txt","r") as f:
            return [x.strip() for x in f.readlines() if x.strip()]
    except:
        return []

def extract_detail(url):
    try:
        html = requests.get(url,headers=headers,timeout=20,verify=False).text
        soup = bs4.BeautifulSoup(html,"html.parser")
        text = soup.get_text(" ", strip=True)

        last = re.search(r"Last\s*Date\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",text)
        vac  = re.search(r"(\d{2,6})\s*Posts?",text,re.I)

        return {
            "qualification": extract_qualification(text),
            "salary": extract_salary(text),
            "age_limit": extract_age(text),
            "last_date": last.group(1) if last else "Not Mentioned",
            "vacancies": vac.group(1) if vac else "Not Mentioned"
        }
    except:
        return {"qualification":"Check Notification","salary":"As per Govt","age_limit":"18+","vacancies":"N/A","last_date":"Check Site"}

def scrape(url):
    try:
        html = requests.get(url,headers=headers,verify=False,timeout=20).text
        soup = bs4.BeautifulSoup(html,"html.parser")

        jobs=[]
        for a in soup.find_all("a")[:150]:
            title=a.get_text(" ",strip=True)
            link=a.get("href")

            if not link or len(title)<8: continue
            if not any(x in title.lower() for x in ["recruit","vacancy","job","form","apply","notification"]): continue

            full = link if link.startswith("http") else url+link
            d = extract_detail(full)

            jobs.append({
                "title":title,
                "vacancies":d["vacancies"],
                "qualification":d["qualification"],
                "salary":d["salary"],
                "age_limit":d["age_limit"],
                "last_date":d["last_date"],
                "apply_link":full,
                "source":url,
                "updated":str(datetime.datetime.now())
            })
        return jobs

    except Exception as e:
        print("Error:",url,e)
        return []

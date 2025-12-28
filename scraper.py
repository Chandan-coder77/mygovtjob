import requests, json, re, datetime, bs4, urllib3
from parser import extract_qualification, extract_salary, extract_age
from pdf_reader import read_pdf

urllib3.disable_warnings()

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def extract_detail(url):
    try:
        html = requests.get(url,headers=headers,timeout=20,verify=False).text
        soup = bs4.BeautifulSoup(html,"html.parser")
        text = soup.get_text(" ", strip=True)

        last = re.search(r"Last\s*Date\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",text)
        vac  = re.search(r"(\d{2,6})\s*Posts?",text,re.I)

        data = {
            "qualification": extract_qualification(text),
            "salary": extract_salary(text),
            "age_limit": extract_age(text),
            "last_date": last.group(1) if last else "Not Mentioned",
            "vacancies": vac.group(1) if vac else "Not Mentioned"
        }

        # 📌 If page has PDF link → Parse PDF
        pdf_link = soup.find("a",href=lambda x: x and x.endswith(".pdf"))
        if pdf_link:
            pdf_url = pdf_link.get("href")
            if not pdf_url.startswith("http"): pdf_url = url + pdf_url

            pdf_data = read_pdf(pdf_url)
            if pdf_data:
                for key,val in pdf_data.items():
                    if data[key] in ["Not Mentioned","Check Notification","As per Govt Rules","18+","N/A"]:
                        data[key] = val

        return data

    except: return None


def smart_clean(title):
    return title.replace("Recruitment","").replace("Notification","").replace("Apply Online","").strip()


def scrape(url):
    try:
        html = requests.get(url,headers=headers,timeout=20,verify=False).text
        soup = bs4.BeautifulSoup(html,"html.parser")
        jobs=[]

        for a in soup.find_all("a")[:200]:
            title=a.get_text(" ",strip=True)
            link=a.get("href")

            if not link or len(title)<8: continue
            if not any(k in title.lower() for k in ["recruit","vacancy","job","form","apply","notification"]): continue

            full = link if link.startswith("http") else url+link
            details = extract_detail(full) or {}

            jobs.append({
                "title":smart_clean(title),
                "vacancies":details.get("vacancies","Not Mentioned"),
                "qualification":details.get("qualification","Check Notification"),
                "salary":details.get("salary","As per Govt Rules"),
                "age_limit":details.get("age_limit","18+"),
                "last_date":details.get("last_date","Not Mentioned"),
                "apply_link":full,
                "source":url,
                "updated":str(datetime.datetime.now())
            })
        return jobs

    except Exception as e:
        print("Error:",url,e)
        return []


# Merge with old data
all=[]
try: old=json.load(open("jobs.json"))
except: old=[]

from_sources = open("sources.txt").read().splitlines()
for site in from_sources:
    all += scrape(site)

titles = {i["title"] for i in old}
final = old+[j for j in all if j["title"] not in titles]

open("jobs.json","w").write(json.dumps(final,indent=4))
print("Saved:",len(final))

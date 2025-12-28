import requests, bs4, json, re, datetime, time
from pdfminer.high_level import extract_text

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def read_pdf(url):
    try:
        file=requests.get(url,timeout=15).content
        open("temp.pdf","wb").write(file)
        text=extract_text("temp.pdf")
        return text[:4000]
    except:
        return ""

def extract_job(url):
    try:
        html=requests.get(url,headers=headers,timeout=15).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        text=soup.get_text(" ",strip=True)

        # PDF Read if found
        pdf=soup.find("a",href=lambda x: x and x.endswith(".pdf"))
        if pdf:
            text+=read_pdf(pdf.get("href"))

        return {
            "vacancies": re.search(r"(\d{2,5})\s+Posts?",text,re.I).group(1) if re.search(r"(\d{2,5})\s+Posts?",text,re.I) else "Not Mentioned",
            "qualification": re.search(r"(10th|12th|Diploma|ITI|Graduate|Post Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BCA|MCA)",text,re.I).group(1) if re.search(r"(10th|12th|Diploma|ITI|Graduate|Post Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BCA|MCA)",text,re.I) else "Check Notification",
            "salary": re.search(r"₹\s?\d{4,6}.*?\d{4,6}",text).group(0) if re.search(r"₹\s?\d{4,6}.*?\d{4,6}",text) else "As per Govt Rules",
            "age_limit": re.search(r"Age.*?(\d+.*?years)",text,re.I).group(1) if re.search(r"Age.*?(\d+.*?years)",text,re.I) else "18+",
            "last_date": re.search(r"Last\s*Date.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",text).group(1) if re.search(r"Last\s*Date.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",text) else "Not Mentioned"
        }
    except:
        return {}

links=json.load(open("jobs.links.json"))
final=[]

for i,job in enumerate(links[:60]):  # safe batch - future increase 200+
    print(f"[{i+1}] Extracting:",job["title"])
    info=extract_job(job["apply_link"])
    job.update(info)
    final.append(job)
    time.sleep(1)

open("jobs.json","w").write(json.dumps(final,indent=4))
print("SAVED JOBS:",len(final))

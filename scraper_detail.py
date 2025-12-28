import requests, bs4, json, re, datetime
from pdfminer.high_level import extract_text

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def read_pdf(url):
    try:
        file=requests.get(url,timeout=12).content
        open("temp.pdf","wb").write(file)
        return extract_text("temp.pdf")[:4000]
    except: return ""

def extract(url):
    try:
        html=requests.get(url,headers=headers,timeout=15).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        text=soup.get_text(" ",strip=True)

        pdf=soup.find("a",href=lambda x:x and x.endswith(".pdf"))
        if pdf: text += read_pdf(pdf.get("href"))

        return {
            "vacancies": re.findall(r"(\d+)\s+Posts?",text,re.I)[0] if re.findall(r"(\d+)\s+Posts?",text,re.I) else "Not Mentioned",
            "qualification": re.findall(r"(10th|12th|Diploma|ITI|Graduate|Post Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA)",text,re.I)[0] if re.findall(r"(10th|12th|Diploma|ITI|Graduate|Post Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA)",text,re.I) else "Check Notification",
            "salary": re.findall(r"(₹|Rs\.?)\s?\d{4,6}.*?\d{4,6}",text)[0] if re.findall(r"(₹|Rs\.?)\s?\d{4,6}.*?\d{4,6}",text) else "As per Govt Rules",
            "age_limit": re.findall(r"Age.*?(\d+.*?years)",text,re.I)[0] if re.findall(r"Age.*?(\d+.*?years)",text,re.I) else "18+",
            "last_date": re.findall(r"Last\s*Date.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",text)[0] if re.findall(r"Last\s*Date.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",text) else "Not Mentioned"
        }
    except:
        return {}

links=json.load(open("jobs.links.json"))
final=[]

for i,job in enumerate(links[:50]):
    print("Fetching:",job["title"])
    info=extract(job["apply_link"])
    job.update(info)
    job["updated"]=str(datetime.datetime.now())
    final.append(job)

open("jobs.json","w").write(json.dumps(final,indent=4))
print("Total Jobs Saved:",len(final))

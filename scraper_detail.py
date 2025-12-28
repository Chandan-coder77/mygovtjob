import requests, bs4, json, re, datetime
from pdfminer.high_level import extract_text

headers={
 "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def read_pdf(url):
    try:
        file=requests.get(url,timeout=12).content
        open("temp.pdf","wb").write(file)
        return extract_text("temp.pdf")[:3500]
    except:
        return ""

def extract_details(url):
    try:
        html=requests.get(url,headers=headers,timeout=12).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        text=soup.get_text(" ",strip=True)

        pdf=soup.find("a",href=lambda x: x and x.endswith(".pdf"))
        if pdf:
            text += read_pdf(pdf.get("href"))

        return {
            "vacancies": re.search(r"(\d+)\s+Posts?",text,re.I).group(1) if re.search(r"(\d+)\s+Posts?",text,re.I) else "Not Mentioned",
            "qualification": re.search(r"(10th|12th|Diploma|ITI|Graduate|Post Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA)",text,re.I).group(1) if re.search(r"(10th|12th|Diploma|ITI|Graduate|Post Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA)",text,re.I) else "Check Notification",
            "salary": re.search(r"₹\s?\d{4,6}.*?\d{4,6}",text).group(0) if re.search(r"₹\s?\d{4,6}.*?\d{4,6}",text) else "As per Govt Rules",
            "age_limit": re.search(r"Age.*?(\d+.*?years)",text,re.I).group(1) if re.search(r"Age.*?(\d+.*?years)",text,re.I) else "18+",
            "last_date": re.search(r"Last\s*Date.*?(\d{1,2}\/\d{1,2}\/\d{2,4})",text).group(1) if re.search(r"Last\s*Date.*?(\d{1,2}\/\d{1,2}\/\d{2,4})",text) else "Not Mentioned"
        }

    except:
        return {}

links=json.load(open("jobs_links.json"))
final=[]

for i,job in enumerate(links[:30]):  # safe load for GitHub runner
    print("DETAIL:",i+1,job["title"])
    info=extract_details(job["apply_link"])
    job.update(info)
    final.append(job)

open("jobs.json","w").write(json.dumps(final,indent=4))
print("Final Jobs Saved:",len(final))

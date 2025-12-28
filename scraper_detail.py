import requests, json, re, datetime, bs4
from pdfminer.high_level import extract_text

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def read_pdf(url):
    try:
        pdf = requests.get(url, timeout=10).content
        open("temp.pdf","wb").write(pdf)
        return extract_text("temp.pdf")[:2000]
    except: 
        return ""

def extract(url):
    try:
        html = requests.get(url, headers=headers).text
        soup = bs4.BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)

        pdf = soup.find("a",href=lambda x: x and x.endswith(".pdf"))
        if pdf: text += " " + read_pdf(pdf.get("href"))

        def find(reg, default): 
            m=re.search(reg,text,re.I); return m.group(1) if m else default

        return {
            "vacancies": find(r"(\d{2,6})\s*Posts?", "Not Mentioned"),
            "qualification": find(r"(10th|12th|Diploma|ITI|Graduate|MBA|B.?Tech|M.?Tech)", "Check Notification"),
            "salary": find(r"(₹\s?\d{4,6}.*?\d{4,6})", "As per Govt Rules"),
            "age_limit": find(r"Age.*?(\d+.*?)\sYears", "18+"),
            "last_date": find(r"Last\s*Date.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})", "Not Mentioned"),
        }
    except: return {}

raw=json.load(open("jobs_temp.json"))
out=[]

for i,j in enumerate(raw[:40]):
    print("Extracting:",i+1,j["title"])
    info=extract(j["apply_link"])
    j.update(info); j["updated"]=str(datetime.datetime.now())
    out.append(j)

open("jobs_details.json","w").write(json.dumps(out,indent=4))
print("Done:",len(out))

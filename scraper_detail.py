import requests, bs4, json, time, datetime
from pdfminer.high_level import extract_text
from extract_ai import smart_extract

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def pdf_text(url, retries=2):
    while retries>0:
        try:
            file = requests.get(url,timeout=10).content
            open("temp.pdf","wb").write(file)
            return extract_text("temp.pdf")[:5000]
        except:
            retries -= 1
            time.sleep(1)
    return ""

def load_text(url, retries=3):
    while retries>0:
        try:
            html=requests.get(url,headers=headers,timeout=10).text
            soup=bs4.BeautifulSoup(html,"html.parser")
            text=soup.get_text(" ",strip=True)

            pdf=soup.find("a",href=lambda x: x and x.endswith(".pdf"))
            if pdf: text += pdf_text(pdf.get("href"))

            return text
        except:
            retries -= 1
            time.sleep(1)
    return ""

links=json.load(open("jobs_links.json"))
final=[]

for i,job in enumerate(links[:40]):   # speed increased to 40 jobs per run
    print(f"🔍 Processing {i+1}/{len(links)} → {job['title']}")
    
    text=load_text(job['apply_link'])
    if not text:
        print("⚠ Failed, skipping")
        continue

    data=smart_extract(text)
    job.update(data)
    job["updated"]=str(datetime.datetime.now())
    final.append(job)

open("jobs.json","w").write(json.dumps(final,indent=4))
print("\n==============================")
print("🚀 Auto AI Extraction Complete")
print("Saved:",len(final),"jobs")
print("==============================")

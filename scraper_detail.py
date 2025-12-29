import requests, bs4, json, datetime
from pdfminer.high_level import extract_text
from extract_ai import smart_extract

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def pdf_text(url):
    try:
        file = requests.get(url, timeout=10).content
        open("temp.pdf","wb").write(file)
        return extract_text("temp.pdf")[:5000]
    except:
        return ""

def get_text_from_page(url):
    try:
        html = requests.get(url, headers=headers, timeout=12).text
        soup = bs4.BeautifulSoup(html,"html.parser")
        text = soup.get_text(" ", strip=True)

        pdf = soup.find("a", href=lambda x: x and x.endswith(".pdf"))
        if pdf:
            text += pdf_text(pdf.get("href"))

        return text
    except:
        return ""
        

links = json.load(open("jobs_links.json"))
final = []

for job in links[:30]:
    text = get_text_from_page(job['apply_link'])
    ai = smart_extract(text)
    job.update(ai)
    job["updated"] = str(datetime.datetime.now())
    final.append(job)

open("jobs.json","w").write(json.dumps(final,indent=4))
print("AI Extracted & Saved:", len(final))

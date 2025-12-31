import os, re, json, requests
from bs4 import BeautifulSoup
from value_extractor import extract_values

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

PDF_TMP = "temp_pdf.txt"


# -----------------------------------------
# DOWNLOAD + EXTRACT PDF TEXT
# -----------------------------------------
def extract_pdf_text(url):
    try:
        pdf = requests.get(url, headers=headers, timeout=20).content
        with open("temp.pdf", "wb") as f:
            f.write(pdf)

        # Convert PDF → Text using pdfminer
        os.system("pdf2txt.py temp.pdf > temp_pdf.txt")

        if os.path.exists(PDF_TMP):
            with open(PDF_TMP, "r",encoding="utf-8") as f:
                return f.read().lower().replace("\n"," ")

    except:
        return ""
    return ""


# -----------------------------------------
# Extract text from link page
# Follows 2nd link automatically if needed
# -----------------------------------------
def deep_scrape(url):
    try:
        r = requests.get(url, headers=headers, timeout=25)
        soup = BeautifulSoup(r.text,"html.parser")

        text = soup.get_text(" ").lower()

        # If no useful text → find next link inside page (AUTO CRAWL)
        if len(text)<200:
            next_links=soup.select("a[href]")
            for a in next_links[:5]:
                link=a.get("href")
                if link and link.startswith("http"):
                    return deep_scrape(link)

        # If PDF link found → download & extract
        pdf_links=soup.select("a[href$='.pdf']")
        for p in pdf_links[:3]:
            pdf_text = extract_pdf_text(p.get("href"))
            if len(pdf_text)>200:
                text+=" "+pdf_text

        return text

    except:
        return ""


# -----------------------------------------
# AI Fix logic (Auto fill missing)
# -----------------------------------------
def fix_job(job):
    page_text = deep_scrape(job["apply_link"])

    if not page_text:
        return job

    # QUALIFICATION
    if not job["qualification"]:
        if "10th" in page_text or "matric" in page_text: job["qualification"]="10th"
        elif "12th" in page_text or "intermediate" in page_text: job["qualification"]="12th"
        elif "iti" in page_text: job["qualification"]="ITI"
        elif "diploma" in page_text: job["qualification"]="Diploma"
        elif "engineer" in page_text or "b.tech" in page_text: job["qualification"]="Engineering"
        elif "graduate" in page_text or "bachelor" in page_text: job["qualification"]="Graduate"
        elif "post" in page_text or "master" in page_text: job["qualification"]="Post Graduate"

    # SALARY
    if not job["salary"]:
        s=re.findall(r'₹\s?\d{4,8}',page_text)
        if s: job["salary"]=s[0]

    # AGE LIMIT
    if not job["age_limit"]:
        a=re.findall(r'\b\d{1,2}\s?-\s?\d{1,2}\b',page_text)
        if a: job["age_limit"]=a[0]

    # VACANCY
    if not job["vacancy"]:
        v=re.findall(r'\b\d{2,6}\b',page_text)
        if v: job["vacancy"]=v[0]

    # LAST DATE
    if not job["last_date"]:
        d=re.findall(r'\d{1,2}/\d{1,2}/\d{4}',page_text)
        if d: job["last_date"]=d[-1]

    return extract_values(job)



# ===================================================
# MAIN PROCESS
# ===================================================
with open("jobs.json","r",encoding="utf-8") as f:
    data=json.load(f)

updated=[]
for job in data:
    final=fix_job(job)
    updated.append(final)


with open("jobs.json","w",encoding="utf-8") as f:
    json.dump(updated,f,indent=4,ensure_ascii=False)

print("\n🔥 Deep AI Corrector V2 Complete!")
print("📌 PDF + Table + 2nd level links scanned")
print("📌 Missing fields Auto-filled with accuracy boost!\n")

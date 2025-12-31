import requests, json, re
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

URLS = ["https://www.freejobalert.com/"]
jobs=[]

# ================== Home Page Job Links ==================
def scrape_homepage(url):
    r=requests.get(url,headers=headers,timeout=20)
    soup=BeautifulSoup(r.text,"html.parser")

    links=soup.select("a[href*='articles'],a[href*='recruit'],a[href*='online'],a[href*='posts']")
    print(f"Found {len(links)} raw links")

    for a in links[:60]:
        title=a.get_text(strip=True)
        link=a.get("href")

        if not link.startswith("http"):
            link=url+link
        
        jobs.append({
            "title":title,
            "apply_link":link,
            "qualification":"",
            "salary":"",
            "age_limit":"",
            "vacancy":"",
            "last_date":""
        })


# ================== Detail Page Extract ==================
def extract_qualification_from_page(text_block):
    patterns=[
        r"(matriculation[\w\s]*10th[\w\s]*pass)",
        r"(10th[\w\s]*pass)",
        r"(12th[\w\s]*pass)",
        r"(any graduate|graduate|bachelor['s]* degree)",
        r"(post graduate|master.degree|pg)",
        r"(diploma[\w\s]*engineering)",
        r"(iti[\w\s]*certificate)",
        r"(b\.sc[\w\s]*|bsc[\w\s]*)",
        r"(m\.sc[\w\s]*|msc[\w\s]*)",
        r"(b\.tech[\w\s]*|m\.tech[\w\s]*)",
        r"(mba[\w\s]*)",
        r"(phd[\w\s]*)"
    ]

    t=text_block.lower()

    for p in patterns:
        match=re.search(p,t)
        if match:
            return match.group(1).strip().title()

    return ""


def scrape_details():
    for job in jobs:
        try:
            r=requests.get(job["apply_link"],headers=headers,timeout=25)
            soup=BeautifulSoup(r.text,"html.parser")

            full_text=soup.get_text(" ",strip=True).lower()

            # ******** Qualification Auto Detect ********
            qual=extract_qualification_from_page(full_text)
            if qual: job["qualification"]=qual

            # Salary detect
            sal=re.findall(r"₹\s?\d{4,8}",full_text)
            if sal: job["salary"]=sal[0]

            # Age detection
            age=re.findall(r"\d{1,2}\s?-\s?\d{1,2}",full_text)
            if age: job["age_limit"]=age[0]

            # Vacancy
            vac=re.findall(r"\b\d{2,5}\b",full_text)
            if vac: job["vacancy"]=vac[0]

            # Last Date
            date=re.findall(r"\d{1,2}/\d{1,2}/\d{4}",full_text)
            if date: job["last_date"]=date[-1]

        except:
            print("skip:",job["title"])
            continue


# ================= Run =================
for site in URLS:
    scrape_homepage(site)

scrape_details()

unique={i["apply_link"]:i for i in jobs}
final=list(unique.values())

with open("jobs.json","w",encoding="utf-8") as f:
    json.dump(final,f,indent=4,ensure_ascii=False)

print("\n🚀 Stage-7 Smart Scraper Complete | Jobs:",len(final))

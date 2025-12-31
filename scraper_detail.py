import requests, json, re
from bs4 import BeautifulSoup
from value_extractor import extract_values

headers={
 "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

URLS=["https://www.freejobalert.com/"]
jobs=[]


# ===========================
# Step-1 : Homepage → Job Links
# ===========================
def scrape_homepage(url):
    r=requests.get(url,headers=headers)
    soup=BeautifulSoup(r.text,"html.parser")

    links=soup.select("a[href*='articles'],a[href*='online'],a[href*='recruit']")
    print(f"\n⚡ Job links Found:",len(links))

    for a in links[:30]:
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


# ===========================
# Step-2 : Detail Page Data Extraction
# ===========================
def scrape_details():
    for job in jobs:
        try:
            r=requests.get(job["apply_link"],headers=headers,timeout=15)
            text=BeautifulSoup(r.text,"html.parser").get_text(" ").lower()

            job["salary"]= re.findall(r'₹?\s?\d{4,7}',text)[0] if re.findall(r'₹?\s?\d{4,7}',text) else ""
            job["age_limit"]= re.findall(r'\d{1,2}\s?-\s?\d{1,2}',text)[0] if re.findall(r'\d{1,2}\s?-\s?\d{1,2}',text) else ""
            job["vacancy"] = re.findall(r'\b\d{2,5}\b',text)[0] if re.findall(r'\b\d{2,5}\b',text) else ""
            job["last_date"]= re.findall(r'\d{1,2}/\d{1,2}/\d{4}',text)[0] if re.findall(r'\d{1,2}/\d{1,2}/\d{4}',text) else ""
            job["qualification"]= extract_values({"qualification":text})["qualification"]

        except:
            pass


# ===========================
# RUN
# ===========================
for site in URLS:
    scrape_homepage(site)

scrape_details()

# Final filtering
clean=[]
for j in jobs:
    j=extract_values(j)
    if j["title"]!="" and (j["qualification"]!="" or j["salary"]!="" or j["vacancy"]!=""):
        clean.append(j)

with open("jobs.json","w",encoding="utf-8") as f:
    json.dump(clean,f,indent=4,ensure_ascii=False)

print("\n🎉 Scraping Completed + Cleaned")
print("📌 jobs.json now contains structured filtered job data 🔥")
print("Next Step → Multi-Page / More Sites / Auto Push 🚀")

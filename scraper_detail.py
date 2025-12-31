import requests, json, re
from bs4 import BeautifulSoup
from value_extractor import extract_values   # 🔥 auto clean + extract layer

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}

URLS = ["https://www.freejobalert.com/"]

jobs = []

# -------- Step 1: Extract titles & links --------
def scrape_homepage(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    
    links = soup.select("a[href*='articles'],a[href*='recruit'],a[href*='online'],a[href*='posts']")
    print(f"Found {len(links)} Job Leads ⚡")

    for a in links[:25]:
        title = a.get_text(strip=True)
        link = a.get("href")

        if not link.startswith("http"):
            link = url + link

        jobs.append({
            "title": title,
            "apply_link": link,
            "qualification": "",
            "salary": "",
            "age_limit": "",
            "vacancy": "",
            "last_date": ""
        })


# -------- Step 2: Fetch details from each job page --------
def scrape_details():
    for job in jobs:
        try:
            r = requests.get(job["apply_link"], headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")

            text = soup.get_text(separator=" ").lower()

            # regex extraction
            job["salary"] = re.findall(r'₹?\s?\d{4,7}', text)[0] if re.findall(r'₹?\s?\d{4,7}', text) else ""
            job["age_limit"] = re.findall(r'\d{1,2}\s?-\s?\d{1,2}', text)[0] if re.findall(r'\d{1,2}\s?-\s?\d{1,2}', text) else ""
            job["vacancy"] = re.findall(r'\b\d{2,5}\b', text)[0] if re.findall(r'\b\d{2,5}\b', text) else ""
            job["last_date"] = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text)[0] if re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text) else ""
            job["qualification"] = extract_values({"qualification": text}).get("qualification","")
        
        except:
            continue


# -------- RUN --------
for site in URLS:
    scrape_homepage(site)

scrape_details()

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=4, ensure_ascii=False)

print("\n🎉 Stage-2 Complete")
print("📌 Now jobs.json will have salary / age / vacancy / last date fields")
print("Next Step → AI Post Verification + Auto Filtering + Daily Cron Feed 🚀")

# ======================= Stage-5 Multi Page Scraper 🚀 =======================
import requests, json, re, time
from bs4 import BeautifulSoup
from value_extractor import extract_values

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

BASE = "https://www.freejobalert.com/"
jobs = []


# ------------------------ PAGE SCRAPER (auto pagination) ------------------------
def scrape_page(url):
    print(f"[Page] → {url}")
    try:
        r = requests.get(url, headers=headers, timeout=25)
    except:
        print("Failed:", url)
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    
    # job article links
    links = soup.select("a[href*='articles'],a[href*='recruit'],a[href*='online'],a[href*='posts']")
    print("Links found:", len(links))

    for a in links[:60]:  # limit for safe
        title = a.get_text(strip=True)
        link = a.get("href")

        if not link.startswith("http"):   # relative to full
            link = BASE + link.lstrip("/")

        jobs.append({
            "title": title,
            "apply_link": link,
            "qualification": "",
            "salary": "",
            "age_limit": "",
            "vacancy": "",
            "last_date": ""
        })

    # ------------ Detect next/older button for pagination ------------
    nxt = soup.find("a", string=re.compile("Next|Older|»|›", re.I))
    if nxt:
        next_url = nxt.get("href")
        if not next_url.startswith("http"):
            next_url = BASE + next_url.lstrip("/")
        time.sleep(2)
        scrape_page(next_url)  # Recursive auto next page scan


# ------------------------- Extract job details deeply -------------------------
def scrape_details():
    for job in jobs:
        try:
            r = requests.get(job["apply_link"], headers=headers, timeout=25)
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text(" ").lower()

            # Basic extraction (initial)
            job["salary"] = re.findall(r'₹\s?\d{4,8}|pay\s*level\s*\d+', text)[0] if re.findall(r'₹\s?\d{4,8}|pay\s*level\s*\d+', text) else ""
            job["age_limit"] = re.findall(r'\d{1,2}\s?to\s?\d{1,2}|\d{1,2}-\d{1,2}', text)[0] if re.findall(r'\d{1,2}\s?to\s?\d{1,2}|\d{1,2}-\d{1,2}', text) else ""
            job["vacancy"] = re.findall(r'\b\d{2,5}\b', text)[0] if re.findall(r'\b\d{2,5}\b', text) else ""
            job["last_date"] = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text)[0] if re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text) else ""

            # AI based structure fix
            job.update(extract_values(job))

        except Exception as e:
            print("Skip:", job["title"][:30], "Reason:", e)
            continue


# ============================ RUN PROCESS =============================

print("\n🚀 Stage-5 Scraper Started — Multi-Page + Smart Extractor\n")

scrape_page(BASE)
scrape_details()

# remove duplicate
unique = {j["apply_link"]: j for j in jobs}
final = list(unique.values())

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(final, f, indent=4, ensure_ascii=False)

print("\n🔥 Stage-5 Complete: Multi-Page Scanning Done")
print("Total Jobs Saved:", len(final))
print("\nNext Step → AI Trainer + Corrector auto run in pipeline\n")

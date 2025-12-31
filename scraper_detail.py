import requests, json, re
from bs4 import BeautifulSoup
from value_extractor import extract_values   # Auto cleaner + structured output

# =======================
# Request Headers
# =======================
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# =======================
# Target Websites
# =======================
URLS = [
    "https://www.freejobalert.com/"
]

jobs_raw = []
jobs_clean = []


# --------------------------------------------------
# Step 1 → Homepage links collector
# --------------------------------------------------
def scrape_homepage(url):
    print(f"\n🌍 Scanning Homepage → {url}")

    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.select("a[href*='articles'],a[href*='recruit'],a[href*='form'],a[href*='post']")
    print(f"🔗 Links found: {len(links)}")

    for a in links[:50]:   # limit safe
        title = a.get_text(strip=True)
        link = a.get("href")

        if not link.startswith("http"):
            link = url + link

        jobs_raw.append({
            "title": title,
            "apply_link": link,
            "qualification": "",
            "salary": "",
            "age_limit": "",
            "vacancy": "",
            "last_date": ""
        })


# --------------------------------------------------
# Step 2 → Job detail page extraction
# --------------------------------------------------
def scrape_details():
    print("\n📄 Extracting job details...")

    for job in jobs_raw:
        try:
            r = requests.get(job["apply_link"], headers=headers, timeout=25)
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text(" ", strip=True).lower()

            # Smart regex extraction
            salary = re.findall(r'(₹\s?\d{4,7}|rs\.?\s?\d+|pay\s*scale\s*\d+)', text)
            age = re.findall(r'(\d{1,2}\s?-\s?\d{1,2})', text)
            vacancy = re.findall(r'\b\d{2,5}\b', text)
            last_date = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text)
            qualification = re.findall(r'(10th|12th|iti|diploma|graduate|b\.sc|ba|bsc|mba|engineering)', text)

            job["salary"] = salary[0] if salary else ""
            job["age_limit"] = age[0] if age else ""
            job["vacancy"] = vacancy[0] if vacancy else ""
            job["last_date"] = last_date[0] if last_date else ""
            job["qualification"] = qualification[0] if qualification else ""

            # Final cleaning layer before saving
            cleaned = extract_values(job)

            # only valid titles saved
            if cleaned["title"] != "":
                jobs_clean.append(cleaned)

        except Exception as e:
            print("❌ Error fetching:", job["apply_link"], "|", e)
            continue


# --------------------------------------------------
# RUN Engine
# --------------------------------------------------
for url in URLS:
    scrape_homepage(url)

scrape_details()

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs_clean, f, indent=4, ensure_ascii=False)

print("\n🎉 Successfully Scraped + Cleaned")
print("📂 Output saved in → jobs.json")
print("🚀 Next— Auto Multi-Site + Pagination Mode coming")

import requests, json, re
from bs4 import BeautifulSoup
from value_extractor import extract_values

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

URLS = ["https://www.freejobalert.com/"]
jobs = []

# Step-1: find job links
def scrape_homepage(url):
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.select("a[href*='articles'],a[href*='recruit'],a[href*='online'],a[href*='posts']")
    print(f"Found {len(links)} raw links")

    for a in links[:50]:
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


# Step-2: deep extract each job page
def scrape_details():
    for job in jobs:
        try:
            r = requests.get(job["apply_link"], headers=headers, timeout=25)
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text(separator=" ").lower()

            job["salary"] = re.findall(r'₹\s?\d{4,8}|pay\s*level\s*\d+', text)[0] if re.findall(r'₹\s?\d{4,8}|pay\s*level\s*\d+', text) else ""
            job["age_limit"] = re.findall(r'\d{1,2}\s?to\s?\d{1,2}|\d{1,2}-\d{1,2}', text)[0] if re.findall(r'\d{1,2}\s?to\s?\d{1,2}|\d{1,2}-\d{1,2}', text) else ""
            job["vacancy"] = re.findall(r'\b\d{2,5}\b', text)[0] if re.findall(r'\b\d{2,5}\b', text) else ""
            job["last_date"] = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text)[0] if re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text) else ""

            details = extract_values(job)
            job.update(details)

        except Exception as e:
            print("skip:", job["title"])
            continue


# Run
for site in URLS:
    scrape_homepage(site)

scrape_details()

# remove duplicates
unique = {i["apply_link"]: i for i in jobs}
final = list(unique.values())

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(final, f, indent=4, ensure_ascii=False)

print("\n🚀 Smart Scraper Stage-3 Complete\nJobs saved:", len(final))

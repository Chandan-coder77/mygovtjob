import requests, json, re
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}

URLS = [
    "https://www.freejobalert.com/",
]

jobs = []

def scrape_fja(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # Find all job links
    links = soup.select("a[href*='recruit'], a[href*='form'], a[href*='notification'], a[href*='vacancy'], a[href*='online']")

    print(f"Found {len(links)} Job Leads 🔍")

    for a in links[:30]:  # limit 30 results per run
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

for site in URLS:
    scrape_fja(site)

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=4, ensure_ascii=False)

print("\n✅ Stage-1 Completed: Job Titles + Links Extracted")
print("Next Step → Fetch job details page to extract salary/age/date")

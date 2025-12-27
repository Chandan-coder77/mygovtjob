import json, requests, bs4, datetime

print("\n🔎 Fetching Latest Govt Jobs From FreeJobAlert...\n")

URL = "https://www.freejobalert.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

try:
    html = requests.get(URL, headers=headers, timeout=20).text
except Exception as e:
    print("❌ Fetch Error:", e)
    exit()

soup = bs4.BeautifulSoup(html,"html.parser")

jobs=[]

#  🔥 Top 10 latest headings scrape
for a in soup.select("a")[:10]:
    title=a.get_text(strip=True)
    link=a.get("href")
    if len(title)>5 and link and "http" in link:
        jobs.append({
            "title": title,
            "vacancies": "Updating...",
            "qualification": "Check Notification",
            "age": "18+",
            "salary": "Govt Rules",
            "last_date": "Updating...",
            "state": "India",
            "category": "Latest",
            "apply_link": link
        })

# Save to jobs.json
open("jobs.json","w").write(json.dumps(jobs,indent=4))

print(f"📁 Jobs Scraped: {len(jobs)}")
print("⏳ Last Update:", datetime.datetime.now())
print("✔ Auto Update Complete\n")

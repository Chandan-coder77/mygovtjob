import json, requests, bs4, datetime

print("\n🚀 Smart Job Scraper Running...\n")

URL = "https://www.freejobalert.com/latest-notifications/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

try:
    html = requests.get(URL, headers=headers, timeout=20).text
except:
    print("❌ Website Not Responding")
    exit()

soup = bs4.BeautifulSoup(html, "html.parser")

jobs=[]

rows = soup.select("table tr")[1:10]   # top 10 jobs

for r in rows:
    data = [x.get_text(strip=True) for x in r.select("td")]
    links = r.select_one("a")["href"] if r.select_one("a") else URL

    if len(data) >= 3:
        job={
            "title": data[0],
            "vacancies": data[1] if data[1] else "Updating...",
            "qualification": "Check Notification",
            "age": "18+",
            "salary": "As per Govt Rules",
            "last_date": data[2] if data[2] else "Updating...",
            "state": "India",
            "category": "Latest",
            "apply_link": links
        }

        jobs.append(job)

open("jobs.json","w").write(json.dumps(jobs,indent=4))

print("📁 Jobs Fetched:",len(jobs))
print("⏳ Updated:",datetime.datetime.now())
print("✔ Done\n")

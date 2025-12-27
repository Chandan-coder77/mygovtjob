import requests, json, bs4, datetime

print("\n🚀 Smart Job Scraper Running...\n")

URL = "https://www.sarkariresult.com/latestjobs/"   # Reliable job listing
html = requests.get(URL, timeout=15).text
soup = bs4.BeautifulSoup(html,"html.parser")

jobs = []

for row in soup.select("ul li a")[:15]:   # Top 15 jobs
    title = row.get_text(strip=True)
    link = row.get("href")
    if not link.startswith("http"):
        link = "https://www.sarkariresult.com" + link

    jobs.append({
        "title": title,
        "vacancies": "Updating...",
        "qualification": "Check Notice",
        "age": "18+",
        "salary": "Govt Rules",
        "last_date": "Updating...",
        "state": "India",
        "category": "Govt Job",
        "apply_link": link
    })

open("jobs.json", "w").write(json.dumps(jobs, indent=4))

print(f"\n📁 Jobs Fetched: {len(jobs)}")
print("⏳ Updated:",datetime.datetime.now())
print("✔ Saved to jobs.json\n")

import requests, json, bs4, datetime

print("\n🚀 Auto Smart Govt Job Scraper Started...\n")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

URL = "https://www.freejobalert.com/latest-notification/"

try:
    r = requests.get(URL, headers=headers, timeout=25)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, "html.parser")
except Exception as e:
    print("❌ Fetch Failed:", e)
    exit()

jobs = []

# 🔥 Extract Real Latest Govt Job Notifications
for row in soup.select(".wpsm_recent_posts_list li")[:25]:  # 25 latest jobs
    title = row.get_text(strip=True)
    link = row.find("a")["href"]

    if not link.startswith("http"):
        link = "https://www.freejobalert.com" + link

    jobs.append({
        "title": title,
        "vacancies": "Updating...",
        "qualification": "Check Notification",
        "age": "18+",
        "salary": "As per Govt Rules",
        "last_date": "Updating...",
        "state": "India",
        "category": "Latest",
        "apply_link": link
    })

# Save ✔
open("jobs.json","w").write(json.dumps(jobs,indent=4))

print(f"📄 Total Jobs Fetched: {len(jobs)}")
print("🕒 Updated:", datetime.datetime.now())
print("✔ Job Auto-Update Successful\n")

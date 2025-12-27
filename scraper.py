import requests, json, bs4, datetime

print("\n🚀 Debug Scraper Started...\n")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

URL = "https://www.freejobalert.com/latest-notification/"

try:
    r = requests.get(URL, headers=headers, timeout=25)
    r.raise_for_status()
    print("🌍 Website Connected Successfully")
except Exception as e:
    print("❌ Connection Failed:", e)
    exit()

soup = bs4.BeautifulSoup(r.text, "html.parser")

# Debug: print top 200 chars
print("\n🔍 Sample HTML Received:\n", r.text[:500], "\n------")

jobs = []

# Testing selector
posts = soup.select(".wpsm_recent_posts_list li")

print(f"📌 Found Posts Count: {len(posts)}")

for p in posts[:10]:
    title = p.get_text(strip=True)
    link = p.find("a")["href"] if p.find("a") else "No Link"
    print("🟢 Job:", title)

    jobs.append({
        "title": title,
        "vacancies":"Updating...",
        "qualification":"Check Notification",
        "age":"18+",
        "salary":"Govt Rules",
        "last_date":"Updating...",
        "state":"India",
        "category":"Latest",
        "apply_link": link
    })

open("jobs.json","w").write(json.dumps(jobs,indent=4))
print("\n📁 JOBS SAVED:", len(jobs))
print("⏳ Updated:", datetime.datetime.now())
print("✔ Debug Completed\n")

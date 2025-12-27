import requests, json, bs4, datetime

print("\n🚀 Smart Job Auto-Update Started...\n")

# ---------- Full Strong Header (prevent block) ----------
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

URL = "https://www.freejobalert.com/latest-notification/"

# ------------ Fetch Website Data ------------
try:
    response = requests.get(URL, headers=headers, timeout=25)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, "html.parser")
except Exception as e:
    print("❌ Error while fetching website:", e)
    exit()

# ------------ Scrap Latest Job List ------------
jobs = []

for row in soup.select("ul li a")[:20]:   # top 20 job posts
    title = row.get_text(strip=True)
    link = row.get("href")

    # complete relative URL fix
    if not link.startswith("http"):
        link = "https://www.freejobalert.com/" + link

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

# ------------ Save in jobs.json ------------
open("jobs.json", "w").write(json.dumps(jobs, indent=4))

print(f"📁 Total Jobs Added: {len(jobs)}")
print("⏳ Updated:", datetime.datetime.now())
print("✔ Auto Update Successfully Completed\n")

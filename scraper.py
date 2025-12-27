import json, requests, bs4, datetime

print("\n🚀 Smart Scraper 2.0 Running...\n")

URL = "https://www.freejobalert.com/latest-notifications/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

html = requests.get(URL, headers=headers, timeout=20).text
soup = bs4.BeautifulSoup(html, "html.parser")

jobs=[]

rows = soup.select("table tr")[1:15]   # 15 jobs fetch

for r in rows:
    td = [x.get_text(strip=True) for x in r.select("td")]
    link = r.select_one("a")["href"] if r.select_one("a") else URL

    if len(td)>=3:
        date = td[0]            # 26/12/2025
        org = td[1]             # Latur DCC Bank
        post = td[2]            # Clerk – 375 Posts / etc

        job={
            "title": f"{org} Recruitment {date}",          # Clean Title
            "vacancies": post.replace("–","-"),            # Clean vacancy
            "qualification": "Check Official Notification",
            "age": "18+",
            "salary": "As per Govt Rules",
            "last_date": date,
            "state": "India",
            "category": "Latest",
            "apply_link": link
        }

        jobs.append(job)

open("jobs.json","w").write(json.dumps(jobs,indent=4))

print(f"📄 Total Jobs Saved: {len(jobs)}")
print("⏳ Updated:",datetime.datetime.now())
print("🔥 All Good!")

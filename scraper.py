import requests, json, bs4, datetime

print("\n🚀 Govt Job Auto Scraper Running...\n")

sources = {
    "SSC":"https://ssc.nic.in/portal/notifications",
    "UPSC":"https://upsc.gov.in/recruitment",
    "Railway":"https://indianrailways.gov.in/railwayboard/view_section.jsp?id=0,7,2158",
    "IBPS":"https://www.ibps.in/",
    "NCS":"https://www.ncs.gov.in/"
}

jobs = []

for cat, url in sources.items():
    try:
        print(f"🔎 Scraping {cat}: {url}")
        soup = bs4.BeautifulSoup(requests.get(url,timeout=10).text,"html.parser")

        # Most sites use links <a> for job notices
        for link in soup.find_all("a")[:10]:
            title = link.get_text(strip=True)

            if len(title) < 10:   # Avoid junk text
                continue

            jobs.append({
                "title": title,
                "vacancies": "Updating...",
                "qualification": "Check Official Notice",
                "age": "18+",
                "salary": "As per Govt Rules",
                "last_date": "Updating...",
                "state": "India",
                "category": cat,
                "apply_link": url
            })

    except Exception as e:
        print(f"❌ Failed {cat} → {e}")

open("jobs.json","w").write(json.dumps(jobs,indent=4))

print(f"\n📁 Total Jobs Fetched: {len(jobs)}")
print("⏳ Last Update:",datetime.datetime.now())
print("✔ Saved Successfully\n")

import requests, json, bs4, datetime

print("\n🚀 Auto Job Scraper Running...\n")

sites = {
    "SSC":"https://ssc.nic.in/",
    "UPSC":"https://upsconline.nic.in/",
    "Railway":"https://indianrailways.gov.in/",
    "Banking":"https://ibps.in/",
    "NCS":"https://www.ncs.gov.in/"
}

jobs = []

for category, url in sites.items():
    try:
        print(f"🔎 Fetching {category} – {url}")
        r = requests.get(url, timeout=10)
        soup = bs4.BeautifulSoup(r.text, "html.parser")

        for h in soup.find_all(["h1","h2","h3"])[:4]:  # हर साइट से 4 titles
            title = h.get_text(strip=True)

            if len(title) < 5: 
                continue

            jobs.append({
                "title": title,
                "vacancies":"Updating...",
                "qualification":"Check Official Notice",
                "age":"18+",
                "salary":"As per Govt Rules",
                "last_date":"Updating...",
                "state":"India",
                "category": category,
                "apply_link": url
            })

    except Exception as e:
        print(f"❌ Failed on {url}: {e}")

# save
open("jobs.json","w").write(json.dumps(jobs, indent=4))
print("\n📁 Total Jobs Fetched:", len(jobs))
print("⏳ Last Run:", datetime.datetime.now())
print("✔ Saved to jobs.json\n")

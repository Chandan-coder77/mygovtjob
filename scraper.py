import requests, json, bs4, datetime

print("\n🚀 Smart Job Scraper Running...\n")

# Pages where real recruitments are published
sources = {
    "SSC": "https://ssc.nic.in/Portal/Notices",
    "UPSC": "https://upsc.gov.in/recruitment/recruitment",
    "Railway": "https://indianrailways.gov.in/",
    "IBPS": "https://www.ibps.in/crp-specialist-officers-xiii/",
    "NCS": "https://www.ncs.gov.in/job-seeker/jobsearch"
}

all_jobs = []

def extract_jobs(url, category):
    print(f"🔎 Checking {category}... {url}")

    try:
        soup = bs4.BeautifulSoup(requests.get(url, timeout=15).text, "html.parser")

        jobs_found = 0

        for a in soup.find_all("a"):
            title = a.get_text(strip=True)

            # VALID Job Title Filter (no skip)
            if len(title) < 12: 
                continue
            if any(x in title.lower() for x in ["login", "home", "content", "about", "privacy", "faq"]):
                continue

            all_jobs.append({
                "title": title,
                "vacancies": "Updating...",
                "qualification": "Check Official Notice",
                "age": "18+",
                "salary": "As per Govt Rules",
                "last_date": "Updating...",
                "state": "India",
                "category": category,
                "apply_link": url
            })

            jobs_found += 1
            if jobs_found >= 10: break   # limit per source

    except Exception as e:
        print(f"❌ Failed {category}: {e}")

# Run for all websites
for cat, link in sources.items():
    extract_jobs(link, cat)

open("jobs.json","w").write(json.dumps(all_jobs, indent=4))

print(f"\n📁 Total Jobs Scraped: {len(all_jobs)}")
print("⏳ Updated:", datetime.datetime.now())
print("✔ Stored in jobs.json\n")

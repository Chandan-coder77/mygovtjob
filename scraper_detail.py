import json, re, requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

job_sites = [
    "https://www.freejobalert.com/",
    "https://www.sarkariresult.com/",
    "https://www.sarkariprep.in/"
]

def extract_block(text):
    blocks = re.split(r'Notification|Recruitment|Apply|Vacancy|Post', text, flags=re.I)
    results = []

    for b in blocks:
        job = {}

        title = re.search(r'([A-Za-z ]{5,50})', b)
        if title:
            job["title"] = title.group().strip()

        q = re.search(r'(10th|12th|ITI|Diploma|Graduate|BA|B\.?Sc|Engineering|MBA)', b, re.I)
        if q:
            job["qualification"] = q.group()

        sal = re.search(r'₹?\s?\d{4,7}', b)
        if sal:
            job["salary"] = sal.group()

        age = re.search(r'\d{1,2}\s?-\s?\d{1,2}', b)
        if age:
            job["age_limit"] = age.group()

        vac = re.search(r'\d{1,4}\s?(Post|Vacancy)', b, re.I)
        if vac:
            job["vacancy"] = re.findall(r'\d{1,4}', vac.group())[0]

        date = re.search(r'\d{1,2}/\d{1,2}/\d{4}', b)
        if date:
            job["last_date"] = date.group()

        if len(job) > 1:
            results.append(job)

    return results


all_jobs = []

for site in job_sites:
    print("\n🌍 Scraping:", site)
    try:
        r = requests.get(site, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.get_text(" ").replace("\n", " ")
        jobs = extract_block(text)

        for j in jobs:
            j["apply_link"] = site

        all_jobs.extend(jobs)

        print(f"✔ Found {len(jobs)} jobs")

    except Exception as e:
        print("❌ Error:", e)

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=4, ensure_ascii=False)

print("\n✅ Smart Scraper Complete – jobs.json updated successfully")

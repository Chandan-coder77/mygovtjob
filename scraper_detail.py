import json, requests, re
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# Job main pages
job_sites = [
    "https://www.freejobalert.com/",
    "https://www.sarkariprep.in/",
    "https://www.sarkariresult.com/"
]

# Smart extract functions
def find(pattern, text):
    result = re.findall(pattern, text, flags=re.I)
    return result[0] if result else ""

def extract_job_blocks(soup):
    """Try to detect job blocks automatically"""
    blocks = soup.find_all(["li","div","article","tr","p"], limit=30)  # top 30 only
    return [b.get_text(" ", strip=True) for b in blocks]

# Master scraping engine
all_jobs = []

for site in job_sites:
    print(f"\n🌍 Fetching → {site}")

    try:
        r = requests.get(site, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text,"html.parser")

        blocks = extract_job_blocks(soup)

        for blk in blocks:

            job = {
                "title": blk[:45],  # first 45 chars
                "qualification": find(r"(10th|12th|BA|B\.?Sc|B\.?Com|Graduate|ITI|Diploma|MBA|Engineering)", blk),
                "salary": find(r"₹\s?\d{4,7}", blk) or find(r"\d+\.?\d*\s*LPA", blk),
                "age_limit": find(r"\d{1,2}\s?-\s?\d{1,2}", blk),
                "vacancy": find(r"\b\d{1,4}\b", blk),
                "last_date": find(r"\d{1,2}/\d{1,2}/\d{4}", blk),
                "apply_link": site   # BASE SITE (later we will scrape actual post link)
            }

            # Skip empty jobs
            if job["qualification"] or job["salary"] or job["last_date"]:
                all_jobs.append(job)

        print(f"✔ Extracted {len(all_jobs)} total jobs till now")

    except Exception as e:
        print("❌ Error:", e)

# Save to jobs.json
with open("jobs.json","w",encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=4, ensure_ascii=False)

print("\n🚀 JOB DATA SAVED TO jobs.json")
print(f"📌 Total Jobs Stored → {len(all_jobs)}")

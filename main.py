# main.py
# -------------------------
# Runs the scraper and updates jobs.json
# Make sure scraper.py contains function => scrape_freejobalert()
# -------------------------

import json
from scraper import scrape_freejobalert   # must match function name in scraper.py

def save_jobs(data, file="jobs.json"):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    print("\n🚀 Running Government Job Scraper...\n")

    jobs = scrape_freejobalert()   # <-- call scraper
    save_jobs(jobs)

    print(f"✔ Jobs updated successfully! Total Jobs: {len(jobs)}\n")

if __name__ == "__main__":
    main()

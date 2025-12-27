import json, os
from scraper import scrape

jobs_file = "jobs.json"
sources_file = "sources.txt"

def load_sources():
    if not os.path.exists(sources_file):
        print("❌ sources.txt missing — Add job URLs inside sources.txt")
        return []
    with open(sources_file, "r") as file:
        return [l.strip() for l in file if l.strip()]

def load_old_jobs():
    return json.load(open(jobs_file)) if os.path.exists(jobs_file) else []

def save_jobs(data):
    with open(jobs_file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    print("\n🚀 Auto Job Scraper Running...\n")
    sites = load_sources()
    old = load_old_jobs()
    new = []

    for url in sites:
        print("🔍 Checking:", url)
        jobs = scrape(url)
        new.extend(jobs)

    # remove duplicates by title
    final = []
    titles = set()

    for job in new + old:
        if job["title"] not in titles and job["qualification"] != "Updating Soon":
            titles.add(job["title"])
            final.append(job)

    save_jobs(final)
    print("✔ Updated Successfully | Total Jobs:", len(final))

if __name__ == "__main__":
    main()

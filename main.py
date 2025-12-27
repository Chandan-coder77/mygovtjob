import json, os
from scraper import scrape

jobs_file = "jobs.json"
sources_file = "sources.txt"

def load_sources():
    with open(sources_file, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def load_old_jobs():
    if not os.path.exists(jobs_file):
        return []
    with open(jobs_file, "r") as file:
        return json.load(file)

def save_jobs(data):
    with open(jobs_file, "w") as file:
        json.dump(data, file, indent=4)

def main():
    print("\n🚀 Running AI Job Scraper...\n")
    sources = load_sources()
    old_jobs = load_old_jobs()
    new_jobs = []

    for url in sources:
        new_jobs.extend(scrape(url))

    titles = set()
    final = []

    for job in new_jobs + old_jobs:
        if job["title"] not in titles and "Not Available" not in job["qualification"]:
            titles.add(job["title"])
            final.append(job)

    save_jobs(final)
    print("✔ Jobs updated successfully! Total:", len(final))

if __name__ == "__main__":
    main()

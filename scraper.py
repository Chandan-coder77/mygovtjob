import json, os, requests
from bs4 import BeautifulSoup

# ---------------------------
# Output file path
# ---------------------------
FILE = "jobs.json"

def scrape(url):
    print("Scraping:", url)

    r = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    })

    soup = BeautifulSoup(r.text, "lxml")
    jobs = []

    cards = soup.select(".jobsearch-card, .card, article")  # generic selectors

    for job in cards:
        title = job.select_one("h2, h3, .title, .job-title")
        vacancy = job.text.lower().replace("vacancy", "").replace("vacancies", "")
        qualification = job.text if "Qualification" in job.text else "Not Available"
        salary = job.text if "Salary" in job.text else "Not Available"
        last_date = job.text if "Last Date" in job.text else "Not Available"
        link = job.select_one("a")

        jobs.append({
            "title": title.get_text(strip=True) if title else "No Title",
            "vacancies": vacancy[:40],
            "qualification": qualification[:300],
            "salary": salary[:150],
            "last_date": last_date[:150],
            "apply_link": link["href"] if link else url,
            "source": url
        })

    return jobs


def save_jobs(new_data):

    old = []
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                old = json.load(f)
        except:
            old = []

    # remove duplicate titles
    final = {job["title"]: job for job in (old + new_data)}
    final = list(final.values())

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(final)} jobs")


if __name__ == "__main__":

    if not os.path.exists("sources.txt"):
        print("Create sources.txt and add job website links")
        exit()

    urls = open("sources.txt").read().splitlines()
    all_data = []

    for url in urls:
        all_data += scrape(url)

    save_jobs(all_data)
    print("Scraping completed successfully.")

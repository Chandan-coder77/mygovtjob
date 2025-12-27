import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive"
}

def clean(text):
    return text.replace("\n"," ").replace("\t"," ").strip()

def scrape_freejobalert():
    url = "https://www.freejobalert.com/"
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []
    sections = soup.select("section")  # major blocks पकड़ने की trick

    for sec in sections:
        title = sec.find("h2")
        if not title: 
            continue

        # Table extract block
        table = sec.find("table")
        if not table:
            continue

        rows = table.find_all("tr")[1:]  # skip headers

        for row in rows:
            cols = row.find_all(["td","th"])
            if len(cols) < 4:
                continue

            job = {
                "title": clean(cols[1].text if len(cols)>1 else "N/A"),
                "vacancies": clean(cols[2].text if len(cols)>2 else "N/A"),
                "qualification": clean(cols[3].text if len(cols)>3 else "N/A"),
                "salary": "N/A",   # salary आगे pdf से आएगी
                "age_limit": "N/A",
                "last_date": clean(cols[-1].text),
                "apply_link": cols[1].find("a")["href"] if cols[1].find("a") else url,
                "source": "https://www.freejobalert.com/"
            }
            # Skip old or invalid
            if job["vacancies"]=="N/A" and job["qualification"]=="N/A":
                continue

            jobs.append(job)

    return jobs


def save_data(data):
    with open("jobs.json","w",encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)
    print("jobs.json updated successfully ✔")


if __name__ == "__main__":
    print("Scraping started...")
    all_jobs = scrape_freejobalert()
    save_data(all_jobs)
    print("Total Jobs Fetched:", len(all_jobs))

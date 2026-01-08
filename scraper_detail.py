import requests, json, time, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

SOURCE_FILE = "trusted_sources.json"
OUTPUT_FILE = "jobs.json"

def clean(text):
    return " ".join(text.split())

def load_sources():
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_existing_jobs():
    if not os.path.exists(OUTPUT_FILE):
        return []
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

def is_probable_job_link(text, href):
    text = text.lower()
    href = href.lower()

    keywords = [
        "recruitment", "apply", "vacancy", "posts",
        "notification", "career", "employment"
    ]

    return any(k in text for k in keywords) or any(k in href for k in keywords)

def process():
    sources = load_sources()
    existing_jobs = load_existing_jobs()
    seen_links = {job.get("apply_link") for job in existing_jobs}

    new_jobs = []

    for source in sources:
        url = source["url"]
        scope = source.get("scope", "ALL")

        print(f"🔍 Scraping: {url}")

        try:
            r = requests.get(url, headers=HEADERS, timeout=25)
            soup = BeautifulSoup(r.text, "html.parser")
            base = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(url))

            for a in soup.find_all("a", href=True):
                title = clean(a.get_text())
                if not title or len(title) < 6:
                    continue

                link = urljoin(base, a["href"])

                if link in seen_links:
                    continue

                if not is_probable_job_link(title, link):
                    continue

                job = {
                    "title": title,
                    "apply_link": link,
                    "qualification": "",
                    "salary": "",
                    "age_limit": "",
                    "vacancy": "",
                    "last_date": "",
                    "source": url,
                    "scope": scope,
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                new_jobs.append(job)
                seen_links.add(link)

                print(f"✅ FOUND: {title}")

        except Exception as e:
            print(f"⚠ Error at {url}: {e}")

        time.sleep(1)

    final_jobs = existing_jobs + new_jobs

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_jobs, f, indent=2, ensure_ascii=False)

    print("\n🔥 SCRAPER DONE")
    print(f"➕ New jobs added: {len(new_jobs)}")
    print(f"📦 Total jobs now : {len(final_jobs)}")

if __name__ == "__main__":
    process()

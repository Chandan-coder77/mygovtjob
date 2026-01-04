import requests, json, re, time, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "jobs.json"

KEYWORDS = [
    "recruitment", "online form", "vacancy",
    "apply", "posts", "notification"
]

BLOCK_WORDS = [
    "result", "cutoff", "answer key",
    "admit card", "syllabus", "exam"
]

def clean(text):
    return re.sub(r"\s+", " ", text).strip()

def is_job_title(title):
    t = title.lower()
    if any(b in t for b in BLOCK_WORDS):
        return False
    return any(k in t for k in KEYWORDS)

def process():
    jobs = []
    seen = set()

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        sources = [x.strip() for x in f if x.strip().startswith("http")]

    for source in sources:
        print(f"🔍 Checking {source}")
        try:
            r = requests.get(source, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")
            base = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(source))

            for a in soup.find_all("a", href=True):
                title = clean(a.get_text())
                if not title:
                    continue

                if not is_job_title(title):
                    continue

                link = urljoin(base, a["href"])
                if link in seen:
                    continue
                seen.add(link)

                job = {
                    "title": title,
                    "apply_link": link,
                    "source": source,
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "qualification": "",
                    "salary": "",
                    "age_limit": "",
                    "vacancy": "",
                    "last_date": "",
                    "status": "RAW"
                }

                jobs.append(job)
                print(f"✅ JOB SAVED: {title}")

        except Exception as e:
            print(f"⚠ Error: {e}")

        time.sleep(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)

    print(f"\n🔥 DONE — {len(jobs)} jobs written to jobs.json")

if __name__ == "__main__":
    process()

import requests
import json
import re
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

# ==================================================
# CONFIG
# ==================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

SOURCE_FILE = "trusted_sources.json"
OUTPUT_FILE = "jobs.json"

# 🔥 Loose keywords (job miss nahi honi chahiye)
KEYWORDS = [
    "recruitment", "apply", "online", "form",
    "vacancy", "vacancies", "posts", "post",
    "bharti", "नियुक्ति", "jobs"
]

# ❌ Sirf non-job pages block
BLOCK_WORDS = [
    "result", "cutoff", "answer key",
    "admit card", "syllabus"
]

# ==================================================
# HELPERS
# ==================================================

def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def is_job_title(title: str) -> bool:
    t = title.lower()
    if len(t) < 6:
        return False
    if any(b in t for b in BLOCK_WORDS):
        return False
    return any(k in t for k in KEYWORDS)

def get_domain(url: str) -> str:
    try:
        return urlparse(url).netloc.replace("www.", "")
    except:
        return ""

# ==================================================
# MAIN SCRAPER
# ==================================================

def process():
    jobs = []
    seen_links = set()

    if not os.path.exists(SOURCE_FILE):
        print("❌ trusted_sources.json missing")
        return

    # ✅ trusted_sources.json = list of domains
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        trusted_domains = json.load(f)

    print(f"🔐 Trusted domains loaded: {len(trusted_domains)}")

    # 🌐 Convert domain → homepage URL
    sources = [f"https://{d}" for d in trusted_domains]

    for source in sources:
        print(f"\n🔍 Checking: {source}")
        try:
            r = requests.get(source, headers=HEADERS, timeout=25)
            soup = BeautifulSoup(r.text, "html.parser")

            base = "{uri.scheme}://{uri.netloc}".format(
                uri=urlparse(source)
            )

            for a in soup.find_all("a", href=True):
                title = clean(a.get_text())
                if not title:
                    continue

                if not is_job_title(title):
                    continue

                link = urljoin(base, a["href"])

                # 🔐 Extra safety: domain check
                if get_domain(link) not in trusted_domains:
                    continue

                if link in seen_links:
                    continue

                seen_links.add(link)

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
                    "stage": "A5.1",
                    "status": "SOFT_ACCEPTED"
                }

                jobs.append(job)
                print(f"✅ SOFT-ACCEPTED: {title}")

        except Exception as e:
            print(f"⚠ Error at {source} → {e}")

        time.sleep(1)

    # 🔥 IMPORTANT: overwrite jobs.json ONLY with scraped jobs
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print(f"\n🔥 DONE — {len(jobs)} jobs SOFT-ACCEPTED into jobs.json")

# ==================================================
# RUN
# ==================================================

if __name__ == "__main__":
    process()

import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import json
import re
import time
import os
import warnings
from urllib.parse import urljoin, urlparse

# ==============================
# 🔕 Suppress XML / HTML warning
# ==============================
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# ==============================
# CONFIG
# ==============================
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "jobs.json"

KEYWORDS = [
    "recruitment",
    "online form",
    "vacancy",
    "apply",
    "posts",
    "notification"
]

BLOCK_WORDS = [
    "admit card",
    "result",
    "answer key",
    "hall ticket",
    "syllabus"
]

# ==============================
# Utility
# ==============================
def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def is_valid_job_title(title):
    t = title.lower()
    if any(b in t for b in BLOCK_WORDS):
        return False
    return any(k in t for k in KEYWORDS)

def normalize_url(base, link):
    return urljoin(base, link)

# ==============================
# 🚀 FAST SCRAPER (LIST ONLY)
# ==============================
def process():
    jobs = []
    seen_links = set()

    if not os.path.exists(SOURCE_FILE):
        print("❌ sources.txt missing")
        return

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        sources = [x.strip() for x in f if x.strip()]

    for source_url in sources:
        print(f"🔍 Checking {source_url}")
        try:
            r = requests.get(source_url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")

            base = "{uri.scheme}://{uri.netloc}".format(
                uri=urlparse(source_url)
            )

            for a in soup.find_all("a"):
                title = clean_text(a.get_text())
                href = a.get("href", "")

                if not title or not href:
                    continue

                if not is_valid_job_title(title):
                    continue

                full_link = normalize_url(base, href)

                if full_link in seen_links:
                    continue

                seen_links.add(full_link)

                print(f"📌 Job Found: {title}")

                jobs.append({
                    "title": title,
                    "apply_link": full_link,
                    "source_page": source_url,
                    "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "confidence_checked_at": None,   # autopilot flag
                })

        except Exception as e:
            print(f"⚠ Error: {e}")

        time.sleep(1)  # 🔥 FAST MODE delay

    # ==============================
    # Save
    # ==============================
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)

    print(f"✅ FAST Scraper Complete — {len(jobs)} jobs collected 🚀")

# ==============================
if __name__ == "__main__":
    process()

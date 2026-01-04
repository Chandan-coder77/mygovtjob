import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import json
import re
import time
import os
import warnings
from urllib.parse import urljoin, urlparse

# ==============================
# 🔕 Suppress warnings
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
    "recruitment", "online form", "vacancy",
    "apply", "posts", "notification"
]

BLOCK_WORDS = [
    "admit card", "result", "answer key",
    "hall ticket", "syllabus", "exam", "panel", "cbt"
]

# ==============================
# Utility
# ==============================
def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def is_valid_title(title):
    t = title.lower()
    if any(b in t for b in BLOCK_WORDS):
        return False
    return any(k in t for k in KEYWORDS)

def normalize_url(base, link):
    return urljoin(base, link)

# ==============================
# 🔍 DETAIL EXTRACT (SAFE + LIGHT)
# ==============================
def extract_details(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    data = {
        "qualification": "",
        "salary": "",
        "age_limit": "",
        "vacancy": "",
        "last_date": ""
    }

    # TABLE FIRST
    for row in soup.find_all("tr"):
        cols = [clean_text(c.get_text()) for c in row.find_all(["td", "th"])]
        if len(cols) < 2:
            continue

        key = cols[0].lower()
        val = cols[1]

        if "qualification" in key or "education" in key:
            data["qualification"] = val
        elif "salary" in key or "pay" in key:
            data["salary"] = val
        elif "age" in key:
            data["age_limit"] = val
        elif "vacanc" in key or "post" in key:
            data["vacancy"] = val
        elif "last date" in key:
            data["last_date"] = val

    # TEXT FALLBACK
    if not data["qualification"]:
        m = re.search(r'(10th|12th|iti|diploma|graduate|degree|b\.?tech|mba)', text, re.I)
        if m:
            data["qualification"] = m.group(1)

    if not data["salary"]:
        m = re.search(r'₹\s?\d[\d,]+', text)
        if m:
            data["salary"] = m.group(0)

    if not data["age_limit"]:
        m = re.search(r'\d{2}\s?-\s?\d{2}', text)
        if m:
            data["age_limit"] = m.group(0)

    if not data["last_date"]:
        m = re.search(r'\d{2}/\d{2}/\d{4}', text)
        if m:
            data["last_date"] = m.group(0)

    return data

# ==============================
# 🚀 MAIN SCRAPER (ODISHA SAFE)
# ==============================
def process():
    jobs = []
    seen = set()

    if not os.path.exists(SOURCE_FILE):
        print("❌ sources.txt missing")
        return

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        sources = [x.strip() for x in f if x.strip() and x.startswith("http")]

    for source_url in sources:
        print(f"🔍 Checking {source_url}")

        try:
            r = requests.get(source_url, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")
            base = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(source_url))

            for a in soup.find_all("a", href=True):
                title = clean_text(a.get_text())
                if not title or not is_valid_title(title):
                    continue

                job_url = normalize_url(base, a["href"])
                if job_url in seen:
                    continue
                seen.add(job_url)

                print(f"📌 Job Found: {title}")

                job = {
                    "title": title,
                    "apply_link": job_url,
                    "qualification": "",
                    "salary": "",
                    "age_limit": "",
                    "vacancy": "",
                    "last_date": "",
                    "status": "PENDING_DETAIL",   # 🔥 VERY IMPORTANT
                    "source": source_url
                }

                # TRY DETAIL PAGE (NON-BLOCKING)
                try:
                    r2 = requests.get(job_url, headers=HEADERS, timeout=15)
                    details = extract_details(r2.text)
                    job.update(details)

                    # अगर कुछ भी मिला तो ACCEPTED
                    if any(job[k] for k in ["qualification","salary","age_limit","vacancy","last_date"]):
                        job["status"] = "DETAIL_OK"

                except:
                    pass

                jobs.append(job)

        except Exception as e:
            print(f"⚠ Error: {e}")

        time.sleep(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)

    print(f"✅ SCRAPER COMPLETE — {len(jobs)} jobs saved 🚀")

# ==============================
if __name__ == "__main__":
    process()

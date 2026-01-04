import requests
from bs4 import BeautifulSoup
import json, re, time, os
from urllib.parse import urljoin, urlparse
from datetime import datetime

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

# ==============================
def clean_text(t):
    return re.sub(r"\s+", " ", t).strip()

def normalize_url(base, link):
    return urljoin(base, link)

# ==============================
def process():
    collected = []
    seen = set()

    if not os.path.exists(SOURCE_FILE):
        print("❌ sources.txt missing")
        return

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        sources = [x.strip() for x in f if x.strip().startswith("http")]

    for source in sources:
        print(f"🔍 Checking {source}")

        try:
            r = requests.get(source, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")
            base = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(source))

            for a in soup.find_all("a", href=True):
                title = clean_text(a.get_text())
                if not title:
                    continue

                link = normalize_url(base, a["href"])
                if link in seen:
                    continue
                seen.add(link)

                collected.append({
                    "title": title,
                    "apply_link": link,
                    "source": source,
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "RAW"
                })

                print(f"📌 RAW SAVED: {title}")

        except Exception as e:
            print(f"⚠ Error: {e}")

        time.sleep(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(collected, f, indent=4, ensure_ascii=False)

    print(f"✅ RAW SCRAPE DONE — {len(collected)} items saved")

# ==============================
if __name__ == "__main__":
    process()

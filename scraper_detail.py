import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import json, re, time, os, warnings
from urllib.parse import urljoin, urlparse
from datetime import datetime

# ==============================
# 🔕 Suppress warnings
# ==============================
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# ==============================
# CONFIG
# ==============================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "jobs.json"

KEYWORDS = [
    "recruitment", "online", "vacancy",
    "apply", "posts", "notification", "advertisement"
]

BLOCK_WORDS = [
    "result", "answer key", "admit card",
    "syllabus", "exam", "panel", "cbt"
]

ODISHA_HINTS = ["osssc", "ossc", "opsc", "odisha"]

# ==============================
# Utility
# ==============================
def clean_text(t):
    return re.sub(r"\s+", " ", t).strip()

def normalize_url(base, link):
    return urljoin(base, link)

def is_valid_title(title, source):
    t = title.lower()

    if any(b in t for b in BLOCK_WORDS):
        return False

    # Odisha sites ko relax karo
    if any(o in source.lower() for o in ODISHA_HINTS):
        return True

    return any(k in t for k in KEYWORDS)

# ==============================
# DETAIL EXTRACT
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

    for row in soup.find_all("tr"):
        cols = [clean_text(c.get_text()) for c in row.find_all(["td","th"])]
        if len(cols) < 2:
            continue

        k = cols[0].lower()
        v = cols[1]

        if "qualification" in k or "education" in k:
            data["qualification"] = v
        elif "salary" in k or "pay" in k:
            data["salary"] = v
        elif "age" in k:
            data["age_limit"] = v
        elif "vacanc" in k or "post" in k:
            data["vacancy"] = v
        elif "last date" in k:
            data["last_date"] = v

    if not data["qualification"]:
        m = re.search(r'(10th|12th|iti|diploma|graduate|degree|b\.?tech|mba)', text, re.I)
        if m: data["qualification"] = m.group(1)

    if not data["salary"]:
        m = re.search(r'₹\s?\d[\d,]+', text)
        if m: data["salary"] = m.group(0)

    if not data["age_limit"]:
        m = re.search(r'\d{2}\s?-\s?\d{2}', text)
        if m: data["age_limit"] = m.group(0)

    if not data["last_date"]:
        m = re.search(r'\d{2}/\d{2}/\d{4}', text)
        if m: data["last_date"] = m.group(0)

    return data

# ==============================
# 🚀 MAIN
# ==============================
def process():
    jobs = []
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

                if not is_valid_title(title, source):
                    continue

                job_url = normalize_url(base, a["href"])
                if job_url in seen:
                    continue
                seen.add(job_url)

                job = {
                    "title": title,
                    "apply_link": job_url,
                    "qualification": "",
                    "salary": "",
                    "age_limit": "",
                    "vacancy": "",
                    "last_date": "",
                    "source": source,
                    "state": "Odisha" if any(o in source.lower() for o in ODISHA_HINTS) else "Other",
                    "status": "BASIC_OK"
                }

                try:
                    r2 = requests.get(job_url, headers=HEADERS, timeout=15)
                    details = extract_details(r2.text)
                    job.update(details)

                    if any(job[k] for k in ["qualification","salary","age_limit","vacancy","last_date"]):
                        job["status"] = "DETAIL_OK"

                except:
                    pass

                jobs.append(job)
                print(f"📌 Saved: {title}")

        except Exception as e:
            print(f"⚠ Error: {e}")

        time.sleep(1)

    final = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_jobs": len(jobs),
        "jobs": jobs
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=4, ensure_ascii=False)

    print(f"✅ DONE — {len(jobs)} jobs saved")

# ==============================
if __name__ == "__main__":
    process()

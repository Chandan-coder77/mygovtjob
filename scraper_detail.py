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

# ✅ STRONG POSITIVE SIGNALS (job related)
KEYWORDS = [
    "recruitment", "vacancy", "notification",
    "apply", "online form", "advertisement",
    "posts", "engagement", "appointment"
]

# ❌ HARD BLOCK (never jobs)
BLOCK_WORDS = [
    "result", "answer key", "admit card", "syllabus",
    "exam", "panel", "cbt", "calendar", "faq",
    "guidelines", "policy", "login", "registration",
    "rules", "tender", "corrigendum", "notice board"
]

# Odisha specific relax (but still job-only)
ODISHA_HINTS = ["osssc", "ossc", "opsc", "odisha"]

# ==============================
# Utility
# ==============================
def clean_text(t):
    return re.sub(r"\s+", " ", t).strip()

def normalize_url(base, link):
    return urljoin(base, link)

def looks_like_job(title: str) -> bool:
    t = title.lower()
    if len(t) < 15:
        return False
    if any(b in t for b in BLOCK_WORDS):
        return False
    return any(k in t for k in KEYWORDS)

# ==============================
# DETAIL EXTRACT (SAFE)
# ==============================
def extract_details(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True).lower()

    data = {
        "qualification": "",
        "salary": "",
        "age_limit": "",
        "vacancy": "",
        "last_date": ""
    }

    # TABLE PRIORITY
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

    # TEXT FALLBACK
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
        m = re.search(r'\d{1,2}/\d{1,2}/\d{4}', text)
        if m: data["last_date"] = m.group(0)

    return data

# ==============================
# 🚀 MAIN SCRAPER
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

                # 🔥 CORE FILTER
                if not looks_like_job(title):
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

                # DETAIL PAGE TRY
                try:
                    r2 = requests.get(job_url, headers=HEADERS, timeout=15)
                    details = extract_details(r2.text)
                    job.update(details)

                    if any(job[k] for k in ["qualification","salary","age_limit","vacancy","last_date"]):
                        job["status"] = "DETAIL_OK"

                except:
                    pass

                jobs.append(job)
                print(f"📌 Job Saved: {title}")

        except Exception as e:
            print(f"⚠ Error: {e}")

        time.sleep(1)

    # 🔥 AUTOPILOT-COMPATIBLE OUTPUT
    final = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_jobs": len(jobs),
        "jobs": jobs
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=4, ensure_ascii=False)

    print(f"✅ DONE — {len(jobs)} REAL JOBS saved")

# ==============================
if __name__ == "__main__":
    process()

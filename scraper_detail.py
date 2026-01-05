import requests, json, re, time, os
from bs4 import BeautifulSoup
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

# 🔑 Job intent words (loose on purpose)
KEYWORDS = [
    "recruitment", "vacancy", "apply",
    "online", "notification", "advertisement",
    "engagement", "appointment"
]

# ❌ Non-job / exam-only words
BLOCK_WORDS = [
    "result", "cutoff", "answer key",
    "admit card", "syllabus", "exam",
    "score", "marks", "cbt"
]

# Odisha / State hint (future learning use)
STATE_HINTS = ["odisha", "ossc", "osssc", "opsc"]

# ==============================
# UTILS
# ==============================
def clean(text):
    return re.sub(r"\s+", " ", text).strip()

def looks_like_job(title: str):
    t = title.lower()

    # hard block
    if any(b in t for b in BLOCK_WORDS):
        return False

    # soft accept if keyword found
    if any(k in t for k in KEYWORDS):
        return True

    # IMPORTANT:
    # If title is long & official-sounding → keep it
    if len(t.split()) >= 5:
        return True

    return False

# ==============================
# MAIN (STEP-A5.1 LOGIC)
# ==============================
def process():
    jobs = []
    seen_links = set()

    if not os.path.exists(SOURCE_FILE):
        print("❌ sources.txt missing")
        return

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        sources = [x.strip() for x in f if x.strip().startswith("http")]

    for source in sources:
        print(f"\n🔍 Checking {source}")

        try:
            r = requests.get(source, headers=HEADERS, timeout=25)
            soup = BeautifulSoup(r.text, "html.parser")

            parsed = urlparse(source)
            base = f"{parsed.scheme}://{parsed.netloc}"

            for a in soup.find_all("a", href=True):
                title = clean(a.get_text())
                if not title:
                    continue

                if not looks_like_job(title):
                    continue

                link = urljoin(base, a["href"])
                if link in seen_links:
                    continue
                seen_links.add(link)

                # 🔥 STEP-A5.1 CORE IDEA
                job = {
                    "title": title,
                    "apply_link": link,
                    "source": source,

                    # ---- soft data (may be empty) ----
                    "qualification": "",
                    "salary": "",
                    "age_limit": "",
                    "vacancy": "",
                    "last_date": "",

                    # ---- intelligence flags ----
                    "status": "SOFT_ACCEPTED",        # ❗ never reject here
                    "confidence": 0.10,               # low but alive
                    "missing_fields": [
                        "qualification",
                        "salary",
                        "age_limit",
                        "vacancy",
                        "last_date"
                    ],

                    # ---- meta ----
                    "state_hint": "Odisha" if any(
                        s in source.lower() for s in STATE_HINTS
                    ) else "Unknown",

                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                jobs.append(job)
                print(f"✅ SOFT-ACCEPTED: {title}")

        except Exception as e:
            print(f"⚠ Error at source {source} → {e}")

        time.sleep(1)

    # ==============================
    # WRITE OUTPUT (ALWAYS NON-EMPTY IF LINKS EXIST)
    # ==============================
    output = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_jobs": len(jobs),
        "stage": "A5.1_SOFT_ACCEPT",
        "jobs": jobs
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"\n🔥 DONE — {len(jobs)} jobs SOFT-ACCEPTED into jobs.json")
    print("🧠 Next: Stage-A5.2 Pattern Memory")

# ==============================
if __name__ == "__main__":
    process()

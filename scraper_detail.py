import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import json
import re
import time
import os
import warnings
from urllib.parse import urljoin, urlparse
from pdfminer.high_level import extract_text

# ==============================
# 🔕 Suppress XML warning
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
    "hall ticket", "syllabus"
]

SIDE_LINK_HINTS = [
    "notification", "advertisement",
    "details", "pdf", "download"
]

MAX_SIDE_LINKS = 2   # ⚡ speed control

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
# PDF Extract (SAFE)
# ==============================
def extract_pdf_text(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        tmp = "temp.pdf"
        with open(tmp, "wb") as f:
            f.write(r.content)

        text = extract_text(tmp)
        os.remove(tmp)
        return clean_text(text)
    except:
        return ""

# ==============================
# Detail Extract (HTML + Table)
# ==============================
def extract_details_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    qualification = salary = age = vacancy = last_date = ""

    # -------- TABLE PRIORITY --------
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cols = [clean_text(c.get_text()) for c in row.find_all(["td","th"])]
            if len(cols) < 2:
                continue

            key = cols[0].lower()
            val = cols[1]

            if "qualification" in key or "education" in key:
                qualification = val
            elif "salary" in key or "pay" in key:
                salary = val
            elif "age" in key:
                age = val
            elif "vacanc" in key or "post" in key:
                vacancy = val
            elif "last date" in key:
                last_date = val

    # -------- TEXT FALLBACK --------
    if not qualification:
        m = re.search(r'(10th|12th|iti|diploma|graduate|degree|b\.?tech|mba)', text, re.I)
        if m: qualification = m.group(1)

    if not salary:
        m = re.search(r'₹\s?\d[\d,]+', text)
        if m: salary = m.group(0)

    if not age:
        m = re.search(r'\d{2}\s?-\s?\d{2}', text)
        if m: age = m.group(0)

    if not vacancy:
        m = re.search(r'vacanc(?:y|ies).*?(\d{1,5})', text, re.I)
        if m: vacancy = m.group(1)

    if not last_date:
        m = re.search(r'\d{2}/\d{2}/\d{4}', text)
        if m: last_date = m.group(0)

    return {
        "qualification": qualification,
        "salary": salary,
        "age_limit": age,
        "vacancy": vacancy,
        "last_date": last_date
    }

# ==============================
# 🔎 SIDE LINK CRAWLER
# ==============================
def crawl_side_links(base_url, soup):
    links = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True).lower()
        href = a["href"].lower()

        if any(h in text or h in href for h in SIDE_LINK_HINTS):
            links.append(normalize_url(base_url, a["href"]))

        if len(links) >= MAX_SIDE_LINKS:
            break

    return links

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
        sources = [x.strip() for x in f if x.strip()]

    for source_url in sources:
        print(f"🔍 Checking {source_url}")

        try:
            r = requests.get(source_url, headers=HEADERS, timeout=15)
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
                }

                # ==============================
                # Detail Page
                # ==============================
                try:
                    r2 = requests.get(job_url, headers=HEADERS, timeout=15)
                    details = extract_details_from_html(r2.text)
                    job.update(details)

                    soup2 = BeautifulSoup(r2.text, "html.parser")

                    # ---------- SIDE LINKS ----------
                    side_links = crawl_side_links(job_url, soup2)
                    for link in side_links:
                        if link.endswith(".pdf"):
                            pdf_text = extract_pdf_text(link)
                            pdf_data = extract_details_from_html(pdf_text)
                            job.update({k:v for k,v in pdf_data.items() if not job.get(k)})
                        else:
                            r3 = requests.get(link, headers=HEADERS, timeout=15)
                            html_data = extract_details_from_html(r3.text)
                            job.update({k:v for k,v in html_data.items() if not job.get(k)})

                except:
                    pass

                jobs.append(job)

        except Exception as e:
            print(f"⚠ Error: {e}")

        time.sleep(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)

    print(f"✅ SMART Scraper Complete — {len(jobs)} jobs collected 🚀")

# ==============================
if __name__ == "__main__":
    process()

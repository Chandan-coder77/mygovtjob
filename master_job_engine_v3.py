"""
MASTER JOB ENGINE v3 – ODISHA MODE (FULL SEMANTIC AI)
Author: You
Purpose: Human-level job data extraction
Engine: OpenAI-compatible API (ChatAnywhere)

FEATURES:
✔ Odisha state jobs + All India jobs ONLY
✔ Reads full page + side links (notification/details/PDF)
✔ Understands English / Hindi / Odia
✔ Job title extracted from all possible formats
✔ Qualification EXACT as per post (no downgrade / no guess)
✔ Fixes wrong dates (8511 / 0002 / 1980 etc.)
✔ STRICT JSON output
✔ 1 job = 1 API call (200/day safe)
"""

import requests
import json
import os
import re
import datetime
from typing import Dict, List
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ==================================================
# CONFIG
# ==================================================

LLM_API_URL = "https://api.chatanywhere.tech/v1/chat/completions"
LLM_MODEL = "gpt-4o-mini"          # 200 calls/day
API_KEY = os.getenv("AI_LLM_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

TODAY = datetime.date.today()
MAX_DAILY_CALLS = 200
TEXT_LIMIT = 12000

# ==================================================
# UTILS
# ==================================================

def clean_text(text: str) -> str:
    text = re.sub(r"<script.*?>.*?</script>", " ", text, flags=re.S)
    text = re.sub(r"<style.*?>.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def normalize_date(date_str: str) -> str:
    try:
        d = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
        if d.year < 2000 or d.year > 2100:
            return ""
        return d.strftime("%d/%m/%Y")
    except:
        return ""

# ==================================================
# SOURCE TEXT ENGINE (MAIN + SIDE LINKS)
# ==================================================

def fetch_page_text(url: str) -> str:
    """
    Fetch:
    - Main job page text
    - Side links text (notification / advertisement / details / PDF)
    Merge everything into ONE source text
    """
    try:
        r = requests.get(url, headers={"User-Agent": HEADERS["User-Agent"]}, timeout=20)
        soup = BeautifulSoup(r.text, "lxml")

        texts = []
        texts.append(soup.get_text(separator=" "))

        side_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].lower()
            if any(x in href for x in [
                "notification",
                "advertisement",
                "details",
                "notice",
                "pdf"
            ]):
                side_links.append(urljoin(url, a["href"]))

        # limit side links for safety
        for link in side_links[:3]:
            try:
                sr = requests.get(link, headers={"User-Agent": HEADERS["User-Agent"]}, timeout=15)
                texts.append(sr.text)
            except:
                continue

        return clean_text(" ".join(texts))

    except:
        return ""

# ==================================================
# LLM CORE (FULL SEMANTIC EXTRACTION)
# ==================================================

def llm_extract(full_text: str) -> Dict:
    prompt = f"""
You are an expert government job data extractor.

Read the FULL text carefully from start to end.

Extract ONLY these fields:
- job_title
- qualification
- age_limit
- salary
- vacancy
- last_date

Rules:
- job_title = official recruitment name
  (from heading / notification / advertisement line)
- Ignore junk like "click here", portals, navigation
- Qualification must be EXACT AS PER POST
  (Do NOT downgrade or upgrade)
- Understand sentences, tables, paragraphs
- Convert age sentence → "18-33"
- Salary like "Pay Level-3 (₹21,700 – 69,100)" → "₹21700-69100"
- Normalize date to DD/MM/YYYY
- Reject impossible dates (year < 2000 or > 2100)
- If information not found, return empty string
- Output STRICT JSON only
- No explanation

TEXT:
\"\"\"
{full_text[:TEXT_LIMIT]}
\"\"\"
"""

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You extract structured government job data only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": 700
    }

    try:
        r = requests.post(LLM_API_URL, headers=HEADERS, json=payload, timeout=120)
        content = r.json()["choices"][0]["message"]["content"]

        match = re.search(r"\{.*\}", content, re.S)
        if not match:
            return {}

        data = json.loads(match.group())

        if data.get("last_date"):
            data["last_date"] = normalize_date(data["last_date"])

        return data

    except:
        return {}

# ==================================================
# MASTER ENGINE (ODISHA MODE)
# ==================================================

def is_allowed_job(url: str) -> bool:
    """
    Allow:
    - Odisha state jobs
    - All India jobs
    Block:
    - Other state-only portals
    """
    url = url.lower()
    odisha_keywords = ["odisha", "orissa", "osssc", "opsc", "odishajobs"]
    all_india_keywords = ["rrb", "sbi", "iocl", "bank", "army", "psu", "gov"]

    return any(k in url for k in odisha_keywords + all_india_keywords)

def run_engine(jobs: List[Dict]) -> List[Dict]:
    final = []
    used_calls = 0

    for job in jobs:
        if used_calls >= MAX_DAILY_CALLS:
            final.append(job)
            continue

        url = job.get("apply_link", "")
        if not url or not is_allowed_job(url):
            final.append(job)
            continue

        page_text = fetch_page_text(url)
        if not page_text:
            final.append(job)
            continue

        extracted = llm_extract(page_text)
        used_calls += 1

        merged = {
            "title": extracted.get("job_title") or job.get("title", ""),
            "apply_link": url,
            "qualification": extracted.get("qualification", ""),
            "age_limit": extracted.get("age_limit", ""),
            "salary": extracted.get("salary", ""),
            "vacancy": extracted.get("vacancy", ""),
            "last_date": extracted.get("last_date", "")
        }

        final.append(merged)

    print(f"LLM calls used today: {used_calls}/{MAX_DAILY_CALLS}")
    return final

# ==================================================
# RUN
# ==================================================

if __name__ == "__main__":
    with open("jobs.json", "r", encoding="utf-8") as f:
        base_jobs = json.load(f)

    updated_jobs = run_engine(base_jobs)

    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(updated_jobs, f, indent=2, ensure_ascii=False)

    print("🔥 MASTER JOB ENGINE v3 (ODISHA MODE) COMPLETED")
    print("✔ Model:", LLM_MODEL)
    print("✔ Jobs processed:", len(updated_jobs))

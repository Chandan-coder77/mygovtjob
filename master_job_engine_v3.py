"""
MASTER JOB ENGINE v3 – ODISHA MODE (CONTROLLED AI)
Author: You
Purpose: Human-level job data extraction with source control

FEATURES:
✔ Odisha + All India only (trusted domains)
✔ Trusted source allowlist (single list mode)
✔ EXACT qualification as per post (no downgrade)
✔ Sentence understanding (no regex guessing)
✔ Date sanity + TODAY expiry filter
✔ No expired jobs (auto removed)
✔ 1 job = 1 API call (200/day safe)
✔ STRICT JSON output
"""

import requests
import json
import os
import re
import datetime
from typing import Dict, List
from urllib.parse import urlparse

# ==================================================
# CONFIG
# ==================================================

LLM_API_URL = "https://api.chatanywhere.tech/v1/chat/completions"
LLM_MODEL = "gpt-4o-mini"   # 200/day safe
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
# LOAD TRUSTED SOURCES (SINGLE LIST MODE)
# trusted_sources.json must be a LIST
# ==================================================

with open("trusted_sources.json", "r", encoding="utf-8") as f:
    TRUSTED_DOMAINS = set(json.load(f))

# ==================================================
# UTILS
# ==================================================

def get_domain(url: str) -> str:
    try:
        return urlparse(url).netloc.replace("www.", "")
    except:
        return ""

def is_trusted_source(url: str) -> bool:
    domain = get_domain(url)
    return any(domain.endswith(d) for d in TRUSTED_DOMAINS)

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

def is_future_date(date_str: str) -> bool:
    """
    Keep only jobs whose last_date >= TODAY
    """
    try:
        d = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
        return d >= TODAY
    except:
        return False

def fetch_page_text(url: str) -> str:
    try:
        r = requests.get(
            url,
            headers={"User-Agent": HEADERS["User-Agent"]},
            timeout=20
        )
        return clean_text(r.text)
    except:
        return ""

# ==================================================
# LLM CORE
# ==================================================

def llm_extract(full_text: str) -> Dict:
    prompt = f"""
You are an expert government job data extractor.

Read the FULL page carefully from start to end.

Extract ONLY these fields:
- job_title
- qualification
- age_limit
- salary
- vacancy
- last_date

Rules:
- job_title = official recruitment name
- qualification = EXACT as per post (no downgrade)
- Understand sentences, tables, notices
- Convert words to numbers if written
- Salary example:
  Pay Level-3 (₹21,700 – 69,100) → ₹21700-69100
- Age sentence → 18-33
- Normalize date to DD/MM/YYYY
- Reject impossible dates
- If not found, return empty string
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
            {"role": "system", "content": "Extract structured job data only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": 700
    }

    try:
        r = requests.post(
            LLM_API_URL,
            headers=HEADERS,
            json=payload,
            timeout=120
        )
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
# MASTER ENGINE
# ==================================================

def run_engine(jobs: List[Dict]) -> List[Dict]:
    final = []
    used_calls = 0

    for job in jobs:
        url = job.get("apply_link", "")

        # Skip untrusted or empty links
        if not url or not is_trusted_source(url):
            continue

        # API limit safety
        if used_calls >= MAX_DAILY_CALLS:
            final.append(job)
            continue

        page_text = fetch_page_text(url)
        if not page_text:
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

        # 🔥 TODAY BASED EXPIRY FILTER
        last_date = merged.get("last_date", "").strip()
        if last_date:
            if not is_future_date(last_date):
                continue  # ❌ expired job removed

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

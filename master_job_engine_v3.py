"""
MASTER JOB ENGINE v3 – FULL SEMANTIC AI (CLOUD LLM)
Author: You
Purpose: Human-level job data extraction
Engine: OpenAI-compatible API (ChatAnywhere)

FEATURES:
✔ Reads full page like human
✔ Understands English / Hindi / Odia
✔ Extracts JOB TITLE from all possible formats
✔ Fixes wrong dates (8511 / 0002 / 1980 etc.)
✔ Converts sentence → structured data
✔ STRICT JSON only
✔ 1 job = 1 API call (200/day safe)
"""

import requests
import json
import os
import re
import datetime
from typing import Dict, List

# ==================================================
# CONFIG
# ==================================================

LLM_API_URL = "https://api.chatanywhere.tech/v1/chat/completions"
LLM_MODEL = "gpt-4o-mini"   # Primary (200/day)
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

def fetch_page_text(url: str) -> str:
    try:
        r = requests.get(url, headers={"User-Agent": HEADERS["User-Agent"]}, timeout=20)
        return clean_text(r.text)
    except:
        return ""

# ==================================================
# LLM CORE (FULL BRAIN)
# ==================================================

def llm_extract(full_text: str) -> Dict:
    """
    Job title possibilities AI must consider:
    - Page <title>
    - H1 / H2 heading
    - "Recruitment of X Posts"
    - "X Online Form 2026"
    - "Advertisement No."
    - Government notification line
    """

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
- Ignore junk like "click here", portals, navigation
- Understand sentences (not regex)
- Convert words to numbers:
  * Matriculation = 10th
  * Intermediate = 12th
- Age sentence → "18-33"
- Salary like "Pay Level-3 (₹21,700 – 69,100)" → "₹21700-69100"
- Normalize date to DD/MM/YYYY
- Reject impossible dates (year < 2000 or > 2100)
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
            {"role": "system", "content": "You extract structured job data only."},
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

    except Exception:
        return {}

# ==================================================
# MASTER ENGINE
# ==================================================

def run_engine(jobs: List[Dict]) -> List[Dict]:
    final = []
    used_calls = 0

    for job in jobs:
        if used_calls >= MAX_DAILY_CALLS:
            final.append(job)
            continue

        url = job.get("apply_link", "")
        if not url:
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

    print("🔥 MASTER JOB ENGINE v3 COMPLETED")
    print("✔ Model:", LLM_MODEL)
    print("✔ Jobs processed:", len(updated_jobs))

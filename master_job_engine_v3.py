"""
MASTER JOB ENGINE v3 – FULL SEMANTIC AI
Author: You
Purpose: 100% sentence-understanding extraction (NOT regex)
Engine: Local LLM (Mistral / LLaMA via Ollama)

RULES:
✔ Reads full page text like a human
✔ Understands English / Hindi / Odia
✔ Extracts real values from sentences, tables, PDFs (via text)
✔ No fake dates (8511, 0002 etc.)
✔ No "click here" junk titles
✔ STRICT JSON output
"""

import requests
import json
import re
import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"   # or "llama3"

TODAY = datetime.date.today()

# --------------------------------------------------
# Utils
# --------------------------------------------------

def clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def normalize_date(date_str: str) -> str:
    """
    Normalize date safely to DD/MM/YYYY
    Reject impossible dates automatically
    """
    try:
        d = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
        if d.year < 2000 or d.year > 2100:
            return ""
        return d.strftime("%d/%m/%Y")
    except:
        return ""

# --------------------------------------------------
# Fetch full page text
# --------------------------------------------------

def fetch_page_text(url: str) -> str:
    try:
        r = requests.get(url, timeout=20)
        return clean_text(r.text)
    except:
        return ""

# --------------------------------------------------
# LLM Extraction (CORE)
# --------------------------------------------------

def extract_with_llm(full_text: str) -> dict:
    prompt = f"""
You are a government job data extractor.

Read the FULL text carefully from start to end.

Extract ONLY these fields:
- job_title
- qualification
- age_limit
- salary
- vacancy
- last_date

Rules:
- job_title = official recruitment name (ignore "click here", portals)
- Understand sentences, not patterns
- Convert words to numbers if needed
- Normalize date to DD/MM/YYYY
- If not found, return empty string
- Output STRICT JSON only
- No explanation

TEXT:
\"\"\"
{full_text[:12000]}
\"\"\"
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        output = r.json()["response"].strip()

        # safety: extract JSON only
        match = re.search(r"\{.*\}", output, re.S)
        if not match:
            return {}

        data = json.loads(match.group())

        # final date sanity
        if data.get("last_date"):
            data["last_date"] = normalize_date(data["last_date"])

        return data

    except Exception as e:
        return {}

# --------------------------------------------------
# MASTER ENGINE
# --------------------------------------------------

def run_engine(jobs: list) -> list:
    final = []

    for job in jobs:
        url = job.get("apply_link", "")
        page_text = fetch_page_text(url)

        if not page_text:
            final.append(job)
            continue

        extracted = extract_with_llm(page_text)

        merged = {
            "title": extracted.get("job_title", job.get("title", "")),
            "apply_link": url,
            "qualification": extracted.get("qualification", ""),
            "salary": extracted.get("salary", ""),
            "age_limit": extracted.get("age_limit", ""),
            "vacancy": extracted.get("vacancy", ""),
            "last_date": extracted.get("last_date", "")
        }

        final.append(merged)

    return final

# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    with open("jobs.json", "r", encoding="utf-8") as f:
        base_jobs = json.load(f)

    enriched = run_engine(base_jobs)

    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    print("🔥 MASTER JOB ENGINE v3 COMPLETED")
    print("✔ Local LLM:", MODEL_NAME)
    print("✔ Jobs processed:", len(enriched))

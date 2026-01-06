"""
MASTER JOB ENGINE – FREE + FUTURE PROOF
Author: You
AI Assist: HuggingFace FREE APIs (Optional, Safe)

RULES:
✔ All India + State jobs allowed
✔ NO job deleted by AI
✔ ONLY expired by LAST DATE
✔ Hindi / Odia / English supported
✔ AI = Assistant, NOT decision maker
"""

import requests
import json
import datetime
import re
import os
from typing import List, Dict

# ======================================================
# GLOBAL HEADERS (IMPORTANT)
# ======================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

# ======================================================
# CONFIG (SAFE – via ENV VARIABLE)
# ======================================================

HF_API_KEY = os.getenv("HF_API_KEY")   # 🔐 from GitHub Secrets
HF_HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "User-Agent": HEADERS["User-Agent"]
} if HF_API_KEY else HEADERS

TODAY = datetime.date.today()

# ======================================================
# UTILS
# ======================================================

def is_expired(last_date: str) -> bool:
    """ONLY date based expiry"""
    try:
        d = datetime.datetime.strptime(last_date, "%d/%m/%Y").date()
        return d < TODAY
    except:
        return False  # date missing → keep job

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

# ======================================================
# STAGE 1 – MULTI SITE CRAWLER
# ======================================================

def crawl_sites(sites: List[str]) -> List[Dict]:
    data = []
    for url in sites:
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            data.append({
                "source": url,
                "raw_text": normalize(r.text)
            })
        except:
            continue
    return data

# ======================================================
# STAGE 2 – TRANSLATION (OPTIONAL AI)
# ======================================================

def translate(text: str) -> str:
    if not HF_API_KEY:
        return text

    api = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
    payload = {
        "inputs": text[:700],
        "parameters": {
            "src_lang": "hin_Deva",
            "tgt_lang": "eng_Latn"
        }
    }

    try:
        r = requests.post(api, headers=HF_HEADERS, json=payload, timeout=20)
        out = r.json()
        if isinstance(out, list) and "translation_text" in out[0]:
            return out[0]["translation_text"]
    except:
        pass

    return text

# ======================================================
# STAGE 3 – RULE BASED EXTRACTION (PRIMARY)
# ======================================================

def rule_extract(text: str) -> Dict:
    job = {
        "salary": "",
        "age_limit": "",
        "vacancy": "",
        "last_date": ""
    }

    if m := re.search(r"₹\s?\d{4,6}", text):
        job["salary"] = m.group()

    if m := re.search(r"\b\d{2}\s?-\s?\d{2}\b", text):
        job["age_limit"] = m.group()

    if m := re.search(r"\b\d{2,6}\b\s?(posts|vacancies)", text, re.I):
        job["vacancy"] = m.group(0)

    if m := re.search(r"\d{2}/\d{2}/\d{4}", text):
        job["last_date"] = m.group()

    return job

# ======================================================
# STAGE 4 – AI NER (SECONDARY ASSIST)
# ======================================================

def ner_extract(text: str) -> Dict:
    if not HF_API_KEY:
        return {}

    api = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"

    try:
        r = requests.post(
            api,
            headers=HF_HEADERS,
            json={"inputs": text[:700]},
            timeout=20
        )
        entities = r.json() if isinstance(r.json(), list) else []

        for e in entities:
            if "₹" in e.get("word", ""):
                return {"salary": e["word"]}
    except:
        pass

    return {}

# ======================================================
# STAGE 5 – JOB CATEGORY CLASSIFIER
# ======================================================

def classify(title: str) -> str:
    if not HF_API_KEY:
        return "OTHER"

    api = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    labels = ["POLICE", "BANK", "PSU", "TEACHING", "APPRENTICE", "OTHER"]

    try:
        r = requests.post(
            api,
            headers=HF_HEADERS,
            json={
                "inputs": title,
                "parameters": {"candidate_labels": labels}
            },
            timeout=20
        )
        return r.json().get("labels", ["OTHER"])[0]
    except:
        return "OTHER"

# ======================================================
# STAGE 6 – VALIDITY GATE (FINAL)
# ======================================================

def validity(job: Dict) -> Dict:
    job["status"] = (
        "EXPIRED"
        if job.get("last_date") and is_expired(job["last_date"])
        else "ACTIVE"
    )
    return job

# ======================================================
# MASTER ENGINE
# ======================================================

def master_engine(raw: List[Dict]) -> List[Dict]:
    final_jobs = []

    for r in raw:
        text = translate(r["raw_text"])

        job = rule_extract(text)

        ai = ner_extract(text)
        for k, v in ai.items():
            if not job.get(k):
                job[k] = v

        job.update({
            "title": text[:120],
            "source": r["source"],
            "category": classify(text[:120])
        })

        final_jobs.append(validity(job))

    return final_jobs

# ======================================================
# RUN
# ======================================================

if __name__ == "__main__":

    SOURCES = [
        "https://www.freejobalert.com",
        "https://www.rrbcdg.gov.in",
        "https://odishajobs.in"
    ]

    raw = crawl_sites(SOURCES)
    jobs = master_engine(raw)

    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print("🔥 MASTER JOB ENGINE COMPLETED")
    print("✔ HF_API_KEY detected:", bool(HF_API_KEY))
    print("✔ Jobs extracted:", len(jobs))

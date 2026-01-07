"""
MASTER JOB ENGINE v2 – FULL PAGE UNDERSTANDING
Author: You
Purpose: Read full web pages (start → end) and extract accurate job data

RULES:
✔ All India + State jobs allowed
✔ NO job deletion
✔ ONLY expired by LAST DATE
✔ Hindi / Odia / English supported
✔ AI = Reader & Extractor, NOT decision maker
✔ v2 runs ONLY to fill missing / unclear fields
"""

import requests
import json
import datetime
import re
import os
from typing import Dict, List

# ======================================================
# GLOBAL HEADERS (ANTI-BLOCK)
# ======================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

# ======================================================
# CONFIG
# ======================================================

HF_API_KEY = os.getenv("HF_API_KEY")
HF_HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "User-Agent": HEADERS["User-Agent"]
} if HF_API_KEY else HEADERS

TODAY = datetime.date.today()

# HuggingFace models (FREE)
MODEL_QA = "deepset/roberta-base-squad2"
MODEL_TRANSLATE = "facebook/nllb-200-distilled-600M"

# ======================================================
# UTILITIES
# ======================================================

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def is_expired(last_date: str) -> bool:
    try:
        d = datetime.datetime.strptime(last_date, "%d/%m/%Y").date()
        return d < TODAY
    except:
        return False

# ======================================================
# FETCH FULL PAGE (START → END)
# ======================================================

def fetch_full_page(url: str) -> str:
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        return normalize(r.text)
    except:
        return ""

# ======================================================
# LANGUAGE NORMALIZATION (Hindi / Odia → English)
# ======================================================

def translate_to_english(text: str) -> str:
    if not HF_API_KEY:
        return text

    payload = {
        "inputs": text[:1500],
        "parameters": {
            "src_lang": "hin_Deva",
            "tgt_lang": "eng_Latn"
        }
    }

    try:
        r = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_TRANSLATE}",
            headers=HF_HEADERS,
            json=payload,
            timeout=25
        )
        out = r.json()
        if isinstance(out, list) and "translation_text" in out[0]:
            return normalize(out[0]["translation_text"])
    except:
        pass

    return text

# ======================================================
# AI QUESTION–ANSWER EXTRACTION (CORE v2)
# ======================================================

def ask_ai(context: str, question: str) -> str:
    if not HF_API_KEY:
        return ""

    payload = {
        "inputs": {
            "question": question,
            "context": context[:3000]
        }
    }

    try:
        r = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_QA}",
            headers=HF_HEADERS,
            json=payload,
            timeout=30
        )
        data = r.json()
        if isinstance(data, dict):
            if data.get("score", 0) >= 0.6:
                return normalize(data.get("answer", ""))
    except:
        pass

    return ""

# ======================================================
# FIELD EXTRACTION USING AI UNDERSTANDING
# ======================================================

def extract_fields_v2(page_text: str) -> Dict:
    result = {
        "salary": "",
        "age_limit": "",
        "vacancy": "",
        "last_date": ""
    }

    # Questions AI will answer
    questions = {
        "salary": "What is the salary or pay scale for this recruitment?",
        "age_limit": "What is the age limit for applying?",
        "vacancy": "How many total vacancies or posts are available?",
        "last_date": "What is the last date to apply?"
    }

    for field, q in questions.items():
        ans = ask_ai(page_text, q)
        if ans:
            result[field] = ans

    return result

# ======================================================
# RULE-BASED NORMALIZATION (FINAL SAFETY)
# ======================================================

def normalize_fields(data: Dict) -> Dict:
    clean = {
        "salary": "",
        "age_limit": "",
        "vacancy": "",
        "last_date": ""
    }

    if m := re.search(r"₹\s?\d{4,6}", data.get("salary", "")):
        clean["salary"] = m.group()

    if m := re.search(r"\b\d{2}\s?[-to]{1,3}\s?\d{2}\b", data.get("age_limit", "")):
        clean["age_limit"] = m.group().replace("to", "-")

    if m := re.search(r"\b\d{2,6}\b", data.get("vacancy", "")):
        clean["vacancy"] = m.group()

    if m := re.search(r"\d{2}/\d{2}/\d{4}", data.get("last_date", "")):
        clean["last_date"] = m.group()

    return clean

# ======================================================
# MASTER JOB ENGINE v2
# ======================================================

def run_master_job_engine_v2(jobs: List[Dict]) -> List[Dict]:
    updated = []

    for job in jobs:
        # Keep original job always
        new_job = job.copy()

        # Check missing fields
        missing = any(
            not job.get(f)
            for f in ["salary", "age_limit", "vacancy", "last_date"]
        )

        if missing and job.get("apply_link"):
            page = fetch_full_page(job["apply_link"])
            page = translate_to_english(page)

            ai_data = extract_fields_v2(page)
            clean = normalize_fields(ai_data)

            for k, v in clean.items():
                if not new_job.get(k) and v:
                    new_job[k] = v

        # Validity check (ONLY DATE)
        new_job["status"] = (
            "EXPIRED"
            if new_job.get("last_date") and is_expired(new_job["last_date"])
            else "ACTIVE"
        )

        updated.append(new_job)

    return updated

# ======================================================
# RUN
# ======================================================

if __name__ == "__main__":
    with open("jobs.json", "r", encoding="utf-8") as f:
        jobs = json.load(f)

    final_jobs = run_master_job_engine_v2(jobs)

    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(final_jobs, f, indent=2, ensure_ascii=False)

    print("🔥 MASTER JOB ENGINE v2 COMPLETED")
    print("✔ Full page understanding enabled")
    print("✔ AI Question-Answer extraction active")
    print("✔ Jobs processed:", len(final_jobs))
    print("✔ HF API detected:", bool(HF_API_KEY))

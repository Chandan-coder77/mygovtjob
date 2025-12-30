import json
import os
import re
import requests
from bs4 import BeautifulSoup

# =========================
# Load JSON Safe Function
# =========================
def load_json(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = f.read()
            try:
                return json.loads(data)              
            except:
                return json.loads(data.strip())
    except:
        return {}


# =========================
# Load Memory from jobs.json
# =========================
memory = load_json("jobs.json")

if isinstance(memory, str):
    memory = json.loads(memory)

qualification_patterns = memory.get("qualification_patterns", [])
salary_patterns = memory.get("salary_patterns", [])
age_patterns = memory.get("age_patterns", [])
lastdate_patterns = memory.get("lastdate_patterns", [])
vacancy_patterns = memory.get("vacancy_patterns", [])


# =========================
# User-Agent (Your Required Header Included ✔)
# =========================
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}


# =========================
# Job Sites to Learn from
# =========================
job_sites = [
    "https://www.freejobalert.com/",
    "https://www.sarkariresult.com/",
    "https://www.sarkariprep.in/"
]


# =========================
# Extract Information
# =========================
def extract_data(text):
    found = {
        "qualification": [],
        "salary": [],
        "age": [],
        "lastdate": [],
        "vacancy": []
    }

    for q in qualification_patterns:
        if q.lower() in text.lower():
            found["qualification"].append(q)

    for s in salary_patterns:
        if s.lower() in text.lower():
            found["salary"].append(s)

    for a in age_patterns:
        if a in text:
            found["age"].append(a)

    for l in lastdate_patterns:
        if l in text:
            found["lastdate"].append(l)

    for v in vacancy_patterns:
        if v in text:
            found["vacancy"].append(v)

    return found


# =========================
# Scraping Runner
# =========================
for site in job_sites:
    print(f"\n🌐 Fetching: {site}")

    try:
        r = requests.get(site, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")

        content = soup.get_text(separator=" ").strip()
        result = extract_data(content)

        print("🔍 Extracted → ", result)

    except Exception as e:
        print("❌ Failed at:", site, "| Error →", e)


print("\n✅ Scraper Finished Successfully (No Crash)")

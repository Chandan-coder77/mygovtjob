import re
from datetime import datetime

def normalize_salary(text):
    if not text: 
        return None

    text = text.lower().replace(",", "").strip()

    # Numbers extract
    match = re.findall(r"₹?\s?(\d+\.?\d*)", text)
    if match:
        num = float(match[0])

        # If LPA detected convert to yearly
        if "lpa" in text or "lakh" in text:
            return int(num * 100000)

        # Normal monthly salary convert to yearly approx
        if "per month" in text or "monthly" in text:
            return int(num * 12)

        return int(num)

    return None


def normalize_date(date_str):
    if not date_str:
        return None

    try:
        # formats like 01/12/2025
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        pass

    try:
        # formats like 1/2/2025
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        return None


def clean_job(job):
    job_clean = {}

    job_clean["title"] = job.get("title", "").strip()
    job_clean["qualification"] = job.get("qualification", "").lower()
    job_clean["salary"] = normalize_salary(job.get("salary", ""))
    job_clean["last_date"] = normalize_date(job.get("last_date", ""))

    return job_clean

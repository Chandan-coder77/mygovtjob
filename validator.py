import re
from datetime import datetime

# ================== SALARY AUTO FIX ==================
def fix_salary(value):
    if not value:
        return None

    txt = str(value).lower().replace(",", "").replace("rs", "").strip()

    # Numeric salary extract
    num = re.findall(r'\d{4,7}', txt)
    if num:
        return f"₹{num[0]}"

    # LPA detect
    lpa = re.findall(r'(\d+\.?\d*)\s*lpa', txt)
    if lpa:
        return f"{lpa[0]} LPA"

    return None


# ================== AGE RANGE FIX ==================
def fix_age(value):
    if not value:
        return None

    txt = str(value).replace(" ", "")
    match = re.findall(r'(\d{1,2})\D+(\d{1,2})', txt)
    if match:
        a, b = match[0]
        if 15 <= int(a) <= 60 and 15 <= int(b) <= 60:
            return f"{a}-{b}"
    return None


# ================== VACANCY FIX ==================
def fix_vacancy(value):
    if not value:
        return None

    num = re.findall(r'\d{1,5}', str(value))
    if num and int(num[0]) <= 5000:  # safety limit
        return num[0]
    return None


# ================== LAST DATE FIX ==================
def fix_last_date(value):
    if not value:
        return None

    match = re.findall(r'(\d{1,2}/\d{1,2}/\d{4})', value)
    if not match:
        return None

    date = match[0]
    try:
        datetime.strptime(date, "%d/%m/%Y")
        return date
    except:
        return None


# ================== MAIN AUTO-CORRECT WRAPPER ==================
def validate_job(job):
    fixed = {}

    # qualification always lowercase
    if job.get("qualification"):
        fixed["qualification"] = job["qualification"].lower()

    # salary
    if job.get("salary"):
        v = fix_salary(job["salary"])
        if v: fixed["salary"] = v

    # age
    if job.get("age_limit"):
        v = fix_age(job["age_limit"])
        if v: fixed["age_limit"] = v

    # vacancy
    if job.get("vacancy"):
        v = fix_vacancy(job["vacancy"])
        if v: fixed["vacancy"] = v

    # last date
    if job.get("last_date"):
        v = fix_last_date(job["last_date"])
        if v: fixed["last_date"] = v

    return fixed if fixed else job

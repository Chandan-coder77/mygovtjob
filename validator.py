import re
from datetime import datetime

# ------------ Validate Salary ------------
def validate_salary(value):
    if not value or len(value) > 15:
        return None

    value = value.replace(",", "").lower()

    num = re.findall(r'\d{4,7}', value)
    if num:
        return f"₹{num[0]}"

    lpa = re.findall(r'(\d+\.?\d*)\s*lpa', value)
    if lpa:
        return f"{lpa[0]} LPA"

    return None


# ------------ Validate Age ------------
def validate_age(value):
    if not value:
        return None

    match = re.findall(r'(\d{1,2}-\d{1,2})', value.replace(" ", ""))
    return match[0] if match else None


# ------------ Validate Vacancy ------------
def validate_vacancy(value):
    if not value:
        return None

    num = re.findall(r"\d{1,4}", str(value))
    if num and int(num[0]) < 5000:
        return num[0]

    return None


# ------------ Validate Last Date ------------
def validate_last_date(value):
    if not value:
        return None

    match = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', value)
    if not match:
        return None

    date = match[0]
    try:
        datetime.strptime(date, "%d/%m/%Y")  # valid check
        return date
    except:
        return None


# ------------ Full Job Validation Wrapper ------------
def validate_job(job):
    fixed = {}

    if "salary" in job:
        v = validate_salary(job["salary"])
        if v: fixed["salary"] = v

    if "age_limit" in job:
        v = validate_age(job["age_limit"])
        if v: fixed["age_limit"] = v

    if "vacancy" in job:
        v = validate_vacancy(job["vacancy"])
        if v: fixed["vacancy"] = v

    if "last_date" in job:
        v = validate_last_date(job["last_date"])
        if v: fixed["last_date"] = v

    if "qualification" in job:
        fixed["qualification"] = job["qualification"].lower()

    return fixed if fixed else job

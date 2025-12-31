import re
from datetime import datetime

# ================= SALARY NORMALIZER =================
def validate_salary(value):
    if not value:
        return None

    text = str(value).replace(",", "").lower()

    # Extract numbers (₹ based)
    nums = re.findall(r'\d{4,7}', text)
    if nums:
        num = int(nums[0])
        if num > 2000000:  # unrealistic salary drop
            return None
        return f"₹{num:,}"

    # Detect LPA
    lpa = re.findall(r'(\d+\.?\d*)\s*lpa', text)
    if lpa:
        return f"{lpa[0]} LPA"

    return None


# ================= AGE RANGE CLEANER =================
def validate_age(value):
    if not value:
        return None

    txt = str(value).replace(" ", "")
    match = re.findall(r'(\d{1,2}-\d{1,2})', txt)
    return match[0] if match else None


# ================= VACANCY LIMIT FILTER =================
def validate_vacancy(value):
    if not value:
        return None

    num = re.findall(r'\d{1,5}', str(value))
    if num:
        n = int(num[0])
        if 1 <= n <= 5000:
            return str(n)

    return None


# ================= LAST DATE REPAIR =================
def validate_last_date(value):
    if not value:
        return None

    match = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', value)
    if not match:
        return None

    date = match[0]

    try:
        datetime.strptime(date, "%d/%m/%Y")  # check valid date real calendar
        return date
    except:
        return None


# ================= FINAL JOB VALIDATION LAYER =================
def validate_job(job):
    fixed = {}

    if job.get("qualification"):
        fixed["qualification"] = str(job["qualification"]).lower()

    if job.get("salary"):
        v = validate_salary(job["salary"])
        if v: fixed["salary"] = v

    if job.get("age_limit"):
        v = validate_age(job["age_limit"])
        if v: fixed["age_limit"] = v

    if job.get("vacancy"):
        v = validate_vacancy(job["vacancy"])
        if v: fixed["vacancy"] = v

    if job.get("last_date"):
        v = validate_last_date(job["last_date"])
        if v: fixed["last_date"] = v

    # जर कुछ भी validate नहीं हुआ तो job as-is return
    return fixed if fixed else job

import re

# ==========================================================
# SAFE STRING WRAPPER (Core Fix for lower() error)
# ----------------------------------------------------------
def to_str(value):
    return str(value).strip().replace("\n", " ") if value is not None else ""


# ==========================================================
# Salary Extract
# ==========================================================
def extract_salary(text):
    text = to_str(text).lower().replace(",", "")

    num = re.findall(r'(\d{4,7})', text)
    if num:
        return f"₹{num[0]}"

    # LPA detect
    lpa = re.findall(r'(\d+\.?\d*)\s*lpa', text)
    if lpa:
        return f"{lpa[0]} LPA"

    return text


# ==========================================================
# Age Extract
# ==========================================================
def extract_age(text):
    text = to_str(text).replace(" ", "")
    m = re.findall(r'(\d{1,2}-\d{1,2})', text)
    return m[0] if m else text


# ==========================================================
# Vacancy Extract
# ==========================================================
def extract_vacancy(text):
    text = to_str(text)
    num = re.findall(r'\d{1,4}', text)
    return num[0] if num else text


# ==========================================================
# Last Date Extract
# ==========================================================
def extract_last_date(text):
    text = to_str(text)
    m = re.findall(r'(\d{1,2}/\d{1,2}/\d{4})', text)
    return m[0] if m else text


# ==========================================================
# Qualification Extract
# ==========================================================
def extract_qualification(text):
    text = to_str(text).lower()
    keys = ["10th","12th","iti","diploma","b.sc","ba","bsc","graduate",
            "post graduate","m.sc","b.com","phd","engineering","mba"]
    for k in keys:
        if k in text:
            return k
    return text


# ==========================================================
# MAIN COMBINER USED BY AI TRAINER
# ==========================================================
def extract_values(job):
    if not isinstance(job, dict):
        return job

    return {
        "title": to_str(job.get("title","")),
        "qualification": extract_qualification(job.get("qualification","")),
        "salary": extract_salary(job.get("salary","")),
        "age_limit": extract_age(job.get("age_limit","")),
        "vacancy": extract_vacancy(job.get("vacancy","")),
        "last_date": extract_last_date(job.get("last_date","")),
        "apply_link": to_str(job.get("apply_link",""))
    }

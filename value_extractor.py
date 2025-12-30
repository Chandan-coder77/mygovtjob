import re

# ----------------- Salary Extract -----------------
def extract_salary(text):
    if not text: return ""
    text = text.lower().replace(",", "")

    match = re.findall(r'₹?\s?(\d{4,7})', text)
    if match:
        return f"₹{match[0]}"
    
    if "lpa" in text:
        num = re.findall(r'(\d+\.?\d*)', text)
        if num:
            return f"{num[0]} LPA"

    return text.strip()


# ----------------- Age Extract -----------------
def extract_age(text):
    if not text: return ""
    match = re.findall(r'(\d{1,2}\s?-\s?\d{1,2})', text)
    if match:
        return match[0].replace(" ", "")
    return text.strip()


# ----------------- Vacancy Extract -----------------
def extract_vacancy(text):
    if not text: return ""
    num = re.findall(r'\d{1,4}', text)
    return num[0] if num else text


# ----------------- Last Date Extract -----------------
def extract_last_date(text):
    if not text: return ""
    match = re.findall(r'(\d{1,2}/\d{1,2}/\d{4})', text)
    return match[0] if match else text.strip()


# ----------------- Qualification Extract -----------------
def extract_qualification(text):
    if not text: return ""
    text = text.lower()
    keywords = ["10th","12th","iti","diploma","b.sc","ba","bsc","graduate","post graduate","m.sc","b.com","phd","engineering","mba"]
    for k in keywords:
        if k in text:
            return k
    return text


# =====================================================
# 🔥 Main Combiner — THIS is what AI Trainer will use
# =====================================================
def extract_values(job):
    if not isinstance(job, dict):
        return job

    job["salary"] = extract_salary(job.get("salary", ""))
    job["age_limit"] = extract_age(job.get("age_limit", ""))
    job["vacancy"] = extract_vacancy(job.get("vacancy", ""))
    job["last_date"] = extract_last_date(job.get("last_date", ""))
    job["qualification"] = extract_qualification(job.get("qualification", ""))

    return job

import re

# =================================================================
# Safe Converter
# =================================================================
def to_str(x):
    return str(x).strip().replace("\n"," ") if x not in [None,"None"] else ""


# =================================================================
# SALARY Extractor (More Accurate – supports range + LPA)
# =================================================================
def extract_salary(text):
    text = to_str(text).lower()

    # ₹21700 - ₹69100 / 25000-50000 type
    m = re.findall(r'₹?\s?(\d{4,7})\s?[-to–]\s?₹?\s?(\d{4,7})', text)
    if m:
        low, high = m[0]
        return f"₹{low}-{high}"

    # single salary 8000 < x < 200000
    n = re.findall(r'₹?\s?(\d{4,7})', text.replace(",", ""))
    if n:
        num = int(n[0])
        if 6000 < num < 200000:
            return f"₹{num}"

    # LPA formats
    lpa = re.findall(r'(\d+\.?\d*)\s*lpa', text)
    if lpa:
        return lpa[0] + " LPA"

    return ""


# =================================================================
# AGE Extractor (Smart normalize)
# =================================================================
def extract_age(text):
    t = to_str(text).lower().replace(" ", "").replace("years", "")
    m = re.findall(r'(\d{1,2})[-to]{1,3}(\d{1,2})', t)

    if m:
        a, b = map(int, m[0])
        if 15 <= a <= 40 and 18 <= b <= 60:
            return f"{a}-{b}"
    return ""


# =================================================================
# VACANCY Extractor (Valid limit based)
# =================================================================
def extract_vacancy(text):
    n = re.findall(r'\b(\d{1,5})\b', to_str(text))
    if n:
        v = int(n[0])
        if 5 < v < 50000:
            return str(v)
    return ""


# =================================================================
# LAST DATE Extractor
# =================================================================
def extract_last_date(text):
    d = re.findall(r'(\d{1,2}/\d{1,2}/\d{4})', to_str(text))
    return d[0] if d else ""


# =================================================================
# QUALIFICATION – FULL SMART ENGINE
# =================================================================
def extract_qualification(text):
    t = to_str(text).lower()

    # Full sentence extraction – Best part!
    # Example output: 
    # "Matriculation or 10th Class Pass from a recognized Board" → returns "10th (Matriculation)"
    sentence = re.findall(r'qualification.?[:\-]?\s?([a-z0-9 ,./&()-]+)', t)
    if sentence:
        s = sentence[0].strip()
        # Short keyword pick also
        for k in ["phd","mba","b.tech","m.tech","ba","b.sc","m.sc","b.com","12th","10th","iti","diploma","graduate","post graduate","engineering"]:
            if k in s:
                return f"{k}+" if " or " in s or "/" in s else k

    # fallback detection keywords
    keys=["10th","12th","iti","diploma","b.sc","ba","graduate","post graduate","m.sc","b.com","mba","engineering","phd"]
    for k in keys:
        if k in t:
            return k

    return ""


# =================================================================
# Final Output Merger
# =================================================================
def extract_values(job):
    if not isinstance(job, dict):
        return job

    return {
        "title": to_str(job.get("title", "")),
        "apply_link": to_str(job.get("apply_link", "")),
        "qualification": extract_qualification(job.get("qualification", "")),
        "salary": extract_salary(job.get("salary", "")),
        "age_limit": extract_age(job.get("age_limit", "")),
        "vacancy": extract_vacancy(job.get("vacancy", "")),
        "last_date": extract_last_date(job.get("last_date", "")),
            }

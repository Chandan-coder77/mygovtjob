import re

# =================================================================
# SAFE STRING (int/None value भी error नहीं देगा)
# =================================================================
def to_str(x):
    return str(x).strip().replace("\n"," ") if x not in [None,"None"] else ""


# =================================================================
# SALARY (valid only if realistic)
# =================================================================
def extract_salary(text):
    text = to_str(text).lower().replace(",","")

    # salary numbers (₹8000–200000 valid)
    s = re.findall(r'\b(\d{4,7})\b', text)
    if s:
        num = int(s[0])
        if 4000 < num < 200000:
            return f"₹{num}"

    # 1.5 LPA / 2.3 LPA detection
    l = re.findall(r'(\d+\.?\d*)\s*lpa', text)
    if l:
        return f"{l[0]} LPA"

    return ""


# =================================================================
# AGE (must be like 18-30 and realistic)
# =================================================================
def extract_age(text):
    t = to_str(text).replace(" ","")
    m = re.findall(r'(\d{1,2}-\d{1,2})', t)
    if m:
        a=m[0]
        s,e = map(int,a.split("-"))
        if 15 <= s <= 40 and 18 <= e <= 60:
            return a
    return ""


# =================================================================
# VACANCY (acceptable only 5 to 50000)
# =================================================================
def extract_vacancy(text):
    n = re.findall(r'\b(\d{1,5})\b', to_str(text))
    if n:
        v=int(n[0])
        if 5 < v < 50000:
            return str(v)
    return ""


# =================================================================
# LAST DATE only dd/mm/yyyy
# =================================================================
def extract_last_date(text):
    d = re.findall(r'(\d{1,2}/\d{1,2}/\d{4})', to_str(text))
    return d[0] if d else ""


# =================================================================
# QUALIFICATION — Stage-6 Smart Prioritized Extractor 🔥
# =================================================================
def extract_qualification(text):
    t = to_str(text).lower()

    priority = [
        ("phd", "PhD"),
        ("engineering", "Engineering"),
        ("b.tech", "Engineering"),
        ("m.sc", "Post Graduate"),
        ("mba", "Post Graduate"),
        ("m.com", "Post Graduate"),
        ("post graduate", "Post Graduate"),
        ("graduate", "Graduate"),
        ("ba", "BA"),
        ("b.sc", "B.Sc"),
        ("bsc", "B.Sc"),
        ("b.com", "B.Com"),
        ("diploma", "Diploma"),
        ("iti", "ITI"),
        ("12th", "12th"),
        ("10th", "10th")   # Fallback (last priority)
    ]

    for key, value in priority:
        if key in t:
            return value

    return ""


# =================================================================
# FINAL MERGER USED IN TRAINER + SCRAPER
# =================================================================
def extract_values(job):
    if not isinstance(job,dict):
        return job

    return {
        "title": to_str(job.get("title","")),
        "apply_link": to_str(job.get("apply_link","")),
        "qualification": extract_qualification(job.get("qualification","")),
        "salary": extract_salary(job.get("salary","")),
        "age_limit": extract_age(job.get("age_limit","")),
        "vacancy": extract_vacancy(job.get("vacancy","")),
        "last_date": extract_last_date(job.get("last_date","")),
}

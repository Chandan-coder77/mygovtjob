import re

def extract_qualification(text):
    patterns = [
        r"(10th|Matric|12th|Diploma|ITI|Graduate|Post Graduate|B\.?Tech|M\.?Tech|MBA|BCA|MCA|BSC|MSC|BA|MA|PhD)",
        r"Qualification[:\-]\s*(.*)"
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m: return m.group(0)
    return "Check Official Notification"

def extract_salary(text):
    patterns = [
        r"₹\s?\d{4,6}\s?[-–to]+\s?₹?\s?\d{4,6}",
        r"Rs\.?\s?\d{4,6}.*\d{4,6}",
        r"Salary[:\-]\s*(.*?)(\n|$)"
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m: return m.group(0)
    return "As per Govt Rules"

def extract_age(text):
    patterns = [
        r"Age\s?Limit[:\-]?\s*\d{1,2}\s*to\s*\d{1,2}",
        r"Minimum\s*Age.*?\d{1,2}",
        r"Maximum\s*Age.*?\d{1,2}"
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m: return m.group(0)
    return "18+ Years"

def extract_last_date(text):
    m = re.search(r"\d{1,2}[\/\-\.\s]\d{1,2}[\/\-\.\s]\d{2,4}", text)
    if m: return m.group(0)
    return "Not Mentioned"

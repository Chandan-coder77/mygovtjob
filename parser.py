import re

def extract_qualification(text):
    patterns=[
        r"(10th|12th|Diploma|ITI|Graduate|Post\s?Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BCA|MCA|BA|MA|PhD)",
        r"Qualification[:\-]\s*(.*)"
    ]
    for p in patterns:
        m=re.search(p,text,re.IGNORECASE)
        if m:return m.group(0)
    return "Check Notification"

def extract_salary(text):
    patterns=[
        r"₹\s?\d{4,6}\s?[-to]*\s?₹?\s?\d{4,6}",
        r"Rs\.?\s?\d{4,6}\s?[-to]*\s?₹?\s?\d{4,6}",
        r"Salary[:\-]\s*(.*?)(\n|$)"
    ]
    for p in patterns:
        m=re.search(p,text,re.IGNORECASE)
        if m:return m.group(0)
    return "As per Govt Rules"

def extract_age(text):
    patterns=[
        r"Age\s?Limit[:\-]?\s*\d{1,2}\s*to\s*\d{1,2}",
        r"Minimum\s*Age.*?\d{1,2}",
        r"Maximum\s*Age.*?\d{1,2}"
    ]
    for p in patterns:
        m=re.search(p,text,re.IGNORECASE)
        if m:return m.group(0)
    return "18+"

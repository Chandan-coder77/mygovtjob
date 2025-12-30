import re

def extract_salary(text):
    if not text: return ""
    text = text.lower()

    # salary numbers extract
    match = re.findall(r'₹?\s?(\d{4,7})', text.replace(",", ""))
    if match:
        return f"₹{match[0]}"
    
    # LPA detect
    if "lpa" in text:
        num = re.findall(r'(\d+\.?\d*)', text)
        if num:
            return f"{num[0]} LPA"
    
    return text.strip()


def extract_age(text):
    if not text: return ""

    match = re.findall(r'(\d{1,2}\s?-\s?\d{1,2})', text)
    if match:
        return match[0].replace(" ", "")
    
    return text.strip()


def extract_vacancy(text):
    if not text: return ""
    num = re.findall(r'\d{1,4}', text)
    return num[0] if num else text


def extract_last_date(text):
    if not text: return ""
    match = re.findall(r'(\d{1,2}/\d{1,2}/\d{4})', text)
    return match[0] if match else text.strip()


def extract_qualification(text):
    if not text: return ""
    text = text.lower()
    keywords = ["10th","12th","iti","diploma","b.sc","ba","bsc","graduate","post graduate","m.sc","b.com","phd","engineering","mba"]
    for k in keywords:
        if k in text:
            return k
    return text

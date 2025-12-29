import re

def find(patterns, text, default=None):
    if isinstance(patterns,str): patterns=[patterns]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m: return m.group(1).strip()
    return default

def smart_extract(text):
    text_low = text.lower()

    return {
        "vacancies": find([r"(\d{1,5})\s+post", r"vacanc(?:y|ies).*?(\d{1,5})"],text_low,"Not Mentioned"),
        "qualification": find([r"(10th|12th|iti|diploma|graduate|post graduate|b\.?tech|m\.?tech|mba|bsc|msc|ba|ma|mca|phd)",
                               r"qualification.*?(\w.*?)\n"],text_low,"Check Notification"),
        "salary": find([r"(₹\s?\d{4,7}.*?\d{4,7})",
                        r"salary.*?(₹.*?)\n"],text_low,"As per Govt Rules"),
        "age_limit": find([r"age.*?(\d{1,2}.?to.? \d{1,2})",
                           r"(\d{2}\+)\s*years"],text_low,"18+"),
        "last_date": find([r"last\s*date.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
                           r"apply.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})"],text_low,"Not Mentioned"),
    }

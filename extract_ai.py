import re

def smart_extract(text):
    text_low = text.lower()

    def find(pattern, default="Not Found"):
        match = re.search(pattern, text_low, re.I)
        return match.group(1).strip() if match else default

    return {
        "title": find(r"(recruitment|vacancy|notification|job)\s*([^\n]*)", default="Unknown Job"),
        "vacancies": find(r"(\d{1,5})\s+post", default="Not Mentioned"),
        "qualification": find(r"(10th|12th|iti|diploma|graduate|post graduate|b\.?tech|m\.?tech|mba|ba|ma|phd|bsc|msc|mca|bca)", default="Check Notification"),
        "salary": find(r"(₹\s?\d{4,7}.*?\d{4,7})", default="As per Govt Rules"),
        "age_limit": find(r"(?:age|years?)\D*?(\d{1,2}\s*-\s*\d{1,2}|\d{2}\+)", default="18+"),
        "last_date": find(r"last\s*date.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})", default="Not Mentioned"),
    }

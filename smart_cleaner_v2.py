import re

# ---------------- SMART CLEANER V2 ----------------
# invalid, garbage, duplicate mixed values auto remove

def clean_text(text):
    if not text or not isinstance(text, str):
        return text
    
    txt = text.strip().lower()

    # remove garbage words & symbols
    remove_words = ["apply now", "click here", "download", "notification", "official", "website"]
    for w in remove_words:
        txt = txt.replace(w, "")

    txt = re.sub(r'\s+', ' ', txt)       # extra spaces remove
    txt = re.sub(r'[,;]+', '', txt)      # extra comma & semicolon remove
    
    return txt.strip()


def clean_job(job):
    # salary/qualification/date normalized clean form
    if "qualification" in job:
        job["qualification"] = clean_text(job["qualification"])

    if "salary" in job:
        job["salary"] = clean_text(str(job["salary"]))

    if "age_limit" in job:
        job["age_limit"] = clean_text(str(job["age_limit"]))

    if "last_date" in job:
        job["last_date"] = clean_text(str(job["last_date"]))

    if "vacancy" in job:
        job["vacancy"] = clean_text(str(job["vacancy"]))

    return job

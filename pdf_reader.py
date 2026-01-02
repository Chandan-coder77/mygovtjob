import os
import re
import requests
from io import BytesIO
from pdfminer.high_level import extract_text
from datetime import datetime

PDF_DIR = "pdf_cache"
os.makedirs(PDF_DIR, exist_ok=True)

# ==============================
# Utility
# ==============================

def clean_text(t):
    return re.sub(r"\s+", " ", t).strip().lower()


def download_pdf(url):
    try:
        name = url.split("/")[-1].split("?")[0]
        if not name.endswith(".pdf"):
            name = f"{hash(url)}.pdf"

        path = os.path.join(PDF_DIR, name)

        if os.path.exists(path):
            return path

        r = requests.get(url, timeout=20)
        with open(path, "wb") as f:
            f.write(r.content)

        return path
    except:
        return None


# ==============================
# Core PDF Extractor
# ==============================

def extract_from_pdf(pdf_url):
    result = {
        "salary": "",
        "qualification": "",
        "age_limit": "",
        "vacancy": "",
        "last_date": ""
    }

    pdf_path = download_pdf(pdf_url)
    if not pdf_path:
        return result

    try:
        text = extract_text(pdf_path)
        text = clean_text(text)

        # -------- Salary --------
        sal = re.findall(r"₹\s?\d{4,6}(?:\s?-\s?₹?\d{4,6})?", text)
        if sal:
            result["salary"] = sal[0]

        # -------- Qualification --------
        quals = ["10th", "12th", "iti", "diploma", "graduate", "b.sc", "ba", "b.tech", "engineering"]
        for q in quals:
            if q in text:
                result["qualification"] = q
                break

        # -------- Age --------
        age = re.findall(r"\b(\d{2}\s?-\s?\d{2})\b", text)
        if age:
            result["age_limit"] = age[0].replace(" ", "")

        # -------- Vacancy --------
        vac = re.findall(r"\b(total\s+)?vacanc(?:y|ies)\s*[:\-]?\s*(\d{1,5})", text)
        if vac:
            result["vacancy"] = vac[0][1]
        else:
            nums = re.findall(r"\b\d{2,5}\b", text)
            if nums:
                result["vacancy"] = nums[0]

        # -------- Last Date --------
        date = re.findall(r"\b\d{1,2}/\d{1,2}/\d{4}\b", text)
        if date:
            result["last_date"] = date[0]

    except:
        pass

    return result


# ==============================
# Helper: find PDF links in HTML
# ==============================

def find_pdf_links(html):
    links = re.findall(r'href=["\'](.*?\.pdf)["\']', html, re.I)
    return list(set(links))

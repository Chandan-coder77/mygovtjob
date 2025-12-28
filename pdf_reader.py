import re
import requests
from io import BytesIO
from PyPDF2 import PdfReader

def read_pdf(url):
    try:
        file = requests.get(url, timeout=20).content
        pdf = PdfReader(BytesIO(file))
        text=""
        for page in pdf.pages:
            text+=page.extract_text()+" "

        # Extract fields from PDF --------------------------------
        vacancy = re.search(r"(\d{2,6})\s*(Posts|Vacancies)",text,re.I)
        qualification = re.search(r"(10th|12th|Diploma|ITI|Graduate|Post\s?Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BCA|MCA|B\.A|M\.A|PhD)",text,re.I)
        salary = re.search(r"₹\s?\d+.*?(\d+)?",text)
        age = re.search(r"Age\s*Limit.*?(\d{1,2}.?\d{1,2})",text,re.I)
        last = re.search(r"(Last\s*Date|Apply\s*Before).*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",text)

        return {
            "vacancies": vacancy.group(1) if vacancy else "Not Mentioned",
            "qualification": qualification.group(0) if qualification else "Check Notification",
            "salary": salary.group(0) if salary else "As per Govt Rules",
            "age_limit": age.group(0).replace("Age Limit","").strip() if age else "18+",
            "last_date": last.group(2) if last else "Not Mentioned"
        }

    except Exception as e:
        print("PDF read error:",e)
        return None

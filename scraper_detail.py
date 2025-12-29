import requests, bs4, json, re, datetime
from pdfminer.high_level import extract_text

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# ============== AI MEMORY LEARNING ENGINE ============= #

def learn_pattern(key, sample):
    try:
        mem = json.load(open("ai_memory.json"))
        if sample not in mem.get(key, []):
            mem[key].append(sample)
            open("ai_memory.json","w").write(json.dumps(mem,indent=4))
    except:
        pass

# ============== PDF READING FUNCTION ============= #

def read_pdf(url):
    try:
        file = requests.get(url, timeout=12).content
        open("temp.pdf", "wb").write(file)
        text = extract_text("temp.pdf")[:4000]   # avoid heavy length
        return text
    except:
        return ""

# ============== EXTRACT JOB INFORMATION ============= #

def extract_details(url):
    try:
        html = requests.get(url, headers=headers, timeout=12).text
        soup = bs4.BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)

        # Auto-detect PDF link
        pdf = soup.find("a", href=lambda x: x and x.endswith(".pdf"))
        if pdf:
            text += read_pdf(pdf.get("href"))

        # Extract fields
        vacancies = re.search(r"(\d{1,6})\s+Posts?", text, re.I)
        qualification = re.search(r"(10th|12th|Diploma|ITI|Graduate|Post Graduate|B\.?Tech|M\.?Tech|MBA|BSC|MSC|BA|MA|MCA|PhD)", text, re.I)
        salary = re.search(r"(₹\s?\d{4,6}.*?\d{4,6}|₹\s?\d{4,6})", text)
        age_limit = re.search(r"Age.*?(\d{1,2}.*?Years?)", text, re.I)
        last_date = re.search(r"Last\s*Date.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})", text)

        info = {
            "vacancies": vacancies.group(1) if vacancies else "Not Mentioned",
            "qualification": qualification.group(1) if qualification else "Check Notification",
            "salary": salary.group(1) if salary else "As per Govt Rules",
            "age_limit": age_limit.group(1) if age_limit else "18+",
            "last_date": last_date.group(1) if last_date else "Not Mentioned"
        }

        # ========== AI LEARNING (Patterns Storage) ========== #
        learn_pattern("vacancy_patterns", info["vacancies"])
        learn_pattern("qualification_patterns", info["qualification"])
        learn_pattern("salary_patterns", info["salary"])
        learn_pattern("age_patterns", info["age_limit"])
        learn_pattern("lastdate_patterns", info["last_date"])

        return info

    except Exception as e:
        print("ERROR DETAIL:", e)
        return {
            "vacancies":"N/A",
            "qualification":"Check Notification",
            "salary":"As per Govt Rules",
            "age_limit":"18+",
            "last_date":"Not Mentioned"
        }


# ============== MAIN RUN PROCESS ============= #

links = json.load(open("jobs_temp.json"))   # fast scraper output
final = []

for i, job in enumerate(links[:25]):  # limit for speed - later remove to unlimited
    print(f"🔍 Extracting ({i+1}) =>", job["title"])
    info = extract_details(job["apply_link"])
    job.update(info)
    final.append(job)

open("jobs_details.json","w").write(json.dumps(final, indent=4))
print("\n✅ JOB DETAILS SAVED — jobs_details.json")

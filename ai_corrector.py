import json, re, requests
from bs4 import BeautifulSoup
from value_extractor import extract_values

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def fix_job(job):
    # Load full page again for deeper extraction
    try:
        r = requests.get(job["apply_link"], headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ").lower()

        # --- Extract missing values using patterns ---
        if not job["qualification"]:
            if "10th" in text: job["qualification"] = "10th"
            elif "12th" in text: job["qualification"] = "12th"
            elif "iti" in text: job["qualification"] = "ITI"
            elif "diploma" in text: job["qualification"] = "Diploma"
            elif "engineer" in text or "b.tech" in text: job["qualification"] = "Engineering"
            elif "graduate" in text: job["qualification"] = "Graduate"

        if not job["salary"] or re.match(r"20\d\d", job["salary"]):
            sal = re.findall(r'₹\s?\d{4,7}', text)
            if sal: job["salary"] = sal[0]

        date = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text)
        if date: job["last_date"] = date[-1]

        vac = re.findall(r'\b\d{2,5}\b', text)
        if vac: job["vacancy"] = vac[0]

        # final structured correction
        return extract_values(job)

    except:
        return job


# MAIN PROCESS
with open("jobs.json","r",encoding="utf-8") as f: data=json.load(f)

clean=[]
for j in data:
    if not any(x in j["title"].lower() for x in ["admit card","result","answer key"]):
        clean.append(fix_job(j))

with open("jobs.json","w",encoding="utf-8") as f:
    json.dump(clean,f,indent=4,ensure_ascii=False)

print("\n🔄 AI Correction Completed!")
print("📌 Irrelevant posts removed + data enriched successfully.\n")

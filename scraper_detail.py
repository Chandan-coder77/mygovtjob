import requests, bs4, json, re, datetime, os

# ========== USER-AGENT (Permanent your preferred) ==========
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# ========== Initialize AI Memory ==========
if not os.path.exists("ai_memory.json"):
    data = {
        "qualification_patterns": [],
        "salary_patterns": [],
        "age_patterns": [],
        "lastdate_patterns": [],
        "vacancy_patterns": [],
        "learn_count": 0
    }
    open("ai_memory.json","w").write(json.dumps(data,indent=4))

ai = json.load(open("ai_memory.json"))

def learn(key,val):
    if val not in ["Not Found","",None] and val not in ai[key]:
        ai[key].append(val)
        ai["learn_count"] += 1


# ========== Extract function ==========
def extract_details(html):
    soup = bs4.BeautifulSoup(html,"html.parser")
    text = soup.get_text(" ",strip=True)

    def find(regex):
        m = re.search(regex,text,re.I)
        return m.group(1) if m else "Not Found"

    data = {
        "vacancy": find(r"(\d{1,4})\s*(Posts?|Vacancy|Seats)"),
        "qualification": find(r"(10th|12th|Diploma|ITI|Graduate|B\.?Tech|M\.?Tech|MBA|BA|MA|MCA|BSC|MSC)"),
        "salary": find(r"(₹\s?\d{4,7}|Rs\.?\s?\d{4,7})"),
        "age_limit": find(r"Age.*?(\d+.*?Years|\d+-\d+)"),
        "last_date": find(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})")
    }

    for k,v in data.items():
        learn(f"{k}_patterns",v)

    return data


# ========== Multi Source Extractor ==========
def process_job(job):
    try:
        print(f"\n🚀 Processing: {job['title']}  | {job['apply_link']}")
        html = requests.get(job['apply_link'],headers=headers,timeout=10).text
        job.update(extract_details(html))
        job["updated"] = str(datetime.datetime.now())
        return job
    except Exception as e:
        job["error"] = str(e)
        return job


# ========== Read & Update All Jobs ==========
jobs = json.load(open("jobs.json"))
output = []

for job in jobs:      # FULL JOB PROCESSING ENABLED
    updated_job = process_job(job)
    output.append(updated_job)

open("jobs.json","w").write(json.dumps(output,indent=4))
open("ai_memory.json","w").write(json.dumps(ai,indent=4))

print("\n==============================")
print("✨ MULTI-SOURCE AI UPDATE DONE")
print("📌 Learned Patterns Count:", ai["learn_count"])
print("==============================")

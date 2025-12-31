import requests, json, re
from bs4 import BeautifulSoup
from value_extractor import extract_values

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

URLS = ["https://www.freejobalert.com/"]
jobs = []

# =========================
# 1) Homepage Scraper
# =========================
def scrape_homepage(url):
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.select("a[href*='articles'],a[href*='recruit'],a[href*='online'],a[href*='posts']")
    print(f"Found raw links: {len(links)}")

    for a in links[:60]:
        title = a.get_text(strip=True)
        link = a.get("href")
        if not link.startswith("http"):
            link = url + link

        jobs.append({
            "title": title,
            "apply_link": link,
            "qualification": "",
            "salary": "",
            "age_limit": "",
            "vacancy": "",
            "last_date": ""
        })


# ========================================
# 2) Deep Scraper — TABLE + TEXT Extractor
# ========================================
def extract_from_tables(soup, job):
    tables = soup.find_all("table")
    
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = [c.get_text(" ", strip=True).lower() for c in row.find_all(["td", "th"])]

            line = " ".join(cols)

            if "qualification" in line and not job["qualification"]:
                job["qualification"] = line.replace("qualification", "").strip()

            if "salary" in line and not job["salary"]:
                salary = re.findall(r'\d{4,8}', line)
                if salary: job["salary"] = f"₹{salary[0]}"

            if "age" in line and not job["age_limit"]:
                age = re.findall(r'\d{1,2}-\d{1,2}', line)
                if age: job["age_limit"] = age[0]

            if "vacancy" in line and not job["vacancy"]:
                vac = re.findall(r'\b\d{1,5}\b', line)
                if vac: job["vacancy"] = vac[0]

            if "last" in line and "date" in line and not job["last_date"]:
                date = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', line)
                if date: job["last_date"] = date[0]


# ========================================
# 3) Deep Scraper From Paragraphs
# ========================================
def extract_from_text(text, job):

    if not job["qualification"]:
        if "10th" in text: job["qualification"] = "10th"
        elif "12th" in text: job["qualification"] = "12th"
        elif "iti" in text: job["qualification"] = "ITI"
        elif "diploma" in text: job["qualification"] = "Diploma"
        elif "b.tech" in text or "engineer" in text: job["qualification"] = "Engineering"
        elif "graduate" in text: job["qualification"] = "Graduate"

    if not job["salary"]:
        sal = re.findall(r'₹\s?\d{4,8}', text)
        if sal: job["salary"] = sal[0]

    if not job["age_limit"]:
        age = re.findall(r'\d{1,2}-\d{1,2}', text)
        if age: job["age_limit"] = age[0]

    if not job["vacancy"]:
        vac = re.findall(r'\b\d{2,5}\b', text)
        if vac: job["vacancy"] = vac[0]

    if not job["last_date"]:
        date = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text)
        if date: job["last_date"] = date[-1]

    return job


# ========================================
# 4) Final Job Scraper
# ========================================
def scrape_details():
    for job in jobs:
        try:
            r = requests.get(job["apply_link"], headers=headers, timeout=25)
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text(" ", strip=True).lower()

            extract_from_tables(soup, job)       # NEW 🔥 table based extraction
            extract_from_text(text, job)         # backup text extraction
            job.update(extract_values(job))      # AI pattern formatter

        except Exception as e:
            print("skip:", job["title"])
            continue


# RUN MAIN
for site in URLS:
    scrape_homepage(site)

scrape_details()

unique = {i["apply_link"]: i for i in jobs}
final = list(unique.values())

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(final, f, indent=4, ensure_ascii=False)

print("\n🚀 Stage-4 Scraper Completed (TABLE + TEXT Extraction Mode ON)")
print("Jobs saved:", len(final))

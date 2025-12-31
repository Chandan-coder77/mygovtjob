import requests, json, re
from bs4 import BeautifulSoup
from value_extractor import extract_values

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

URL = "https://www.freejobalert.com/"
jobs = []

# Fetch homepage links
def scrape_homepage():
    r = requests.get(URL, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.select("a[href*='articles'],a[href*='recruit'],a[href*='online'],a[href*='posts']")
    print(f"Found raw links: {len(links)}")

    for a in links[:60]:                              # Limit for safe run
        title = a.get_text(strip=True)
        link = a.get("href")
        if not title or len(title) < 8: continue
        if not link.startswith("http"): link = URL + link

        jobs.append({
            "title": title.strip(),
            "apply_link": link,
            "qualification": "",
            "salary": "",
            "age_limit": "",
            "vacancy": "",
            "last_date": ""
        })


# Detailed scrape of each job
def extract_job_detail(job):
    try:
        r = requests.get(job["apply_link"], headers=headers, timeout=25)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ").lower()

        # Basic extraction
        job["salary"] = re.findall(r'₹\s?\d{4,8}', text)[0] if re.findall(r'₹\s?\d{4,8}', text) else ""
        job["age_limit"] = re.findall(r'\d{1,2}-\d{1,2}|\d{1,2}\s?to\s?\d{1,2}', text)[0] if re.findall(r'\d{1,2}-\d{1,2}|\d{1,2}\s?to\s?\d{1,2}', text) else ""
        job["vacancy"] = re.findall(r'\b\d{2,5}\b', text)[0] if re.findall(r'\b\d{2,5}\b', text) else ""
        job["last_date"] = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text)[0] if re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text) else ""

        details = extract_values(job)
        job.update(details)

        return job
    except:
        return job


# Run scraping
scrape_homepage()
detailed = [extract_job_detail(j) for j in jobs]

# Auto remove duplicates by apply_link
unique = {i['apply_link']: i for i in detailed}
final = list(unique.values())

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(final, f, indent=4, ensure_ascii=False)

print("\n🚀 Smart Scraper Updated (Clean + Extract + Unique)")
print(f"Jobs saved: {len(final)}\n")

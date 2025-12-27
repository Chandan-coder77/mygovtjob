import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

def extract_block(text):
    blocks = re.split(r'\d{1,2}/\d{1,2}/\d{4}', text)
    return blocks[:20]  # avoid large dump

def scrape(url):
    print("Scraping:", url)
    jobs = []

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)

            if not any(x in title.lower() for x in ["recruit", "online", "form", "vacancy", "post"]):
                continue

            job_link = a['href']
            if job_link.startswith("/"):
                job_link = url + job_link

            try:
                page = requests.get(job_link, headers=headers, timeout=10)
                inner = BeautifulSoup(page.text, "html.parser")
                text = clean_text(inner.get_text(" "))

                # Split into separate job sections
                blocks = extract_block(text)

                for block in blocks:
                    jobs.append({
                        "title": (title[:80]+"...") if len(title)>80 else title,
                        "vacancies": extract(r'(\d+)\s*Posts?', block),
                        "qualification": extract(r'Qualification:?(.{0,80})', block),
                        "salary": extract(r'Salary:?(.{0,60})', block),
                        "age_limit": extract(r'Age\s*Limit:?(.{0,40})', block),
                        "last_date": extract(r'Last\s*Date:?(.{0,30})', block),
                        "apply_link": job_link,
                        "source": url
                    })

            except:
                pass

    except Exception as e:
        print("ERROR:", e)

    return jobs


def extract(pattern, text):
    m = re.search(pattern, text, re.I)
    return clean_text(m.group(1)) if m else "N/A"

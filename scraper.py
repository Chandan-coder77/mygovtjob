import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# ---------- Helper Extract Function ----------
def extract(pattern, text):
    if not text:
        return "Not Available"
    match = re.search(pattern, text, re.I)
    return match.group(1).strip() if match else "Not Available"


def scrape(url):
    print("Scraping:", url)
    jobs = []

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # find job post links
        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)

            # only valid job links filter
            if len(title) < 6 or "notification" not in title.lower() and "recruit" not in title.lower():
                continue

            job_link = a['href']
            if job_link.startswith("/"):
                job_link = url + job_link

            # 2nd page open
            try:
                job_page = requests.get(job_link, headers=headers, timeout=10)
                inner = BeautifulSoup(job_page.text, "html.parser")
                text = inner.get_text(" ", strip=True)

                vacancy = extract(r"(\d+)\s*Posts?", text)
                qualification = extract(r"Qualification:?(.+?)Age", text)
                salary = extract(r"Salary:?(.+?)Age", text)
                age = extract(r"Age\s*Limit:?(.+?)Last", text)
                last_date = extract(r"Last\s*Date:?(.+?)\s", text)

                jobs.append({
                    "title": title,
                    "vacancies": vacancy,
                    "qualification": qualification,
                    "salary": salary,
                    "age_limit": age,
                    "last_date": last_date,
                    "apply_link": job_link,
                    "source": url
                })

            except:
                pass

    except Exception as e:
        print("Error:", e)

    return jobs

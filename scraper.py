import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def extract_text(soup, keywords):
    for tag in soup.find_all(["p", "li", "span", "div"]):
        text = tag.get_text(strip=True).lower()
        for key in keywords:
            if key in text:
                return tag.get_text(strip=True)
    return "Not Available"

def clean_title(title):
    title = re.sub(r"Recruitment|Apply Online|Notification|Admit Card|Result", "", title, flags=re.I)
    return title.strip("-: ")

def scrape(url):
    try:
        print("Scraping:", url)
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        jobs = []
        links = soup.find_all("a", href=True)

        for link in links:
            title = clean_title(link.get_text(strip=True))
            if len(title) < 4: 
                continue

            job_link = link['href']
            if job_link.startswith("/"):
                job_link = url.rstrip("/") + job_link

            job_page = requests.get(job_link, headers=headers, timeout=10)
            inner = BeautifulSoup(job_page.text, "html.parser")

            vacancies = extract_text(inner, ["vacancy", "post", "posts"])
            qualification = extract_text(inner, ["qualification", "educational"])
            salary = extract_text(inner, ["salary", "pay"])
            age = extract_text(inner, ["age limit", "age"])
            last_date = extract_text(inner, ["last date", "closing date", "apply till"])

            jobs.append({
                "title": title,
                "vacancies": vacancies,
                "qualification": qualification,
                "salary": salary,
                "age_limit": age,
                "last_date": last_date,
                "apply_link": job_link,
                "source": url,
            })

        return jobs

    except Exception as e:
        print("Error scraping:", url, e)
        return []

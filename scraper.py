import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def extract_field(text, key):
    """ Smart extractor: Vacancy, Qualification, Age, Salary, Dates """
    text = text.replace("\n", " ")
    patterns = {
        "vacancy": r"(\d+\s*posts?|\d+ vacancies|\d+\s*post)",
        "qualification": r"Qualification[:\-]?\s*([^,.;\n]+)",
        "age": r"Age\s*Limit[:\-]?\s*([^,.;\n]+)",
        "salary": r"Salary[:\-]?\s*([^,.;\n]+)",
        "last_date": r"Last\s*Date[:\-]?\s*([^,.;\n]+)"
    }

    match = re.search(patterns.get(key, ""), text, re.IGNORECASE)
    return match.group(1).strip() if match else "Updating Soon"

def scrape(url):
    print("Scraping:", url)
    jobs = []
    try:
        r = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")

        cards = soup.select("article, .job-card, .post-list, li, .entry-content")
        for card in cards[:40]:  # 40 job limit per site
            text = card.get_text(" ", strip=True)

            title = card.find("a").get_text(strip=True) if card.find("a") else None
            link = card.find("a")["href"] if card.find("a") else url

            if not title or len(title) < 8:
                continue

            job = {
                "title": title,
                "vacancies": extract_field(text, "vacancy"),
                "qualification": extract_field(text, "qualification"),
                "age": extract_field(text, "age"),
                "salary": extract_field(text, "salary"),
                "last_date": extract_field(text, "last_date"),
                "apply_link": link,
                "source": url
            }

            jobs.append(job)

    except Exception as e:
        print("Error:", e)

    return jobs

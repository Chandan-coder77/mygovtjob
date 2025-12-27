import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def scrape(url):
    print("\n📌 Scraping:", url)

    try:
        r = requests.get(url, headers=headers, timeout=15)
        print("➡ Status:", r.status_code)

        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, "html.parser")

        # FreeJobAlert jobs mostly inside tables
        rows = soup.select("table a, .post a, a[href*='recruit'], a[href*='job']")
        print("🔎 Links Found:", len(rows))

        jobs = []

        for a in rows[:50]:     # limit 50 for test
            title = a.get_text(strip=True)
            link = a.get("href")

            if not title or len(title) < 6:
                continue

            if link.startswith("/"):
                link = url.rstrip("/") + link

            jobs.append({
                "title": title,
                "vacancies": "Fetching Soon",
                "qualification": "Fetching Soon",
                "salary": "Fetching Soon",
                "age_limit": "Fetching Soon",
                "last_date": "Fetching Soon",
                "apply_link": link,
                "source": url
            })

        print("✔ Jobs Extracted:", len(jobs))
        return jobs

    except Exception as e:
        print("❌ Error:", e)
        return []

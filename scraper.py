# scraper.py
# ------------------------------------------
# v2.0 - Advanced Smart Scraper
# Works with FreeJobAlert categories & posts
# ------------------------------------------

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def extract_short(text):
    """Long qualification text को छोटा और साफ format में convert करता है"""
    if not text:
        return "N/A"
    text = text.replace("\n", " ").strip()
    return text[:180] + "..." if len(text) > 180 else text


def scrape_freejobalert():
    url = "https://www.freejobalert.com/"
    print(f"🔍 Fetching jobs from: {url}")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # Page से top government notifications पकड़ना
    for box in soup.select(".entry-content ul li a")[:40]:  # limit to avoid overload
        title = box.get_text(strip=True)
        link = box.get("href")

        # Vacancy number निकालने की कोशिश
        vacancy = "".join([x for x in title if x.isdigit()]) or "N/A"

        job_detail = {"qualification": "N/A", "salary": "N/A", "age_limit": "N/A"}

        # Job page open for deep details
        try:
            page = requests.get(link, headers=headers, timeout=10)
            deep = BeautifulSoup(page.text, "html.parser")

            text = deep.get_text(" ", strip=True)

            # Auto extract keywords
            for line in text.split():
                if "Age" in text[:500]:
                    job_detail["age_limit"] = "Found"  # later upgrade to exact value
                if "Salary" in text[:500]:
                    job_detail["salary"] = "Available"
                if "Qualification" in text or "Graduate" in text:
                    job_detail["qualification"] = extract_short(text[text.index("Qualification"):][:200])

        except:
            pass

        jobs.append({
            "title": title,
            "vacancies": vacancy,
            "qualification": job_detail["qualification"],
            "salary": job_detail["salary"],
            "age_limit": job_detail["age_limit"],
            "last_date": "Check site",   # Next version auto extract
            "apply_link": link,
            "source": url
        })

    return jobs

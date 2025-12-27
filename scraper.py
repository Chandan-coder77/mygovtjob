import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# remove extra garbage
def clean_text(text):
    text = re.sub(r"\s+", " ", text).strip()
    remove_words = [
        "Reminder", "Others", "Eligibility", "Syllabus", "Exam", "Download",
        "Notification", "More Information", "Overview"
    ]
    for w in remove_words:
        text = text.replace(w, "")
    return text[:80] + "..." if len(text) > 80 else text

# extract field better
def find(pattern, text):
    m = re.search(pattern, text, re.I)
    if m:
        return clean_text(m.group(1))
    return "N/A"

def scrape(url):
    print("Scraping:", url)
    jobs = []

    try:
        home = requests.get(url, headers=headers, timeout=10).text
        soup = BeautifulSoup(home, "html.parser")

        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            if not re.search(r"(recruit|vacan|apply|post|form|job)", title, re.I):
                continue

            link = a['href']
            if link.startswith("/"):
                link = url + link

            try:
                job_html = requests.get(link, headers=headers, timeout=10).text
                txt = clean_text(BeautifulSoup(job_html, "html.parser").get_text(" "))

                job = {
                    "title": title[:70],
                    "vacancies": find(r"(\d{1,5})\s+Posts?", txt),
                    "qualification": find(r"Qualification:?(.{0,120})", txt),
                    "salary": find(r"Salary:?(.{0,120})", txt),
                    "age_limit": find(r"Age\s*Limit:?(.{0,60})", txt),
                    "last_date": find(r"Last\s*Date:?(.{0,60})", txt),
                    "apply_link": link,
                    "source": url
                }

                jobs.append(job)

            except Exception:
                pass

    except:
        pass

    return jobs

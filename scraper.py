import requests, json, datetime, bs4
from parser import extract_qualification, extract_salary, extract_age, extract_last_date

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}

def crawl_site(url):
    try:
        html = requests.get(url, headers=headers, timeout=20).text
        soup = bs4.BeautifulSoup(html, "html.parser")
        links = soup.find_all("a")

        jobs = []
        for a in links[:80]:  # limit to 80 to avoid noise
            text = a.get_text(" ", strip=True)

            if any(x in text.lower() for x in ["recruitment","vacancy","online","form","notification"]):
                
                job_url = a.get("href")
                if not job_url: continue
                if not job_url.startswith("http"):
                    job_url = url.rstrip("/") + "/" + job_url.lstrip("/")

                job = {
                    "title": text,
                    "qualification": extract_qualification(text),
                    "salary": extract_salary(text),
                    "age_limit": extract_age(text),
                    "last_date": extract_last_date(text),
                    "apply_link": job_url,
                    "source": url,
                    "updated": str(datetime.datetime.now())
                }
                jobs.append(job)

        return jobs

    except Exception as e:
        print("Error scraping:", url, e)
        return []

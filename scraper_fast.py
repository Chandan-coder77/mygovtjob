import requests, bs4, json

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

SITES = [
    "https://www.freejobalert.com/",
    "https://www.sarkariresult.com/latestjob/",
    "https://ssc.nic.in/",
    "https://upsc.gov.in/recruitment/recruitment",
    "https://rrbcdg.gov.in/employment-notices.php",
    "https://sbi.co.in/web/careers"
]

def scrape(url):
    try:
        html = requests.get(url, headers=headers, timeout=12).text
        soup = bs4.BeautifulSoup(html, "html.parser")
        jobs = []

        for a in soup.find_all("a")[:120]:
            title = a.get_text(" ", strip=True)
            link = a.get("href")

            if not link or len(title) < 8: continue
            if not any(k in title.lower() for k in ["recruit","job","vacancy","apply","online","notification"]): continue

            full = link if link.startswith("http") else url + link

            jobs.append({"title": title, "apply_link": full, "source": url})
        return jobs
    except:
        return []

all_data = []
for site in SITES:
    print("Scanning:", site)
    all_data += scrape(site)

json.dump(all_data, open("jobs_temp.json","w"), indent=4)
print("Links:", len(all_data))

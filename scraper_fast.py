import requests, bs4, json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

SITES = [
    "https://www.freejobalert.com/",
    "https://www.sarkariresult.com/latestjob/"
]

LIMIT = 5   # Fast test mode

def scrape(url):
    try:
        html = requests.get(url, headers=headers, timeout=10).text
        soup = bs4.BeautifulSoup(html, "html.parser")
        jobs = []

        for a in soup.find_all("a")[:120]:
            title = a.get_text(" ", strip=True)
            link = a.get("href")

            if not title or not link: continue
            if not any(x in title.lower() for x in ["job","recruit","apply","vacancy","notification"]): continue

            full = link if link.startswith("http") else url + link
            jobs.append({ "title": title, "apply_link": full, "source": url })

            if len(jobs) >= LIMIT: break

        return jobs
    except:
        return []


# Run and save
data=[]
for site in SITES:
    print("Scanning:",site)
    data += scrape(site)

json.dump(data, open("jobs.json","w"), indent=4)
print("🔥 Fast Test Links Saved:", len(data))

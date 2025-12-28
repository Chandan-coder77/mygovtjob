import requests, bs4, json, time

headers = {
 "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def fetch_links(url):
    print("SCRAPING:", url)
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        data=[]

        for a in soup.find_all("a")[:200]:
            title = a.get_text(" ", strip=True)
            link = a.get("href")

            if not link or len(title) < 8: 
                continue

            keywords=["recruit","job","vacancy","apply","notification","form"]
            if not any(k in title.lower() for k in keywords):
                continue

            full = link if link.startswith("http") else url.rstrip("/")+"/"+link.lstrip("/")

            data.append({
                "title": title,
                "apply_link": full,
                "source": url
            })

        return data

    except Exception as e:
        print("ERROR:", url, e)
        return []


sites=open("sources.txt").read().splitlines()
all=[]

for s in sites:
    all += fetch_links(s)
    time.sleep(2) # GitHub timeout safe

open("jobs.links.json","w").write(json.dumps(all, indent=4, ensure_ascii=False))
print("TOTAL LINKS SAVED:", len(all))

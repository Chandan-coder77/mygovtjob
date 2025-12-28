import requests, bs4, json, datetime

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def crawl(url):
    try:
        html = requests.get(url,headers=headers,timeout=15).text
        soup = bs4.BeautifulSoup(html,"html.parser")

        links=[]
        for a in soup.find_all("a")[:200]:
            name = a.get_text(" ",strip=True)
            href = a.get("href")

            if not href or len(name)<6: continue
            key = name.lower()

            if any(x in key for x in ["recruit","vacancy","post","online","form","job","notice","notification"]):
                full = href if href.startswith("http") else url.rstrip("/")+"/"+href.lstrip("/")
                links.append({
                    "title":name,
                    "apply_link":full,
                    "source":url,
                    "updated":str(datetime.datetime.now())
                })

        return links
    except:
        return []

sites=open("sources.txt").read().splitlines()
all_links=[]

for s in sites:
    print("Scraping:",s)
    all_links+=crawl(s)

open("jobs.links.json","w").write(json.dumps(all_links,indent=4))
print("LINKS SAVED:",len(all_links))

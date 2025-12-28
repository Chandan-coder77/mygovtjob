import requests, bs4, json, datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def load_sources():
    return [x.strip() for x in open("sources.txt").read().splitlines() if x.strip()]

def quick_scrape(url):
    try:
        html = requests.get(url, headers=headers, timeout=10).text
        soup = bs4.BeautifulSoup(html, "html.parser")

        jobs=[]
        for a in soup.find_all("a")[:80]:  
            title=a.get_text(" ",strip=True)
            link=a.get("href")

            if not link or len(title)<8: continue
            if not any(x in title.lower() for x in ["recruit","vacancy","apply","form","notification","job"]): continue

            full = link if link.startswith("http") else url + link

            jobs.append({
                "title":title,
                "apply_link":full,
                "source":url,
                "updated":str(datetime.datetime.now())
            })

        return jobs
    except:
        return []

all=[]
for site in load_sources():
    print("FAST:",site)
    all+=quick_scrape(site)

try:
    old=json.load(open("jobs_links.json"))
except:
    old=[]

titles=set(i['title'] for i in old)
final = old+[j for j in all if j['title'] not in titles]

open("jobs_links.json","w").write(json.dumps(final,indent=3))
print("Saved Links:",len(final))

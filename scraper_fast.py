import requests, bs4, json

# --------- FAST TEST MODE ---------
# अभी सिर्फ 1 साइट (FreeJobAlert)
# बाद में हम +10 sites add करेंगे
SITES = [
    "https://www.freejobalert.com/"
]

headers={
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

jobs=[]

for url in SITES:
    print("SCRAPING:",url)
    try:
        html=requests.get(url,headers=headers,timeout=10).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        links=soup.find_all("a")

        for a in links[:10]:  # << TEST: only 10 links fetch
            title=a.get_text(strip=True)
            link=a.get("href")

            if not link or len(title)<6: continue
            if not ("recruit" in title.lower() or "job" in title.lower() or "apply" in title.lower() or "notification" in title.lower()): continue

            full = link if link.startswith("http") else url+link

            jobs.append({
                "title":title,
                "apply_link":full,
                "source":url
            })

    except Exception as e:
        print("ERR:",e)

open("jobs.json","w").write(json.dumps(jobs,indent=4))
print("\nFAST SCRAPE COMPLETE —",len(jobs),"links saved")
print("Next step → scraper_detail.py auto extract करेगा")

import requests, bs4, json

headers={
 "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

sites=open("sources.txt").read().splitlines()
all_links=[]

def collect(url):
    try:
        print("Crawling:",url)
        html=requests.get(url,headers=headers,timeout=15).text
        soup=bs4.BeautifulSoup(html,"html.parser")

        for a in soup.find_all("a")[:200]:
            title=a.get_text(" ",strip=True)
            link=a.get("href")

            if link and len(title)>6 and any(x in title.lower() for x in ["recruit","vacancy","job","apply","form","notification"]):
                full=link if link.startswith("http") else url.rstrip('/')+'/'+link.lstrip('/')
                all_links.append({"title":title,"apply_link":full,"source":url})

    except Exception as e:
        print("ERROR:",url,e)

for s in sites:
    collect(s)

open("jobs.links.json","w").write(json.dumps(all_links,indent=4))
print("Saved Links:",len(all_links))

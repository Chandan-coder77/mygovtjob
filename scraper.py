import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def find(pattern, text, length=80):
    m = re.search(pattern, text, re.I)
    if m:
        t = clean(m.group(1))
        return t[:length] + "..." if len(t) > length else t
    return "N/A"

def scrape(url):
    print("Scraping:", url)
    jobs=[]
    
    try:
        html=requests.get(url,headers=headers,timeout=10).text
        soup=BeautifulSoup(html,"html.parser")

        for a in soup.find_all("a",href=True):
            title=a.get_text(strip=True)

            if not re.search(r"(recruit|vacan|apply|post|form|job|online)",title,re.I):
                continue

            link=a['href']
            if link.startswith("/"): link=url+link

            try:
                page=requests.get(link,headers=headers,timeout=10).text
                full=clean(BeautifulSoup(page,"html.parser").get_text(" "))

                jobs.append({
                    "title": title[:70],
                    "vacancies": find(r'(\d{1,5})\s+Posts?',full),
                    "qualification": find(r'Qualification:?(.{0,120})',full),
                    "salary": find(r'Salary:?(.{0,80})',full),
                    "age_limit": find(r'Age\s*Limit:?(.{0,60})',full),
                    "last_date": find(r'Last\s*Date:?(.{0,40})',full),
                    "apply_link": link,
                    "source": url
                })

            except: pass

    except: pass

    return jobs

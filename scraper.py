import requests, json, datetime, bs4
from parser import extract_qualification, extract_salary, extract_age

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

SITES = [
    "https://www.freejobalert.com/",
    "https://www.sarkariresult.com/",
    "https://www.sarkariresult.com/latestjob/",
    "https://www.ncs.gov.in/",
    "https://www.ssc.nic.in/",
    "https://www.upsc.gov.in/recruitment/recruitment",
    "https://www.rrbcdg.gov.in/employment-notices.php",
    "https://www.ibps.in/",
    "https://bankofindia.co.in/Careers",
    "https://sbi.co.in/web/careers",
    "https://www.india.gov.in/my-government/jobs",
    "https://www.drdo.gov.in/careers",
    "https://joinindianarmy.nic.in/",
    "https://www.isro.gov.in/Careers",
]   # future you can add 50+ sites here easily

def scrap(url):
    try:
        html=requests.get(url,headers=headers,timeout=20).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        links=soup.find_all("a")

        jobs=[]
        for a in links[:60]:
            text=a.get_text(" ",strip=True)
            if any(x in text.lower() for x in ["recruitment","vacancy","online","form","result","admit","notification"]):
                job_page=a.get("href")
                if job_page and len(text)>7:
                    job={
                        "title":text.replace("Recruitment","").strip(),
                        "apply_link":job_page if job_page.startswith("http") else url+job_page,
                        "qualification":extract_qualification(text),
                        "salary":extract_salary(text),
                        "age_limit":extract_age(text),
                        "category":"Govt Job",
                        "source":url.split("//")[1].split("/")[0],
                        "updated":str(datetime.datetime.now())
                    }
                    jobs.append(job)
        return jobs

    except Exception as e:
        print("Error:",url,e)
        return []

all_jobs=[]
for site in SITES:
    print("Scraping →",site)
    all_jobs+=scrap(site)

print("Total Scraped:",len(all_jobs))

try:
    old=json.load(open("jobs.json"))
except:
    old=[]

titles=set(i["title"] for i in old)
final = old+[j for j in all_jobs if j["title"] not in titles]

open("jobs.json","w").write(json.dumps(final,indent=4))
print("Saved:",len(final))

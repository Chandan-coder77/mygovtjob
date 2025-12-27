import requests, re, json, datetime, bs4
from parser import extract_qualification, extract_salary, extract_age

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# Multiple Govt Job Sources
SITES = [
"https://www.freejobalert.com/",
"https://www.sarkariresult.com/",
"https://www.sarkariresult.com/latestjob/",
"https://ssc.nic.in/",
"https://www.upsc.gov.in/recruitment/recruitment",
"https://www.rrbcdg.gov.in/employment-notices.php",
"https://sbi.co.in/web/careers",
"https://bankofindia.co.in/Careers",
"https://www.ibps.in/",
"https://www.ncs.gov.in/",
"https://www.india.gov.in/my-government/jobs",
"https://www.drdo.gov.in/careers",
"https://joinindianarmy.nic.in/",
"https://isro.gov.in/Careers",
]  # अब भी 50+ जोड़ सकते हो सिर्फ SITES में add करके

def get_details(url):
    try:
        page=requests.get(url,headers=headers,timeout=15).text
        txt=" ".join(bs4.BeautifulSoup(page,"html.parser").stripped_strings)

        vacancy=re.search(r"\d{1,5}\s?posts|\d{1,5}\s?vacancy",txt,re.I)
        lastdate=re.search(r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}",txt)

        return {
            "vacancies":vacancy.group(0) if vacancy else "Available",
            "qualification":extract_qualification(txt),
            "salary":extract_salary(txt),
            "age_limit":extract_age(txt),
            "last_date":lastdate.group(0) if lastdate else "Not Mentioned"
        }
    except:
        return {
            "vacancies":"Available",
            "qualification":"Check Notification",
            "salary":"As per Govt Rules",
            "age_limit":"18+",
            "last_date":"Not Mentioned"
        }


def scrap(url):
    try:
        html=requests.get(url,headers=headers,timeout=15).text
        soup=bs4.BeautifulSoup(html,"html.parser")
        jobs=[]

        for a in soup.find_all("a")[:100]:
            text=a.get_text(" ",strip=True)

            if any(x in text.lower() for x in ["recruit","vacancy","online","form","notice","jobs","recruitment"]):
                link=a.get("href")
                if link and len(text)>5:
                    full=link if link.startswith("http") else url+link

                    data=get_details(full)

                    jobs.append({
                        "title":text.replace("Recruitment","").strip(),
                        **data,
                        "apply_link":full,
                        "state":"India",
                        "category":"Govt Job",
                        "source":url.split("//")[1].split("/")[0],
                        "updated":str(datetime.datetime.now())
                    })
        return jobs

    except: return []


# Run Scraper
all=[]
for site in SITES:
    print("📥 Fetching →",site)
    all+=scrap(site)


try: old=json.load(open("jobs.json"))
except: old=[]

titles=set(i["title"] for i in old)
final=old+[j for j in all if j["title"] not in titles]

open("jobs.json","w").write(json.dumps(final,indent=4,ensure_ascii=False))

print("\n✔ Jobs Updated:",len(final))

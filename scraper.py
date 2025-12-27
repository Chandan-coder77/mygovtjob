import json,requests,bs4,datetime,re

print("\n🚀 Smart Govt Job Scraper (Advanced) Running...\n")

URL="https://www.freejobalert.com/"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0 Safari/537.36"}

html=requests.get(URL,headers=headers,timeout=20).text
soup=bs4.BeautifulSoup(html,"html.parser")

def detect_category(text):
    T=text.lower()
    if "bank" in T or "sbi" in T or "bob" in T or "boi" in T:return "Banking"
    if "rail" in T:return "Railway"
    if "ssc" in T:return "SSC"
    if "upsc" in T:return "UPSC"
    if "teacher" in T or "faculty" in T:return "Teaching"
    if "police" in T or "defence" in T or "army" in T:return "Defence"
    return "Latest"

jobs=[]

def fetch_details(link):
    """Post page se Qualification & Salary extract"""
    try:
        page=requests.get(link,headers=headers,timeout=20).text
        sp=bs4.BeautifulSoup(page,"html.parser")
        
        text=sp.get_text(" ").lower()

        # find qualification
        q=re.search(r'qualification[:\- ]+(.+?)\n',text)
        qualification=q.group(1).strip() if q else "Not Mentioned"

        # find salary
        s=re.search(r'salary[:\- ]+(.+?)\n',text)
        salary=s.group(1).strip() if s else "As per Notification"

        return qualification,salary
    
    except:
        return "Not Mentioned","As per Notification"


# scrape homepage table
for row in soup.select("table tbody tr")[:15]:   # first 15 jobs
    try:
        cols=row.find_all("td")
        date=cols[0].get_text(strip=True)
        org=cols[1].get_text(strip=True)
        posts=cols[2].get_text(strip=True)
        link=row.find("a")["href"]

        q,sal = fetch_details(link)  # Fetch details from inside page

        job={
            "title":org.replace("Recruitment","").strip(),   # clean title
            "vacancies":posts.replace("–","-"),
            "qualification":q,
            "age":"18+",
            "salary":sal,
            "last_date":date,
            "state":"India",
            "category":detect_category(org),
            "apply_link":link
        }
        jobs.append(job)

    except Exception as e:
        print("Error:",e)


# Merge + Save
try: old=json.load(open("jobs.json"))
except: old=[]

titles=set(i["title"] for i in old)
final = old+[j for j in jobs if j["title"] not in titles]

open("jobs.json","w").write(json.dumps(final,indent=4))

print("📁 Jobs Saved:",len(final))
print("⏳ Updated:",datetime.datetime.now())
print("✔ Done\n")

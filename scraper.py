import json,requests,bs4,datetime

print("\n🔎 Fetching Govt Jobs from FreeJobAlert...\n")

URL="https://www.freejobalert.com/"
html=requests.get(URL,headers={"User-Agent":"Mozilla/5.0"}).text
soup=bs4.BeautifulSoup(html,"html.parser")

new_jobs=[]

# Top job titles read
for li in soup.select(".menu li a")[:5]:
    title=li.get_text(strip=True)

    job={
        "title":title,
        "vacancies":"Updating...",
        "qualification":"Check Notification",
        "age":"18+",
        "salary":"As Govt Rules",
        "last_date":"Check Website",
        "state":"India",
        "category":"Central",
        "apply_link":URL
    }
    new_jobs.append(job)

# old jobs read
try:
    old=json.load(open("jobs.json"))
except:
    old=[]

titles=set(j["title"].lower() for j in old)
final=old+[j for j in new_jobs if j["title"].lower() not in titles]

open("jobs.json","w").write(json.dumps(final,indent=4))
print("📁 Total Jobs:",len(final))
print("⏳ Last Updated:",datetime.datetime.now())
print("✔ Auto Update Success!\n")

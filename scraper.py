import json, requests, bs4, datetime

print("\n🔎 Fetching Govt Jobs...\n")

URL = "https://www.ncs.gov.in/"   # Live portal
html = requests.get(URL).text
soup = bs4.BeautifulSoup(html,"html.parser")

new_jobs=[]

# Website से headings पढ़ रहे हैं (Top 5 as sample)
for h in soup.find_all(["h1","h2","h3"])[:5]:
    title = h.get_text(strip=True)

    job={
        "title":title,
        "vacancies":"Updating...",
        "qualification":"Check Official Notice",
        "age":"18+",
        "salary":"As per Govt Rules",
        "last_date":"Updating...",
        "state":"India",
        "category":"Central",
        "apply_link":URL
    }

    new_jobs.append(job)

# पहले के jobs लोड कर रहे हैं (overwrite नहीं)
try:
    old=json.load(open("jobs.json"))
except:
    old=[]

# duplicate remove
titles=set(i["title"].lower() for i in old)
final=old+[i for i in new_jobs if i["title"].lower() not in titles]

open("jobs.json","w").write(json.dumps(final,indent=4))

print("📁 Jobs Updated:",len(final))
print("⏳ Last Run:",datetime.datetime.now())
print("✔ Auto Update Complete\n")

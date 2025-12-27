import json,requests,bs4,datetime,re

print("\n🚀 Smart Govt Job Scraper Running...\n")

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

jobs=[]

# =========================================================
# SOURCE 1 — FreeJobAlert (Latest Govt Jobs)
# =========================================================
try:
    URL="https://www.freejobalert.com/"
    html=requests.get(URL,headers=headers,timeout=20).text
    soup=bs4.BeautifulSoup(html,"html.parser")

    def detect_category(text):
        T=text.lower()
        if "bank" in T or "sbi" in T or "bob" in T or "boi" in T:return "Banking"
        if "rail" in T:return "Railway"
        if "ssc" in T:return "SSC"
        if "upsc" in T:return "UPSC"
        if "teacher" in T or "faculty" in T:return "Teaching"
        if "police" in T or "defence" in T or "army" in T or "navy" in T:return "Defence"
        return "Latest"

    for row in soup.select("table tbody tr")[:20]:
        try:
            cols=row.find_all("td")
            date=cols[0].get_text(strip=True)
            org=cols[1].get_text(strip=True)
            posts=cols[2].get_text(strip=True)
            link=row.find("a")["href"]

            job={
                "title":org,                         # Title cleaned (no Recruitment,date)
                "vacancies":posts.replace("–","-"),
                "qualification":"Check Notification",
                "age":"18+",
                "salary":"As per Govt Rules",
                "last_date":date,
                "state":"India",
                "category":detect_category(org),
                "apply_link":link,
                "source":"FreeJobAlert"
            }
            jobs.append(job)
        except:
            pass
    print("✔ FreeJobAlert Added")
except:
    print("❌ FreeJobAlert Failed")


# =========================================================
# SOURCE 2 — SarkariResult (Only Forms — no result/admit)
# =========================================================
try:
    print("📡 Fetching from SarkariResult ...")

    html=requests.get("https://www.sarkariresult.com/",headers=headers,timeout=20).text
    soup=bs4.BeautifulSoup(html,"html.parser")

    for row in soup.select(".post li a")[:20]:
        title=row.get_text(strip=True)
        link=row["href"]

        # Skip result/admit/syllabus
        if any(x in title.lower() for x in ["result","admit","syllabus","answer","certificate"]):
            continue

        job={
            "title":title,
            "vacancies":"Updating...",
            "qualification":"Check Notification",
            "age":"18+",
            "salary":"As per Govt Rules",
            "last_date":"Updating...",
            "state":"India",
            "category":detect_category(title),
            "apply_link":link,
            "source":"SarkariResult"
        }
        jobs.append(job)

    print("✔ SarkariResult Added")
except:
    print("❌ SarkariResult Failed")


# =========================================================
# Save + No Duplicate Title
# =========================================================
try:
    old=json.load(open("jobs.json"))
except:
    old=[]

titles=set(i["title"] for i in old)
final=old+[j for j in jobs if j["title"] not in titles]

open("jobs.json","w").write(json.dumps(final,indent=4))

print("\n📁 Total Jobs Saved:",len(final))
print("⏳ Last Update:",datetime.datetime.now())
print("✔ Auto Job Update Complete\n")

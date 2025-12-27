import json, requests, bs4, datetime

print("\n🚀 Smart Govt Job Scraper Running...\n")

URL="https://www.freejobalert.com/"
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

html=requests.get(URL,headers=headers,timeout=20).text
soup=bs4.BeautifulSoup(html,"html.parser")


# ---------------- Category Detector ----------------
def detect_category(text):
    T=text.lower()
    if "bank" in T or "sbi" in T or "bob" in T or "boi" in T:return "Banking"
    if "rail" in T:return "Railway"
    if "ssc" in T:return "SSC"
    if "upsc" in T:return "UPSC"
    if "teacher" in T or "faculty" in T:return "Teaching"
    if "police" in T or "defence" in T or "army" in T:return "Defence"
    return "Latest"
# ---------------------------------------------------


jobs=[]

# --------------- extract top jobs -----------------
for row in soup.select("table tbody tr")[:30]:
    try:
        cols=row.find_all("td")
        date = cols[0].get_text(strip=True)

        # TITLE only from link text
        a = row.find("a")
        org = a.get_text(strip=True) if a else ""

        posts = cols[2].get_text(strip=True) if len(cols)>2 else ""

        # if title empty (fallback)
        title_clean = org.split("Recruitment")[0].strip()
        if not title_clean:
            title_clean = posts[:40].strip()

        job={
            "title": title_clean,                       # final clean name
            "vacancies": posts.replace("–","-"),
            "qualification":"Check Official Notification",
            "age":"18+",
            "salary":"As per Govt Rules",
            "last_date": date,
            "state":"India",
            "category": detect_category(title_clean),
            "apply_link": a["href"] if a else ""
        }
        jobs.append(job)
    except:
        pass


# Merge Old + No duplicates
try:
    old=json.load(open("jobs.json"))
except:
    old=[]

titles=set(i["title"] for i in old)
final = old + [j for j in jobs if j["title"] not in titles and j["title"]!=""]


open("jobs.json","w").write(json.dumps(final,indent=4))

print("\n📁 Total Jobs Saved:",len(final))
print("⏳ Updated:",datetime.datetime.now())
print("✔ Auto Job Update Complete\n")

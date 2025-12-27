import json, requests, bs4, datetime,re
print("\n🚀 Smart Govt Job Scraper Running...\n")

URL="https://www.freejobalert.com/"
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

html=requests.get(URL,headers=headers,timeout=30).text
soup=bs4.BeautifulSoup(html,"html.parser")


# CATEGORY DETECTOR
def detect_category(text):
    T=text.lower()
    if "bank" in T:return "Banking"
    if "rail" in T:return "Railway"
    if "ssc" in T:return "SSC"
    if "upsc" in T:return "UPSC"
    if "teacher" in T or "faculty" in T:return "Teaching"
    if "police" in T or "defence" in T or "army" in T or "navy" in T:return "Defence"
    return "Latest"


jobs=[]

# Extract top table jobs only recruitment posts
for row in soup.select("table tbody tr")[:30]:
    try:
        cols=row.find_all("td")
        date=cols[0].get_text(strip=True)
        a=row.find("a")
        title=a.get_text(strip=True) if a else ""

        # FILTER 🔥 only recruitment forms
        if not re.search(r"(Form|Recruitment|Online|Vacancy|Post)",title,re.I):
            continue

        posts=cols[2].get_text(strip=True) if len(cols)>2 else "Updating"
        clean_title = re.sub(r"\s*\d{2}/\d{2}/\d{4}", "", title).strip()

        job={
            "title": clean_title,
            "vacancies": posts.replace("–","-"),
            "qualification":"Check Official Notification",
            "age":"18+",
            "salary":"As per Govt Rules",
            "last_date": date,
            "state":"India",
            "category": detect_category(clean_title),
            "apply_link": a["href"]
        }
        jobs.append(job)

    except:
        pass


open("jobs.json","w").write(json.dumps(jobs,indent=4))
print("📁 Saved:",len(jobs),"Jobs")
print("⏳ Updated:",datetime.datetime.now())
print("✔ Done\n")

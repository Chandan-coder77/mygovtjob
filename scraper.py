import requests, json, bs4, datetime

print("\n🚀 Updating Govt Jobs automatically...\n")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch(url):
    try:
        return requests.get(url, headers=headers, timeout=20).text
    except Exception as e:
        print("❌ Failed:", url, "\nReason:", e)
        return ""

all_jobs=[]

# 1️⃣ Sarkari Result
html = fetch("https://sarkariresult.com/latestjob.php")
if html:
    soup = bs4.BeautifulSoup(html,"html.parser")
    for a in soup.select("a")[:10]:
        title = a.get_text(strip=True)
        link = a["href"]
        if not link.startswith("http"):
            link="https://sarkariresult.com/"+link
        all_jobs.append({
            "title":title,
            "vacancies":"Updating...",
            "qualification":"Check Notice",
            "age":"18+",
            "salary":"Govt Rules",
            "last_date":"Updating...",
            "state":"India",
            "category":"Govt Job",
            "apply_link":link
        })


# 2️⃣ FreeJobAlert Backup
html2 = fetch("https://www.freejobalert.com/")
if html2:
    soup2 = bs4.BeautifulSoup(html2,"html.parser")
    for li in soup2.select("li a")[:10]:
        all_jobs.append({
            "title":li.get_text(strip=True),
            "vacancies":"Updating",
            "qualification":"Check Notice",
            "age":"18+",
            "salary":"Govt Rules",
            "last_date":"Updating...",
            "state":"India",
            "category":"Govt Job",
            "apply_link":li["href"]
        })

open("jobs.json","w").write(json.dumps(all_jobs,indent=4))
print(f"📄 Total jobs saved: {len(all_jobs)}")
print("⏳ Updated:",datetime.datetime.now())
print("✔ Auto success\n")

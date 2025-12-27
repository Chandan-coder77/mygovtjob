import json, requests, bs4, datetime, re

print("\n🚀 Smart Govt Job Scraper Running...\n")

URL = "https://www.freejobalert.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

html = requests.get(URL, headers=headers, timeout=20).text
soup = bs4.BeautifulSoup(html, "html.parser")


# ================= CATEGORY DETECTOR =================
def detect_category(text):
    T = text.lower()
    if "bank" in T or "sbi" in T or "bob" in T or "boi" in T:
        return "Banking"
    if "rail" in T:
        return "Railway"
    if "ssc" in T:
        return "SSC"
    if "upsc" in T:
        return "UPSC"
    if "teacher" in T or "faculty" in T:
        return "Teaching"
    if "police" in T or "defence" in T or "army" in T or "navy" in T:
        return "Defence"
    return "Latest"
# ======================================================


jobs = []

# Scraping Latest Jobs (Top 20)
for row in soup.select("table tbody tr")[:20]:
    try:
        cols = row.find_all("td")
        date = cols[0].get_text(strip=True)
        org = cols[1].get_text(strip=True)
        posts = cols[2].get_text(strip=True)
        link = row.find("a")["href"]

        # 🔥 Date को Title से हटाने का Logic
        clean_org = re.sub(r'\s*\d{1,2}/\d{1,2}/\d{4}\s*$', '', org).strip()

        job = {
            "title": f"{clean_org} Recruitment",  # 🔥 सिर्फ Organization + Recruitment
            "vacancies": posts.replace("–", "-"),
            "qualification": "Check Official Notification",
            "age": "18+",
            "salary": "As per Govt Rules",
            "state": "India",
            "category": detect_category(org),
            "last_date": date,  # 🔥 Last Date अब सबसे नीचे
            "apply_link": link
        }
        jobs.append(job)
    except:
        pass

# ========== No Duplicate + Save JSON ==========
try:
    old = json.load(open("jobs.json"))
except:
    old = []

titles = set(i["title"] for i in old)
final = old + [j for j in jobs if j["title"] not in titles]

open("jobs.json", "w").write(json.dumps(final, indent=4))

print("📁 Total Jobs Saved:", len(final))
print("⏳ Last Update:", datetime.datetime.now())
print("✔ Auto Job Update Complete\n")

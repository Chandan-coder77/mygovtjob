import json,requests,bs4,re,datetime,time

print("\n🚀 INDIA MEGA GOVT SCRAPER STARTED...\n")

#================ HIGH POWER USER-AGENT (100% Recommended) ================
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language":"en-US,en;q=0.9",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
#=========================================================================

def clean(x): return re.sub("\s+"," ",x).strip()

def make_job(title,vac,qual,age,sal,last,state,cat,link,src):
    return {
        "title":clean(title),
        "vacancies":clean(vac),
        "qualification":clean(qual),
        "age_limit":clean(age),
        "salary":clean(sal),
        "last_date":clean(last),
        "state":state,
        "category":cat,
        "apply_link":link,
        "source":src
    }

def detect_cat(t):
    T=t.lower()
    if "rail" in T: return "Railway"
    if "ssc" in T: return "SSC"
    if "upsc" in T: return "UPSC"
    if "bank" in T or "sbi" in T or "boi" in T or "bob" in T: return "Banking"
    if "teacher" in T or "lectur" in T: return "Teaching"
    if "police" in T or "army" in T or "defence" in T: return "Defence"
    return "Govt Job"

jobs=[]

#=======================================================================
# 1. FREEJOBALERT SCRAPER
#=======================================================================
print("📡 FreeJobAlert...")
try:
    soup=bs4.BeautifulSoup(requests.get("https://www.freejobalert.com/",headers=headers,timeout=30).text,"html.parser")
    rows=soup.select("table tbody tr")[:20]

    for row in rows:
        try:
            td=row.find_all("td")
            date,org,post=td[0].text,td[1].text,td[2].text
            link=row.find("a")["href"]

            inner=bs4.BeautifulSoup(requests.get(link,headers=headers).text,"html.parser")
            text=inner.get_text(" ",strip=True)

            qualification=re.findall(r"(?i)qualifi.*?(?=age|fee|salary|₹|rs)",text)
            salary=re.findall(r"(?i)salary.*?(?=qualifi|age|fee)",text)
            age=re.findall(r"(?i)age.*?(?=qualifi|salary|fee)",text)

            jobs.append(make_job(
                title=org.replace("Recruitment","").replace(date,""),
                vac=post,
                qual=qualification[0] if qualification else "Check Notification",
                age=age[0] if age else "18+",
                sal=salary[0] if salary else "As per Govt Rules",
                last=date,
                state="India",
                cat=detect_cat(org),
                link=link,
                src="FreeJobAlert"
            ))
        except: pass

except Exception as e:
    print("⚠ FreeJobAlert Error:",e)


#=======================================================================
# 2. SARKARI RESULT SCRAPER
#=======================================================================
print("📡 SarkariResult...")
try:
    soup=bs4.BeautifulSoup(requests.get("https://www.sarkariresult.com/",headers=headers).text,"html.parser")
    for a in soup.select("a")[:150]:
        t=a.text
        if any(x in t for x in ["Form","Recruit","Vacancy","Admit"]):
            jobs.append(make_job(t,"","Check Notification","18+","Govt Rules","","India",detect_cat(t),"https://www.sarkariresult.com/"+a['href'],"SarkariResult"))
except: print("⚠ Error")


#=======================================================================
# 3. NCS.GOV.IN API
#=======================================================================
print("📡 NCS Jobs...")
try:
    r=requests.get("https://www.ncs.gov.in/_layouts/15/ncsp/user/vacancy.asmx/GetGovVacancy",headers=headers).json()
    for j in r["d"][:40]:
        jobs.append(make_job(j["jobTitle"],j["noVacancy"],j["qualificationReq"],"18+",j["salary"],j["lastDate"],j["stateName"],"Govt Job","https://www.ncs.gov.in","NCS"))
except: print("⚠ Error")


#=======================================================================
# 4. SSC.gov.in
#=======================================================================
print("📡 SSC...")
try:
    soup=bs4.BeautifulSoup(requests.get("https://ssc.nic.in/",headers=headers).text,"html.parser")
    for x in soup.select("a")[:80]:
        if any(k in x.text for k in ["Recruit","Exam","Vacancy"]):
            jobs.append(make_job(x.text,"","Check Notification","18+","","","India","SSC","https://ssc.nic.in"+x['href'],"SSC"))
except: print("⚠ Error")


#=======================================================================
# 5. RAILWAY RRB
#=======================================================================
print("📡 Railway RRB...")
try:
    soup=bs4.BeautifulSoup(requests.get("https://www.rrbcdg.gov.in/",headers=headers).text,"html.parser")
    for x in soup.select("a")[:100]:
        if "Recruit" in x.text or "Notification" in x.text:
            jobs.append(make_job(x.text,"","Check Notification","18+","","","India","Railway","https://www.rrbcdg.gov.in/"+x['href'],"Railway"))
except: print("⚠ Error")


#=======================================================================
# 6. UPSC.gov.in
#=======================================================================
print("📡 UPSC...")
try:
    soup=bs4.BeautifulSoup(requests.get("https://upsc.gov.in",headers=headers).text,"html.parser")
    for x in soup.select("a")[:100]:
        if "Recruit" in x.text or "Exam" in x.text:
            jobs.append(make_job(x.text,"","Check PDF","18+","Govt Rules","","India","UPSC","https://upsc.gov.in"+x['href'],"UPSC"))
except: print("⚠ Error")


#=======================================================================
# MERGE + REMOVE DUPLICATE + SAVE
#=======================================================================
try: old=json.load(open("jobs.json"))
except: old=[]

exist=set(i["title"] for i in old)
final=old+[j for j in jobs if j["title"] not in exist]

open("jobs.json","w").write(json.dumps(final,indent=4))

print("\n==============================")
print(f"✔ TOTAL JOBS SAVED = {len(final)}")
print("🟢 Scraping Finished:",datetime.datetime.now())
print("==============================\n")

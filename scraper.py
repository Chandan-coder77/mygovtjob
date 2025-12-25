import requests
from bs4 import BeautifulSoup
import json

jobs=[]   # final combined data stored here

# ======================= 1. SSC =======================
def ssc_scraper():
    url="https://ssc.nic.in/"
    try:
        r=requests.get(url,timeout=15)
        soup=BeautifulSoup(r.text,"html.parser")

        for item in soup.find_all("a")[:3]:              # future expand
            jobs.append({
                "title":"SSC Latest Jobs",
                "vacancies":"Update Soon",
                "qualification":"10th/12th/Graduate",
                "age":"18+",
                "salary":"As per rules",
                "last_date":"Check Website",
                "state":"All India",
                "category":"SSC",
                "apply_link":"https://ssc.nic.in/"
            })
    except:
        print("SSC Failed")


# ======================= 2. UPSC =======================
def upsc_scraper():
    url="https://upsc.gov.in/"
    try:
        r=requests.get(url,timeout=15)
        soup=BeautifulSoup(r.text,"html.parser")

        jobs.append({
            "title":"UPSC New Recruitment",
            "vacancies":"Update Soon",
            "qualification":"Graduate/PG",
            "age":"21+",
            "salary":"As per rules",
            "last_date":"Check Website",
            "state":"All India",
            "category":"UPSC",
            "apply_link":"https://upsc.gov.in/"
        })
    except:
        print("UPSC Failed")


# ======================= 3. Railway =======================
def railway_scraper():
    url="https://indianrailways.gov.in/"
    try:
        requests.get(url,timeout=15)

        jobs.append({
            "title":"Railway Recruitment",
            "vacancies":"Upcoming",
            "qualification":"10th/ITI/Diploma",
            "age":"18+",
            "salary":"As per rules",
            "last_date":"Check Website",
            "state":"All India",
            "category":"Railway",
            "apply_link":"https://indianrailways.gov.in/"
        })
    except:
        print("Railway Failed")


# ======================= 4. BANK Coming Next =======================
def bank_scraper():
    jobs.append({
        "title":"Bank Jobs (Auto-Upcoming Update)",
        "vacancies":"Waiting extractor",
        "qualification":"Graduate",
        "age":"21+",
        "salary":"As per rules",
        "last_date":"Soon",
        "state":"All India",
        "category":"Bank",
        "apply_link":"https://ibps.in"
    })


# ======================= 5. Police =======================
def police_scraper():
    jobs.append({
        "title":"Police Recruitment (Auto-Upcoming Update)",
        "vacancies":"Soon",
        "qualification":"10th/12th",
        "age":"18+",
        "salary":"As per rules",
        "last_date":"Soon",
        "state":"State Wise",
        "category":"Police",
        "apply_link":"https://police.gov.in"
    })


# ======================= 6. Teacher =======================
def teacher_scraper():
    jobs.append({
        "title":"Teacher/TET Jobs",
        "vacancies":"Updating",
        "qualification":"B.Ed/CTET",
        "age":"21+",
        "salary":"As per norms",
        "last_date":"Check Website",
        "state":"India",
        "category":"Teacher",
        "apply_link":"https://ctet.nic.in"
    })


# ======================= RUN ALL =======================
ssc_scraper()
upsc_scraper()
railway_scraper()
bank_scraper()
police_scraper()
teacher_scraper()

# Save output
with open("jobs.json","w") as f:
    json.dump(jobs,f,indent=4)

print("JOB DATA UPDATED SUCCESSFULLY ✔")

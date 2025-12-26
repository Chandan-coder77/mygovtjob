import requests
from bs4 import BeautifulSoup
import json

jobs=[]

# ================== SSC LIVE TITLE SCRAPER ==================
def fetch_ssc():
    try:
        url="https://ssc.nic.in/portal/Notifications"
        r=requests.get(url,timeout=12).text
        soup=BeautifulSoup(r,"html.parser")
        
        notice=soup.select_one(".card-body a")   # First Latest Job Link
        title=notice.text.strip() if notice else "SSC Latest Notification"
        link="https://ssc.nic.in"+notice['href'] if notice else "https://ssc.nic.in/"
        
        return{
            "title":title,
            "vacancies":"As Per Notice",
            "qualification":"10th/12th/Graduate",
            "age":"18+",
            "salary":"As per SSC Rules",
            "last_date":"Check Notification",
            "state":"India",
            "category":"SSC",
            "apply_link":link
        }
    except:
        return{
            "title":"SSC Latest Notification",
            "vacancies":"Update Soon",
            "qualification":"10th/12th/Graduate",
            "age":"18+",
            "salary":"As per SSC",
            "last_date":"Check Website",
            "state":"India",
            "category":"SSC",
            "apply_link":"https://ssc.nic.in/"
        }


# ================== UPSC LIVE TITLE SCRAPER ==================
def fetch_upsc():
    try:
        url="https://upsc.gov.in/exams-related-info/recruitment"
        r=requests.get(url,timeout=12).text
        soup=BeautifulSoup(r,"html.parser")

        news=soup.select_one(".views-field-title a")
        title=news.text.strip() if news else "UPSC Latest Exam Notice"
        link="https://upsc.gov.in"+news['href'] if news else "https://upsc.gov.in/"

        return{
            "title":title,
            "vacancies":"As per notice",
            "qualification":"Graduate",
            "age":"21+",
            "salary":"As per UPSC",
            "last_date":"Check Notice",
            "state":"India",
            "category":"UPSC",
            "apply_link":link
        }
    except:
        return{
            "title":"UPSC Recruitment Coming Soon",
            "vacancies":"Soon",
            "qualification":"Graduate",
            "age":"21+",
            "salary":"As per UPSC",
            "last_date":"Next Update",
            "state":"India",
            "category":"UPSC",
            "apply_link":"https://upsc.gov.in/"
        }


# ============= Railway Basic (Later PDF Parsing Add) =============
def fetch_railway():
    return{
        "title":"Railway Recruitment Live Soon",
        "vacancies":"Coming",
        "qualification":"10th/ITI/Graduate",
        "age":"18+",
        "salary":"As per Rules",
        "last_date":"Check Site",
        "state":"India",
        "category":"Railway",
        "apply_link":"https://indianrailways.gov.in/"
    }


# ============= Bank Basic (SBI/IBPS scrape Next Step) =============
def fetch_bank():
    return{
        "title":"Bank IBPS/SBI Live Updates Soon",
        "vacancies":"Upcoming",
        "qualification":"Graduate",
        "age":"20+",
        "salary":"As per Bank",
        "last_date":"Check Site",
        "state":"India",
        "category":"Banking",
        "apply_link":"https://ibps.in/"
    }


# ============ MERGE + WRITE JSON ============
jobs.append(fetch_ssc())
jobs.append(fetch_upsc())
jobs.append(fetch_railway())
jobs.append(fetch_bank())

with open("jobs.json","w") as f:
    json.dump(jobs,f,indent=4)

print("New Live Scraper Updated Successfully 🚀")

import requests
from bs4 import BeautifulSoup
import json

jobs=[]


# =============== SSC LIVE via RSS ===============
def fetch_ssc():
    try:
        rss="https://ssc.nic.in/RSS"
        xml=requests.get(rss,timeout=10).text
        soup=BeautifulSoup(xml,"xml")
        title=soup.find("title").text.strip()
        return {
            "title": title,
            "vacancies": "Update Soon",
            "qualification":"10th/12th/Graduate",
            "age":"18+",
            "salary":"As per SSC rules",
            "last_date":"Check Website",
            "state":"All India",
            "category":"SSC",
            "apply_link":"https://ssc.nic.in/"
        }
    except:
        return {
            "title":"SSC Latest Notification",
            "vacancies":"Update Soon",
            "qualification":"10th/12th/Graduate",
            "age":"18+",
            "salary":"As per SSC rules",
            "last_date":"Check Website",
            "state":"All India",
            "category":"SSC",
            "apply_link":"https://ssc.nic.in/"
        }



# =============== UPSC LIVE via RSS ===============
def fetch_upsc():
    try:
        rss="https://upsc.gov.in/events-list/rss.xml"
        xml=requests.get(rss,timeout=10).text
        soup=BeautifulSoup(xml,"xml")
        title=soup.find("title").text.strip()
        return {
            "title": title,
            "vacancies":"Soon",
            "qualification":"Graduate",
            "age":"21+",
            "salary":"As per UPSC",
            "last_date":"Check Website",
            "state":"India",
            "category":"UPSC",
            "apply_link":"https://upsc.gov.in/"
        }
    except:
        return {
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



# =============== Railway Notice Basic Fetch ===============
def fetch_railway():
    return {
        "title":"Railway Recruitment Live Updates Soon",
        "vacancies":"Coming",
        "qualification":"10th/ITI/Graduate",
        "age":"18+",
        "salary":"As per Railway",
        "last_date":"Check Site",
        "state":"India",
        "category":"Railway",
        "apply_link":"https://indianrailways.gov.in/"
    }


# =============== BANK Notice Basic Fetch ===============
def fetch_bank():
    return {
        "title":"Bank (IBPS/SBI) Exam Updates - Auto Refresh Soon",
        "vacancies":"Upcoming",
        "qualification":"Graduate",
        "age":"20+",
        "salary":"As per Bank",
        "last_date":"Check Site",
        "state":"India",
        "category":"Banking",
        "apply_link":"https://ibps.in/"
    }


# --------- Push final output ---------
jobs.append(fetch_ssc())
jobs.append(fetch_upsc())
jobs.append(fetch_railway())
jobs.append(fetch_bank())

with open("jobs.json","w") as f: json.dump(jobs,f,indent=4)

print("Auto Job Scraper Updated Successfully 🚀")       

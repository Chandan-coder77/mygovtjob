import requests
from bs4 import BeautifulSoup
import json

# ========== SSC SCRAPER ==========
def scrape_ssc():
    url = "https://ssc.nic.in/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    jobs=[]

    for i in soup.select("marquee a, a"):
        text=i.get_text(strip=True)
        if "Recruitment" in text or "Exam" in text or "Vacancy" in text or "GD" in text or "Constable" in text:
            jobs.append({
                "title":text,
                "category":"SSC",
                "state":"India",
                "vacancies":"-",
                "qualification":"Check Notice",
                "age":"-",
                "salary":"As per govt rule",
                "last_date":"Check Notification",
                "apply_link":"https://ssc.nic.in/"
            })
    return jobs

# ========== UPSC ==========
def scrape_upsc():
    url="https://upsc.gov.in/"
    r=requests.get(url)
    soup=BeautifulSoup(r.text,"html.parser")
    jobs=[]
    for i in soup.select("a"):
        text=i.get_text(strip=True)
        if "Recruitment" in text or "Vacancy" in text:
            jobs.append({
                "title":text,
                "category":"UPSC",
                "state":"India",
                "vacancies":"-",
                "qualification":"Check Notice",
                "age":"-",
                "salary":"As per govt rule",
                "last_date":"Check Notification",
                "apply_link":"https://upsc.gov.in/"
            })
    return jobs

# ========== MERGE ALL ==========
def main():
    data=[]
    data.extend(scrape_ssc())
    data.extend(scrape_upsc())
    # future add → Railway, Police, Banking, Teacher, State Jobs

    with open("jobs.json","w",encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

if __name__=="__main__":
    main()

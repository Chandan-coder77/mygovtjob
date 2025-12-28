import json, os
from scraper import crawl_site

FILE = "jobs.json"

def load_jobs():
    if os.path.exists(FILE):
        try:
            return json.load(open(FILE))
        except:
            return []
    return []

def save_jobs(data):
    with open(FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

def main():
    old = load_jobs()

    urls = open("sources.txt").read().splitlines()
    new_jobs=[]

    for u in urls:
        new_jobs += crawl_site(u)

    unique = {j["title"]:j for j in (old+new_jobs)}
    final = list(unique.values())

    save_jobs(final)
    print("✔ Jobs updated:",len(final))

if __name__ == "__main__":
    main()

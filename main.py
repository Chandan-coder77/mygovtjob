import json
from scraper import load_sources, scrape

def main():
    print("\n🔍 AI Job Scraper Started...\n")
    sites = load_sources()
    all_jobs = []

    for site in sites:
        print("Scraping:", site)
        all_jobs += scrape(site)

    try:
        old = json.load(open("jobs.json"))
    except:
        old = []

    titles = set(i['title'] for i in old)
    final = old + [j for j in all_jobs if j['title'] not in titles]

    open("jobs.json","w").write(json.dumps(final,indent=4))
    print("\n📁 Saved Total Jobs:",len(final))

if __name__ == "__main__":
    main()

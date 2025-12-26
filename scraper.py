import json,requests,bs4,datetime

print("Running scraper...")

jobs=[{
    "title":"Govt Job Portal Live Soon",
    "vacancies":"Updating...",
    "qualification":"Check Official Notice",
    "age":"18+",
    "salary":"Govt Rules",
    "last_date":"Updating",
    "state":"India",
    "category":"Govt Job",
    "apply_link":"https://www.ncs.gov.in/"
}]

open("jobs.json","w").write(json.dumps(jobs,indent=4))
print("Updated:",datetime.datetime.now())

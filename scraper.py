import json

jobs = [
    {
        "title": "SSC GD Constable 2025",
        "vacancies": "25000+",
        "qualification": "10th Pass",
        "age": "18-23",
        "salary": "₹21,700 – ₹69,100",
        "last_date": "12 Jan 2025",
        "state": "All India",
        "category": "SSC",
        "apply_link": "https://ssc.nic.in/"
    },
    {
        "title": "Forester Recruitment 2025",
        "vacancies": "650",
        "qualification": "12th/Graduate",
        "age": "18-32",
        "salary": "₹25,500 – ₹81,100",
        "last_date": "20 Jan 2025",
        "state": "All India",
        "category": "Forest",
        "apply_link": "https://forest.odisha.gov.in/"
    }
]

with open("jobs.json","w") as f:
    json.dump(jobs,f,indent=4)

print("✔ jobs.json updated successfully!")

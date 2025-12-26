import json

# Temporary dummy data to fix blank issue
data = [
    {
        "title": "Govt Job Portal Live Soon",
        "vacancies": "Updating...",
        "qualification": "Check Official Notice",
        "age": "18+",
        "salary": "Govt Rules",
        "last_date": "Updating",
        "state": "India",
        "category": "Govt Job",
        "apply_link": "https://www.ncs.gov.in/"
    }
]

# Write to jobs.json
with open("jobs.json", "w") as f:
    json.dump(data, f, indent=4)

print("✔ Dummy data written to jobs.json")

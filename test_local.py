import json

try:
    jobs = json.load(open("jobs.json"))
    print("Jobs Loaded:", len(jobs))
    print("Sample:", jobs[0])
except Exception as e:
    print("Error reading jobs.json:", e)

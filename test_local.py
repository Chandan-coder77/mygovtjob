import json, datetime

print("\n=== TEST WRITE MODE ACTIVE ===")

# 1) Load Jobs
try:
    jobs = json.load(open("jobs.json"))
    print("Jobs loaded:", len(jobs))
except Exception as e:
    print("ERROR loading jobs.json:", e)
    exit()

# 2) Modify first item to confirm write
jobs[0]["test_update"] = "OK_" + str(datetime.datetime.now())

# 3) Save back
try:
    open("jobs.json","w").write(json.dumps(jobs,indent=4))
    print("jobs.json UPDATED successfully")
except Exception as e:
    print("WRITE ERROR jobs.json:", e)
    exit()

# 4) AI memory check
try:
    mem = json.load(open("ai_memory.json"))
    mem["test_memory"] = str(datetime.datetime.now())
    open("ai_memory.json","w").write(json.dumps(mem,indent=4))
    print("ai_memory.json UPDATED successfully")
except Exception as e:
    print("AI MEMORY WRITE ERROR:", e)
    exit()

print("\n🎉 LOCAL TEST COMPLETED — Now check files in repo")

import json

try: old=json.load(open("jobs.json"))
except: old=[]

new=json.load(open("jobs_details.json"))

titles={x["title"] for x in old}
final=old+[j for j in new if j["title"] not in titles]

json.dump(final,open("jobs.json","w"),indent=4)
print("Total Jobs:",len(final))

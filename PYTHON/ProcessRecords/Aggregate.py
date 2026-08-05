import json
#Count total records
def count(data):
    count=0
    for record in data:
        count+=1
    print(count)
with open("MOCK_DATA.JSON","r") as f:
    data=json.load(f)
    count(data)


#count of every email doiman
with open("MOCK_DATA.json","r") as f:
    data=json.load(f)
    gmail=0
    google=0
    apache=0
    for records in data:
        if "gmail.com" in records["email"]:
            gmail+=1
        elif "google.com" in records["email"]:
            google+=1
        else:
            apache+=1
    print(f"google.com:{google}\ngmail.com:{gmail}\napache.com:{apache}")



import json

#Print all the records
with open("MOCK_DATA.json","r") as f:
    data=json.load(f)
    # print(data)

#Print only 10 records
with open("MOCK_DATA.json","r") as f:
    data=json.load(f)
    # for record in data:
    #     if record["id"]>=1 & record["id"]<11:
    #         print(record)
    # print(data[:10])

#Print full names
with open("MOCK_DATA.json","r") as f:
    data=json.load(f)
    for records in data:
        print(records["first_name"],records["last_name"])

#Print record with gender male
with open("MOCK_DATA.json","r") as f:
    data=json.load(f)
    for records in data:
        if records["gender"]=="Male":
            print(records)

#Print record with name starting with A
with open("MOCK_DATA.json","r") as f:
    data=json.load(f)
    for records in data:
        if records["first_name"].startswith("A"):
            print(records)


        


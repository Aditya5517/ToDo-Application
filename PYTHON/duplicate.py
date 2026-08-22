check=[1,2,3,4,1,2];
map={}
present =False
for i in check:
    if i in map:
        present=True
        break
    else:
        map[i]=1
if present:
    print("Duplicate present")
else:
    print("No Duplicate present")
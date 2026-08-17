from utils import validators
try: 
    value = input("Enter Value: ")
    count = {}
    for ch in value:
        count[ch] = count.get(ch,0)+1
    print(count)
except ValueError:
    print("Invalid Data Type, enter a valid string")
except  Exception:
    print("An unaccepted error occured")
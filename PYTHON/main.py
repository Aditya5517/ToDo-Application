from utils.validators import validate_input

name = input("Enter your name: ")

if validate_input(name):
    print("Valid Input")
else:
    print("Invalid Input")
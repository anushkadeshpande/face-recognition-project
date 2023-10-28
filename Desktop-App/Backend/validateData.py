import re

def validateData(name, address, phone, email):
    
    # name 
    if name!="" and name.isalpha() and len(name) >= 3:
        print("Valid Name")
    else:
        return "Please enter a valid name!"

    # address
    if address!="":
        print("Valid Address")
    else:
        return "Please enter a valid address!"

    # phone
    if phone!="" and phone.isdigit() and len(phone) == 10:
        print("Valid Phone")
    else:
        return "Please enter a valid phone number!"

    # email
    emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    if email!="" and re.fullmatch(emailRegex, email):
        print("Valid Email")
    else:
        return "Please enter a valid email address!"
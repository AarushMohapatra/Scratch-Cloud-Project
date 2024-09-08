import scratchattach as scratch3
import pandas as pd
import csv
import time

scratchuser = input("Username: ")
scratchpass = input("Password: ")
project = input("Project ID: ")
session = scratch3.login(scratchuser, scratchpass)
conn = session.connect_cloud(project)
olddata = ''
oldrequest = ''
conn.set_var(variable='scratchattach Status', value=1)

charaters = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
charaters_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '_', ':', ' ', '.']

for cool in range(32):
    charaters.append(str(cool + 10))

userlimit = ['3', '9']

if len(charaters) == len(charaters_keys):
    print("setup done")

print(charaters)

while True:
    data = scratch3.get_var(project_id=project, variable="send data")
    print(data)

    if olddata != data:
        length = len(data)
        usertemp = []
        user = ''
        i = 0
        ie = 1
        
        while usertemp != userlimit: #and ie < len(data):
            if usertemp == userlimit:
                break
            usertemp = [data[i], data[ie]]
            print(usertemp)
            i += 1
            ie += 1
            identifier = usertemp[0] + usertemp[1]
            print(identifier)
            
            for r in range(len(charaters_keys)):
                if identifier == charaters[r] and identifier != 39:
                    user += charaters_keys[r]
                    print(user)
                    break

            if i >= len(data) or ie >= len(data):
                break

        found = False

        with open(r'data.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
        
        for row in rows:
            if row['username'] == user:
                row['code'] = data
                found = True
                print(f"Updated code for existing user {user}")
                break
        
        if not found:
            with open(r'data.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['username', 'code'])
                writer.writerow({'username': user, 'code': data})
                print(f"Added new user {user}")
        else:
            with open(r'data.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['username', 'code'])
                writer.writeheader()
                writer.writerows(rows)

    else:
        print("No change detected in data!")

    request = scratch3.get_var(project_id=project, variable="request")
    print(request)

    if oldrequest != request and request != '':
        length = len(request)
        usertemp = []
        user = ''
        i = 0
        ie = 1
        
        while usertemp != userlimit: #and ie < len(request):
            if usertemp == userlimit:
                break
            usertemp = [request[i], request[ie]]
            print(usertemp)
            i += 1
            ie += 1
            identifier = usertemp[0] + usertemp[1]
            print(identifier)
            
            for r in range(len(charaters_keys)):
                if identifier == charaters[r] and identifier != 39:
                    user += charaters_keys[r]
                    print(user)
                    break

            if i >= len(request) or ie >= len(request):
                break

        found = False
        code = None

        with open(r'data.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == user:
                    code = row['code']
                    found = True
                    print(f"Found code {code} for user {user}")
                    conn.set_var(variable='scratchattach Status', value=4)
                    conn.set_var(variable='request data', value=code)
                    conn.set_var(variable='request', value='')
                    time.sleep(1)
                    conn.set_var(variable='scratchattach Status', value=1)
                    break

        if not found:
            conn.set_var(variable='request data', value='051818518')
            print("No match found.")
        else:
            print(f"Code for user {user} is {code}")

    else:
        print("No change detected in request!")

    olddata = data
    oldrequest = request

conn.set_var(variable='scratchattach Status', value=0)


# -*- coding: latin-1 -*-

from codecs import ascii_decode
from urllib import response
import requests
import json


def GetTimetable(Url:str, Username: str,Password: str, Week: str, Day: int):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    myobj = {
        'client_id':'ANDR',
        'grant_type':'password',
        'username':Username,
        'password':Password
        }
    response = requests.post(Url + "/api/login", headers=headers ,data= myobj)

    print("Status Code", response.status_code)
    print("JSON Response ", response.json().get("access_token"))


    token = response.json().get("access_token")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer " +str(token)
        }

    response = requests.get(Url + "/api/3/timetable/actual?" + Week, headers=headers,stream=False)

    print("Status Code", response.status_code)

    jsondata = response.json()
    with open("developer.json", "w", encoding='utf8') as write_file:
        json.dump(jsondata,write_file, indent=2, ensure_ascii=False)

    jsonday = jsondata.get("Days")[Day-1]
    jsonclass = jsonday.get("Atoms")
    jsonsubjects = jsondata.get("Subjects")
    jsonteachers = jsondata.get("Teachers")
    jsonrooms = jsondata.get("Rooms")

# Získání dat z hodin
    print("Hodiny:")
    output = {}
    for i in range(0,len(jsonclass)):
        subname = "Volno"
        teachname = "Nikdo"
        roomnum = "000"
        # Název hodiny
        subject = jsonclass[i].get("SubjectId")
        for a in range(0,len(jsonsubjects)):
            if jsonsubjects[a].get("Id") == subject:
                
                subname = jsonsubjects[a].get("Name")



        # Jméno učitele
        teacher = jsonclass[i].get("TeacherId")
        for a in range(0,len(jsonteachers)):
            if jsonteachers[a].get("Id") == teacher:
                teachname = jsonteachers[a].get("Name")

        # Místnost
        room = jsonclass[i].get("RoomId")
        for a in range(0,len(jsonrooms)):
            if jsonrooms[a].get("Id") == room:
                roomnum = jsonrooms[a].get("Abbrev")
        
        output[i+1] = {"subject": subname, "teacher": teachname, "room": roomnum}

    

    return output




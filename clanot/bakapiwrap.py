
# -*- coding: latin-1 -*-

# Bakalari API Wrapper
#! DO NOT DELETE - Keep for reference and use in non-async projects.

import requests

'''
Získání tokenu pomocí přihlašovacích údajů.

POZOR!
    Vrací data v dictonary! Použijte ".get()" pro získání dat
'''
def Login(Url:str, Username:str, Password:str):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    myobj = {
        'client_id':'ANDR',
        'grant_type':'password',
        'username':Username,
        'password':Password
        }
    response = requests.post(Url + "/api/login", headers=headers ,data= myobj)
    return {'token': str(response.json().get("access_token")), "refresh": str(response.json().get("refresh_token"))}


'''
Získání tokenu z refresh tokenu
    Refresh token vyprší přibližně za 1 měsíc, po vypršení použijte "Login()"

POZOR!
    Vrací data v dictonary! Použijte ".get()" pro získání dat
'''
def RefreshToken(Url:str, Token:str):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    myobj = {
        'client_id':'ANDR',
        'grant_type':'refresh_token',
        'refresh_token': str(Token)
        }
    response = requests.post(Url + "/api/login", headers=headers ,data= myobj)
    return {'token': str(response.json().get("access_token")), "refresh": str(response.json().get("refresh_token"))}

def GetRawTimetable(Url:str, Token:str, Week: str):
    # získání rozvrhu v json formátu
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer " +str(Token)
        }
    response = requests.get(Url + "/api/3/timetable/actual?" + Week, headers=headers,stream=False).json()
    return response

def GetTimetable(response:dict, Week: str, Day: int):
    jsondata = response
    jsonday = jsondata.get("Days")[Day-1]
    jsonclass = jsonday.get("Atoms")
    jsonsubjects = jsondata.get("Subjects")
    jsonteachers = jsondata.get("Teachers")
    jsonrooms = jsondata.get("Rooms")
    # Získání dat z hodin
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

def GetFullTimetable(response:dict, Week: str):
    jsondata = response
    jsondays = jsondata.get("Days")
    jsonsubjects = jsondata.get("Subjects")
    jsonteachers = jsondata.get("Teachers")
    jsonrooms = jsondata.get("Rooms")
    # Získání dat z hodin
    output = {}
    for d in range(0,5):
        jsonclass = jsondays[d].get("Atoms")
        classes = {}
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
            classes[i+1] = {"subject": subname, "teacher": teachname, "room": roomnum}
        days = ["po","ut","st","ct","pa"]
        output[days[d]] = classes
    return output

#        _                   _   
#    ___| | __ _ _ __   ___ | |_ 
#   / __| |/ _` | '_ \ / _ \| __|
#  | (__| | (_| | | | | (_) | |_ 
#   \___|_|\__,_|_| |_|\___/ \__|
#
# Version: 2.1
# Authors: HyScript7, Mobilex
# License: MIT License
# Copyright (c) 2022 HyScript7 & mobilex1122
#
from bs4 import BeautifulSoup
import requests

async def GetToday(URL:str):
    req= requests.get(URL)
    soup = BeautifulSoup(req.text, "html.parser")
    first = soup.find("div",attrs={"class":"jidelnicekDen"}).find_all("div", attrs={"class":"column jidelnicekItem"})
    return {"1": first[0].get_text().strip(), "2": first[1].get_text().strip()}

async def GetNext(URL:str):
    req= requests.get(URL)
    soup = BeautifulSoup(req.text, "html.parser")
    first = soup.find_all("div",attrs={"class":"jidelnicekDen"})[1].find_all("div", attrs={"class":"column jidelnicekItem"})
    return {"1": first[0].get_text().strip(), "2": first[1].get_text().strip()}


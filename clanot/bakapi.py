#        _                   _   
#    ___| | __ _ _ __   ___ | |_ 
#   / __| |/ _` | '_ \ / _ \| __|
#  | (__| | (_| | | | | (_) | |_ 
#   \___|_|\__,_|_| |_|\___/ \__|
#
# Version: 2.0
# Authors: HyScript7, Mobilex
#

import requests
import time
import datetime

class token():
    """bakapiwraper token class
    This class handles all token / auth related operations.
    To fetch the auth token, use token.get(), which returns a string
    
    Keyword arguments:
    url -- Url of the Bakaláři server
    username -- Username that will be used to authenticate
    password -- Password that will be used to authenticate
    Return: None
    """
    
    def __init__(self, url: str, username: str, password: str) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.token = None
        self.refresh = None
        self.lastRefresh = time.time()
        self.tokenLifetime = 600 # 10 Minutes
    
    async def login(self) -> None:
        print("Logging into Balakari")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {'client_id':'ANDR', 'grant_type':'password', 'username': self.username, 'password': self.password}
        response = requests.post(self.url + "/api/login", headers=headers ,data=payload)
        self.token = response.json().get("access_token")
        self.refresh = response.json().get("refresh_token")
        self.lastRefresh = time.time()
    
    async def refresh(self) -> None:
        print("Refreshing Balakari Token")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {'client_id':'ANDR', 'grant_type':'refresh_token', 'refresh_token': self.refresh}
        response = requests.post(self.url + "/api/login", headers=headers ,data=payload)
        self.token = response.json().get("access_token")
        self.refresh = response.json().get("refresh_token")
        self.lastRefresh = time.time()

    async def get(self) -> str:
        if self.token is None or self.refresh is None:
            await self.login()
        if round(time.time()) - self.lastRefresh > self.tokenLifetime:
            await self.refresh()
        return self.token

class timetable():
    """bakapiwrapper timetable class
    This class handles timetable fetching for a specific day or week.
    To fetch raw json data, use timetable.fetchRawWeek(authtoken, "year, month, day")
    """
    def __init__(self, url: str) -> None:
        self.url = url
        pass
    async def parseFromTimestamp(self, time: int) -> str:
        dt = datetime.datetime.fromtimestamp(time)
        year = dt.year
        month = dt.month
        if len(str(month)) == 1:
            month = "0" + str(month)
        day = dt.day
        if len(str(day)) == 1:
            day = "0" + str(day)
        week_day = dt.weekday()
        return (f"{year}, {month}, {day}", week_day)
    async def parseFromDate(self, year: int, month: int, day: int):
        dt = datetime.datetime(year, month, day)
        year = dt.year
        month = dt.month
        if len(str(month)) == 1:
            month = "0" + str(month)
        day = dt.day
        week_day = dt.weekday()
        return (f"{year}, {month}, {day}", week_day)
    async def fetchRawWeek(self, Token: token, week: str):
        # TODO: Rename this function to fetchTimetable()
        headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": "Bearer " + await Token.get()}
        return requests.get(self.url + "/api/3/timetable/actual?" + week, headers=headers,stream=False).json()
    async def parseTimetable(self, data: dict):
        #TODO: Port function GetTimetable() from bakapiwrap
        pass

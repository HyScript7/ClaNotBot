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

class token():
    """bakapiwraper token class
    This class handles all token / auth related operations.
    
    Keyword arguments:
    url -- Url of the Bakaláři server
    username -- Username that will be used to authenticate
    password -- Password that will be used to authenticate
    Return: None
    """
    
    async def __init__(self, url: str, username: str, password: str) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.token = None
        self.refresh = None
        self.lastRefresh = time.time()
        self.tokenLifetime = 600 # 10 Minutes
    
    async def login(self) -> None:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {'client_id':'ANDR', 'grant_type':'password', 'username': self.username, 'password': self.password}
        response = requests.post(self.url + "/api/login", headers=headers ,data=payload)
        self.token = response.json().get("access_token")
        self.refresh = response.json().get("refresh_token")
        self.lastRefresh = time.time()
    
    async def refresh(self) -> None:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {'client_id':'ANDR', 'grant_type':'refresh_token', 'refresh_token': self.refresh}
        response = requests.post(self.url + "/api/login", headers=headers ,data=payload)
        self.token = response.json().get("access_token")
        self.refresh = response.json().get("refresh_token")
        self.lastRefresh = time.time()

    async def __call__(self) -> str:
        if self.token is None or self.refresh is None:
            await self.login()
        if round(time.time()) - self.lastRefresh > self.tokenLifetime:
            await self.refresh()
        return self.token

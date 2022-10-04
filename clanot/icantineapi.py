import requests
from bs4 import BeautifulSoup


from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re



def GetToday(URL:str):

    req= requests.get('http://jidelna.gasos-ro.cz')

    soup = BeautifulSoup(req.text, "html.parser")

    first = soup.find("div",attrs={"class":"jidelnicekDen"}).find_all("div", attrs={"class":"column jidelnicekItem"})

    return {"1": first[0].get_text().strip(), "2": first[1].get_text().strip()}

def GetNext(URL:str):
    pass



print(GetToday("https://jidelna.gasos-ro.cz/"))
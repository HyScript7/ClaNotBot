from bs4 import BeautifulSoup
import requests

def GetToday(URL:str):

    req= requests.get(URL)

    soup = BeautifulSoup(req.text, "html.parser")

    first = soup.find("div",attrs={"class":"jidelnicekDen"}).find_all("div", attrs={"class":"column jidelnicekItem"})

    return {"1": first[0].get_text().strip(), "2": first[1].get_text().strip()}

def GetNext(URL:str):
    req= requests.get(URL)

    soup = BeautifulSoup(req.text, "html.parser")

    first = soup.find_all("div",attrs={"class":"jidelnicekDen"})[1].find_all("div", attrs={"class":"column jidelnicekItem"})

    return {"1": first[0].get_text().strip(), "2": first[1].get_text().strip()}
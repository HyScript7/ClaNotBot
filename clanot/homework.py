import json
from os.path import exists

class Homework():

    def __init__(self, path:str) -> None:
        self.path = path
    
    async def new(self, settime:str ,finishtime:str, title:str, content:str) -> None:
        json_object = None
        if exists(self.path):
            with open(self.path, 'r') as openfile:
                json_object = json.load(openfile)
 
        


        data = {
            "endtime": finishtime,
            "title": title,
            "content":content
        }

        json_object.set(settime, data)

        json_object = json.dumps(dictionary, indent=4)
        with open(self.path, "w") as outfile:
            outfile.write(json_object)

import json
from os.path import exists

class Homework():

    def __init__(self, path:str) -> None:
        self.path = path
    
    async def new(self, settime:str ,finishtime:str, title:str, content:str) -> None:
        json_object = {"test":"test"}
        if exists(self.path):
            with open(self.path, 'r') as openfile:
                json_object = json.load(openfile)
 
        


        data = {
            "endtime": finishtime,
            "title": title,
            "content":content
        }

        json_object[settime] = data

        json_data= json.dumps(json_object, indent=4)
        with open(self.path, "w") as outfile:
            outfile.write(json_data)

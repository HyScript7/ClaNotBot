from clanot import bakapiwrap as baka
import json

with open("./testing_dataset.json", "r") as ds:
    print(baka.GetTimetable(json.loads(ds.read()), "2022-09-19", 1))

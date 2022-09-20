from clanot import bakapiwrap as baka
from decouple import config
import json

bakauser = str(config("BAKAUSER"))
bakapass = str(config("BAKAPASS"))

token = baka.Login("https://sbakalari.gasos-ro.cz", bakauser, bakapass).get("token")
ts = baka.GetRawTimetable("https://sbakalari.gasos-ro.cz", token, "2022-09-20")

with open("./testdataset.json", "w") as file:
    file.write(json.dumps(ts.json(), indent=4))


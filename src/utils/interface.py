import eel
import json


def process_states(states):
    if states["hasGroundStationFile"] == True:
        print("have file gs")
        

@eel.expose  # Expose this function to Javascript
def getFormData(j, files = None):
    states = {"hasGroundStationFile":False, "groundStationFile": None ,
              "hasTleFile": False, "TleFile":None}
    print("json ", j)
    filesJ = json.loads(files)

    if files != None:
        for i in filesJ:            
            print(i["key"])
            if i['key'] == "groundStationFile":
                states["hasGroundStationFile"] = True
                states["groundStationFile"] = i['file']
            elif i['key'] == "tleFile":
                states["hasTleFile"] = True
                states["TleFile"] = i['file']
    process_states(states)
    return "ok"
import eel
import json
from myUtils import process


@eel.expose  # Expose this function to Javascript
def getFormData(j, files=None):
    states = {
        "hasGroundStationFile": False,
        "groundStationFile": None,
        "hasTleFile": False,
        "tleFile": None,
        "tleInfo": {
            "NICE_NAME": "",
            "NUM_ORBS": 0,
            "NUM_SATS_PER_ORB": 0,
            "PHASE_DIFF": True,
            "INCLINATION_DEGREE": 0,
            "ECCENTRICITY": 0,
            "ARG_OF_PERIGEE_DEGREE": 0,
            "MEAN_MOTION_REV_PER_DAY": 0,
        },
    }
    print("json ", j)
    filesJ = json.loads(files)

    if files != None:
        for i in filesJ:
            print(i["key"])
            if i["key"] == "groundStationFile":
                states["hasGroundStationFile"] = True
                states["groundStationFile"] = i["file"]
            elif i["key"] == "tleFile":
                states["hasTleFile"] = True
                states["tleFile"] = i["file"]

    if states["hasTleFile"] == False:
        states["tleInfo"]["NICE_NAME"] = j["NICE_NAME"]
        states["tleInfo"]["NUM_ORBS"] = j["NUM_ORBS"]
        states["tleInfo"]["NUM_SATS_PER_ORB"] = j["NUM_SATS_PER_ORB"]
        states["tleInfo"]["PHASE_DIFF"] = j["PHASE_DIFF"]
        states["tleInfo"]["INCLINATION_DEGREE"] = j["INCLINATION_DEGREE"]
        states["tleInfo"]["ECCENTRICITY"] = j["ECCENTRICITY"]
        states["tleInfo"]["ARG_OF_PERIGEE_DEGREE"] = j["ARG_OF_PERIGEE_DEGREE"]
        states["tleInfo"]["MEAN_MOTION_REV_PER_DAY"] = j["MEAN_MOTION_REV_PER_DAY"]
    return process.process_states(states)

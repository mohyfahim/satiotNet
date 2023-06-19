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
        "hasISL": False,
        "algo": "",
        "SATELLITE_CONE_RADIUS_M": 0,
        "ALTITUDE_M": 0,
        "time_step_ms": 0,
        "duration_s": 0,
    }

    j = json.loads(j)
    print(j)
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
        states["tleInfo"]["NUM_ORBS"] = int(j["NUM_ORBS"])
        states["tleInfo"]["NUM_SATS_PER_ORB"] = int(j["NUM_SATS_PER_ORB"])
        if "PHAE_DIFF" in j:
            states["tleInfo"]["PHASE_DIFF"] = True
        else:
            states["tleInfo"]["PHASE_DIFF"] = False

        states["tleInfo"]["INCLINATION_DEGREE"] = float(j["INCLINATION_DEGREE"])
        states["tleInfo"]["ECCENTRICITY"] = float(j["ECCENTRICITY"])
        states["tleInfo"]["ARG_OF_PERIGEE_DEGREE"] = float(j["ARG_OF_PERIGEE_DEGREE"])
        states["tleInfo"]["MEAN_MOTION_REV_PER_DAY"] = float(
            j["MEAN_MOTION_REV_PER_DAY"]
        )
    if "hasISL" in j:
        states["hasISL"] = True
    if "algorithm_free_one_only_gs_relays" in j:
        states["algo"] = "algorithm_free_one_only_gs_relays"
    else:
        states["algo"] = "algorithm_free_one_only_over_isls"

    states["SATELLITE_CONE_RADIUS_M"] = int(j["SATELLITE_CONE_RADIUS_M"])
    states["ALTITUDE_M"] = int(j["ALTITUDE_M"])
    states["time_step_ms"] = int(j["time_step_ms"])
    states["duration_s"] = int(j["duration_s"])
    return process.process_states(states)

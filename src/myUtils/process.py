import sys
import os
import datetime

from myUtils import defpaths

sys.path.append(os.path.join(defpaths.MYUTILS_PATH, "../../hypatia/satgenpy"))
import satgen


def generateExtendGroundStations(inputFile, outputPath):
    satgen.extend_ground_stations(inputFile, outputPath + "/ground_stations.txt")


def process_states(states):
    TRY_PATH = (
        defpaths.OUTPUT_PATH
        + "/"
        + datetime.datetime.now().strftime("%Y-%d-%m-%H-%M-%S")
    )
    INPUT_PATH = TRY_PATH + "/" + "input"
    OUTPUT_PATH = TRY_PATH + "/" + "output"
    if not os.path.isdir(TRY_PATH):
        os.makedirs(TRY_PATH, exist_ok=True)
        os.makedirs(INPUT_PATH, exist_ok=True)
        os.makedirs(OUTPUT_PATH, exist_ok=True)

    if states["hasTleFile"] == True:
        with open(OUTPUT_PATH + "/tles.txt", "w") as tle:
            tle.write(states["tleFile"]["content"])
    else:
        print("Generating TLEs...")
        if states["info"]["ECCENTRICITY"] == 0:
            states["info"]["ECCENTRICITY"] = 0.0000001

        satgen.generate_tles_from_scratch_manual(
            OUTPUT_PATH + "/tles.txt",
            states["info"]["NICE_NAME"],
            states["info"]["NUM_ORBS"],
            states["info"]["NUM_SATS_PER_ORB"],
            states["info"]["PHASE_DIFF"],
            states["info"]["INCLINATION_DEGREE"],
            states["info"]["ECCENTRICITY"],
            states["info"]["ARG_OF_PERIGEE_DEGREE"],
            states["info"]["MEAN_MOTION_REV_PER_DAY"],
        )

    if states["hasGroundStationFile"] == True:
        GROUNDSTATION_PATH = INPUT_PATH + "/groundStations.txt"
        with open(GROUNDSTATION_PATH, "w") as gs:
            gs.write(states["groundStationFile"]["content"])
        generateExtendGroundStations(GROUNDSTATION_PATH, OUTPUT_PATH)
    else:
        return "error, ground station error"

    return "ok"
import sys
import os
import datetime
import math

from myUtils import defpaths

sys.path.append(os.path.join(defpaths.MYUTILS_PATH, "../../hypatia/satgenpy"))
import satgen
from satgen.post_analysis.print_routes_and_rtt import print_routes_and_rtt

EARTH_RADIUS = 6378135.0


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
    ANALYZE_PATH = TRY_PATH + "/" + "analyze"
    if not os.path.isdir(TRY_PATH):
        os.makedirs(TRY_PATH, exist_ok=True)
        os.makedirs(INPUT_PATH, exist_ok=True)
        os.makedirs(OUTPUT_PATH, exist_ok=True)
        os.makedirs(ANALYZE_PATH, exist_ok=True)

    if states["hasTleFile"] == True:
        with open(OUTPUT_PATH + "/tles.txt", "w") as tle:
            tle.write(states["tleFile"]["content"])
    else:
        print("Generating TLEs...")
        if states["tleInfo"]["ECCENTRICITY"] == 0:
            states["tleInfo"]["ECCENTRICITY"] = 0.0000001

        satgen.generate_tles_from_scratch_manual(
            OUTPUT_PATH + "/tles.txt",
            states["tleInfo"]["NICE_NAME"],
            states["tleInfo"]["NUM_ORBS"],
            states["tleInfo"]["NUM_SATS_PER_ORB"],
            states["tleInfo"]["PHASE_DIFF"],
            states["tleInfo"]["INCLINATION_DEGREE"],
            states["tleInfo"]["ECCENTRICITY"],
            states["tleInfo"]["ARG_OF_PERIGEE_DEGREE"],
            states["tleInfo"]["MEAN_MOTION_REV_PER_DAY"],
        )

    if states["hasGroundStationFile"] == True:
        print("Generating ground stations...")
        GROUNDSTATION_PATH = INPUT_PATH + "/groundStations.txt"
        with open(GROUNDSTATION_PATH, "w") as gs:
            gs.write(states["groundStationFile"]["content"])
        generateExtendGroundStations(GROUNDSTATION_PATH, OUTPUT_PATH)
    else:
        return "error, ground station error"

    print("Generating ISLs...")

    if states["hasISL"] == True:
        satgen.generate_plus_grid_isls(
            OUTPUT_PATH + "/isls.txt",
            states["tleInfo"]["NUM_ORBS"],
            states["tleInfo"]["NUM_SATS_PER_ORB"],
            isl_shift=0,
            idx_offset=0,
        )
    else:
        satgen.generate_empty_isls(OUTPUT_PATH + "/isls.txt")

    MAX_GSL_LENGTH_M = math.sqrt(
        math.pow(states["SATELLITE_CONE_RADIUS_M"], 2)
        + math.pow(states["ALTITUDE_M"], 2)
    )
    MAX_ISL_LENGTH_M = 2 * math.sqrt(
        math.pow(EARTH_RADIUS + states["ALTITUDE_M"], 2)
        - math.pow(EARTH_RADIUS + 80000, 2)
    )

    print("Generating description...")
    satgen.generate_description(
        OUTPUT_PATH + "/description.txt",
        MAX_GSL_LENGTH_M,
        MAX_ISL_LENGTH_M,
    )

    ground_stations = satgen.read_ground_stations_extended(
        OUTPUT_PATH + "/ground_stations.txt"
    )
    gsl_interfaces_per_satellite = 1

    print("Generating GSL interfaces info..")
    satgen.generate_simple_gsl_interfaces_info(
        OUTPUT_PATH + "/gsl_interfaces_info.txt",
        states["tleInfo"]["NUM_ORBS"] * states["tleInfo"]["NUM_SATS_PER_ORB"],
        len(ground_stations),
        gsl_interfaces_per_satellite,  # GSL interfaces per satellite
        1,  # (GSL) Interfaces per ground station
        1,  # Aggregate max. bandwidth satellite (unit unspecified)
        1,  # Aggregate max. bandwidth ground station (same unspecified unit)
    )

    # Forwarding state
    print("Generating forwarding state...")
    satgen.help_dynamic_state(
        TRY_PATH,
        20,  # Number of threads
        "output",
        states["time_step_ms"],
        states["duration_s"],
        MAX_GSL_LENGTH_M,
        MAX_ISL_LENGTH_M,
        states["algo"],
        True,
    )

    return "ok"

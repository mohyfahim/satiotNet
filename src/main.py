import os
import platform
import sys
import eel

SRC_PATH = os.path.dirname(os.path.realpath(__file__))

print(SRC_PATH)
# Set web files folder and optionally specify which file types to check for eel.expose()
eel.init(SRC_PATH + "/web", allowed_extensions=[".js", ".html"])

from myUtils import interface

def closeCallBack(path, ws):
    print("closed ", path, " ws:", ws)
    if path == "index.html":
        sys.exit(0)


try:
    eel.start(
        "index.html", mode="chrome", size=(1920, 1080), close_callback=closeCallBack
    )
except EnvironmentError:
    print("error1")
    # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
    if sys.platform in ["win32", "win64"] and int(platform.release()) >= 10:
        eel.start("index.html", mode="edge")
    else:
        print("error")  # TODO: platform alert

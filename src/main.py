import os
import platform
import sys
import eel


# Set web files folder and optionally specify which file types to check for eel.expose()
eel.init("web", allowed_extensions=[".js", ".html"])


@eel.expose  # Expose this function to Javascript
def say_hello_py(x):
    print("Hello from %s" % x)


def closeCallBack(path, ws):
    print("closed ", path, " ws:", ws)
    if path == "index.html":
        sys.exit(0)


say_hello_py("Python World!")

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

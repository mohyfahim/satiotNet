import eel
import json

@eel.expose  # Expose this function to Javascript
def getFormData(j, files = None):
    print("json ", j)
    if files != None:
        filesJ = json.loads(files)
        print(filesJ)
            

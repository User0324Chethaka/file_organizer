import json
import subprocess
import platform

file_path  = r"../activate.json"

activation = None
with open(file_path, "r") as jf:
    activation = json.load(jf)

os_platform = platform.system()

p = None
if os_platform.lower == 'windows':
    p = 'python' 
else:
    p = 'python3'

if activation["organizer"] == 'y':
    subprocess.run([p, r"./organizer/organizer_main.py"])

if activation["RTOD"] == 'y':
    subprocess.run([p, r"./RTOD/RTOD_main.py"])

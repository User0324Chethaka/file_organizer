import json
import subprocess
import platform

file_path  = r"../activate.json"

user_input = None
with open(file_path, "r") as jf:
    user_input = json.load(jf)

p = None
if platform.system().lower() == 'windows':
    p = 'python' 
else:
    p = 'python3'

if user_input["organizer"] == 'y':
    subprocess.run([p, r"./organizer/organizer_main.py"])

if user_input["RTOD"] == 'y':
    subprocess.run([p, r"./RTOD/RTOD_main.py"])

user_input["organizer"] = "n"
user_input["RTOD"] = "n"
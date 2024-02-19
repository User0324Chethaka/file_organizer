# To edit the defautl file locations of 
# "Documetns", "Music", "Video", "Pictures"
# based on the operating system 

import json
import platform

file_path = r"./program_data/file_date/file_formats.json"
data = None
with open(file_path, "r") as jf:
    data = json.load(jf)

if platform.system().lower == 'windows':
    data["documents"]["location"] = r""
from datetime import datetime, timedelta
import os
import platform
import json
import shutil


def read_input(path_: str) -> dict:
    '''read the content of json files and return it'''

    abs_path = os.path.abspath(path_) # get the absolute path
    with open(abs_path, "r") as jf:
        rtrn = json.load(jf)

    return rtrn

def move_files(file_dict: dict) -> None:
    '''make a main dir inside the specidied dir by the user
    inside the main dir make a dir for each file type
    move files into the dirs they belong'''

    user_input = read_input(r"../RTOD_user_input.json")
    info = user_input["type_and_location"] 
    main_name = str(datetime.now())

    for key, val in file_dict.items():
        location = info[key]
        main_path = os.path.join(location, main_name)
        if not os.path.exists(main_path):
            os.makedirs(main_path)
        
        sub_dir_name = key.upper()
        sub_dir_path = os.path.join(main_path, sub_dir_name)
        os.makedirs(sub_dir_path)

        for file in val:
            shutil.copy2(file.path, sub_dir_path)


def organize_files(file_ls: list) -> None:
    ''' organize files into dictionary based on their file extention '''
    
    file_dict = {}

    for file in file_ls:
        ext = file.name.split(".")[-1]
        if ext not in file_dict.keys():
            file_dict[ext] = []

        file_dict[ext].append(file)
    
    move_files(file_dict)

def get_files(path_: str, file_ls: list) -> None:
    ''' load all the movable files in memory / python list'''
    user_input = read_input(r"../RTOD_user_input.json")

    for item in os.scandir(path_):
        if item.is_dir() and os.listdir(item.path) != []:
            get_files(path_, file_ls)
        elif item.is_file() and item.name.split(".")[-1] in user_input["type_and_location"].keys():
            file_ls.append(item)


def activation() -> None:
    user_input = read_input(r"../RTOD_user_input.json")

    if platform.system().lower() == 'windows':
            # Get the absolute path of the user's profile directory
            user_profile_dir = os.getenv('USERPROFILE')

            # Join the profile directory with the standard "Downloads" directory name
            download_dir = os.path.join(user_profile_dir, "Downloads")
        
    else:
        # Get the absolute path of the user's home directory
        home_dir = os.path.expanduser("~")

        # Join the home directory with the standard "Downloads" directory name
        download_dir = os.path.join(home_dir, "Downloads")

    file_ls = []
    get_files(download_dir, file_ls)

    organize_files(file_ls)

def calculate_delta() -> timedelta:
    user_input = read_input(r"../RTOD_user_input.json")
    time_data = user_input["time_period"]

    for key, val in time_data.itmes():
        if val and val.isdigit():
            time_data[key] = float(val)
        else:
            time_data[key] = float(0)

    delta = timedelta(seconds=time_data["s"],
                      minutes=time_data["min"],
                      hours=time_data["h"],
                      days=time_data["d"],
                      weeks=time_data["w"])

    return delta


def main() -> None:

    user_input = read_input(r"../RTOD_user_input.json")

    if user_input["automatic"].lower() == 'n':
        activation()
    else:
       while True:

        user_input = read_input(r"../RTOD_user_input.json")
        if user_input["stop_auto"] == 'y':
            break

        activation()
        last_run = datetime.now()

        if datetime.now() >= last_run + calculate_delta():
            activation()
            last_run = datetime.now() 


if __name__ == "__main__": 
    main()
from datetime import datetime
import os
import platform
import json
import shutil


def read_input(path_: str) -> dict:
    '''read the content of json files and return it'''

    abs_path: str = os.path.abspath(path_) # get the absolute path
    with open(abs_path, "r") as jf:
        rtrn: dict = json.load(jf)

    return rtrn


def move_files(file_dict: dict) -> None:
    '''make a main dir inside the specidied dir by the user
    inside the main dir make a dir for each file type
    move files into the dirs they belong'''

    user_input: dict = read_input(r"../RTOD_user_input.json")
    info: dict = user_input["type_and_location"] 
    main_name: str = str(datetime.now())

    for key, val in file_dict.items():
        location: str = info[key]
        main_path: str = os.path.join(location, main_name)
        if not os.path.exists(main_path):
            os.makedirs(main_path)
        
        sub_dir_name: str = key.upper()
        sub_dir_path: str = os.path.join(main_path, sub_dir_name)
        os.makedirs(sub_dir_path)

        for file in val:
            shutil.copy2(file.path, sub_dir_path)


def organize_files(file_ls: list[os.DirEntry]) -> None:
    ''' organize files into dictionary based on their file extention '''
    
    file_dict: dict = {}

    for file in file_ls:
        ext: str = file.name.split(".")[-1]
        if ext not in file_dict.keys():
            file_dict[ext] = []

        file_dict[ext].append(file)
    
    move_files(file_dict)

def edit_RTOD_moved_files(ls: list) -> None:
    rel_file_path = r"../program_data/runtime_data/RTOD_moved_files.json"
    abs_file_path = os.path.abspath(rel_file_path)

    with open(abs_file_path, "a") as jf:
        file_: dict = json.load(jf)

        for item in ls:
            file_["moved_files"].append(item)

def get_files(path_: str, file_ls: list) -> None:
    ''' load all the movable files in memory / python list'''

    user_input: dict = read_input(r"../RTOD_user_input.json")
    valid_types: list = list(user_input["type_and_location"].keys())

    moved_files_dict: dict = read_input(r"../program_data/runtime_data/RTOD_moved_files.json")
    moved_files: list[os.DirEntry] = moved_files_dict["moved_files"]
    new_files: list[os.DirEntry] = []

    for item in os.scandir(path_):
        ext: str = item.name.split(".")[-1]

        if item.is_dir() and os.listdir(item.path) != []:
            get_files(path_, file_ls)
        elif item.is_file() and ext in valid_types and item not in moved_files:
            file_ls.append(item)
            new_files.append(item)

    edit_RTOD_moved_files(new_files)


def main() -> None:
    '''activate the program'''

    if platform.system().lower() == 'windows':
            # Get the absolute path of the user's profile directory
            user_profile_dir: str = os.getenv('USERPROFILE')

            # Join the profile directory with the standard "Downloads" directory name
            download_dir: str = os.path.join(user_profile_dir, "Downloads")
        
    else:
        # Get the absolute path of the user's home directory
        home_dir  = os.path.expanduser("~")

        # Join the home directory with the standard "Downloads" directory name
        download_dir: str = os.path.join(home_dir, "Downloads")

    file_ls: list[os.DirEntry] = []
    get_files(download_dir, file_ls)

    organize_files(file_ls)


if __name__ == "__main__": 
    main()
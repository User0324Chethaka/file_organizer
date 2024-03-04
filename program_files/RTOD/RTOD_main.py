from datetime import datetime
import os
import platform
import json
import shutil


def read_input(path_: str, file_type: str) -> dict|list[int]:
    '''read the content of files and return it'''

    abs_path: str = os.path.abspath(path_) # get the absolute path
    rtrn: None|dict|list[int] = None   

    if file_type == 'j':
        with open(abs_path, "r") as jf:
            rtrn: dict = json.load(jf)
    elif file_type == 't':
        with open(abs_path, "r") as f:
            lines: list = f.readlines() 
            rtrn: list[int] = [int(line.strip()) for line in lines]

    return rtrn


def move_files(file_dict: dict) -> None:
    '''make a main dir inside the specidied dir by the user
    inside the main dir make a dir for each file type
    move files into the dirs they belong'''

    user_input: dict = read_input(r"../RTOD_user_input.json")
    info: dict = user_input["type_and_location"] 
    main_name: str = f" RTOD {datetime.now()}"

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


def write_to_inode_data(inode_id):
    with open(os.path.abspath(r"./inode_data.txt"), "a") as f:
        f.write(inode_id)


def did_not_move(path_) -> bool:
    ''' check whether a file was moved during a previous runtime'''

    moved_files: list[int] = read_input(path_, 't')

    file_stat: os.stat_result = os.stat(path_)
    indoe_id: int = file_stat.st_ino

    if indoe_id not in moved_files:
        write_to_inode_data(indoe_id)
        return True
    else:
        return False


def get_files(path_: str, file_ls: list) -> None:
    ''' load all the movable files in memory / python list'''

    user_input: dict = read_input(r"../RTOD_user_input.json")
    valid_types: list = list(user_input["type_and_location"].keys())

    for item in os.scandir(path_):
        ext: str = item.name.split(".")[-1]

        if item.is_dir() and os.listdir(item.path) != []:
            get_files(path_, file_ls)
        elif item.is_file() and ext in valid_types and did_not_move(item.path):
            file_ls.append(item)


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
from datetime import datetime
import os
import platform
import json
import shutil


def read_input(path_: str, file_type: str) -> dict|list[int]|None:
    '''read the content of files and return it'''

    abs_path: str = os.path.abspath(path_) # get the absolute path
    rtrn: None|dict|list[int] = None   

    if file_type == 'j':
        with open(abs_path, "r") as jf:
            rtrn: dict = json.load(jf)
    elif file_type == 't':
        # for the 1st time program running
        if os.path.getsize(abs_path) == 0:
            rtrn = None
        else: 
            with open(abs_path, "r", encoding='utf-8') as f:
                lines: list = f.readlines() 
                rtrn: list[int] = [int(line.strip()) for line in lines]

    return rtrn


def move_files(file_dict: dict) -> None:
    '''make a main dir inside the specidied dir by the user
    inside the main dir make a dir for each file type
    move files into the dirs they belong'''

    user_input: dict = read_input(r"../RTOD_user_input.json", 'j')
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
    ''' update inode_data.txt file'''

    abs_path = os.path.abspath(r"./RTOD/inode_data.txt")
    with open(abs_path, "a", encoding='utf-8') as f:
        f.write(f"{str(inode_id)}\n")


def get_item_data(path_: str) -> tuple[bool, int]:
    ''' check whether a file was moved during a previous runtime'''

    inode_data_file_path: str = os.path.abspath(r"./RTOD/inode_data.txt")
    inode_data: list[int]|None = read_input(inode_data_file_path, 't')

    # moved_files = [] if inode_data = None
    moved_files: list = inode_data if inode_data else []

    file_stat: os.stat_result = os.stat(path_)
    inode_id: int = file_stat.st_ino

    if inode_id not in moved_files:
        return True, inode_id
    else:
        return False, None


def get_files(path_: str, file_ls: list) -> None:
    ''' load all the movable files in memory / python list'''

    user_input: dict = read_input(r"../RTOD_user_input.json", 'j')
    valid_types: list = list(user_input["type_and_location"].keys())

    for item in os.scandir(path_):
        # get file extention
        ext: str = item.name.split(".")[-1]
        
        did_not_move: bool
        inode_id: int|None
        did_not_move, inode_id = get_item_data(item.path)

        if item.is_dir() and os.listdir(item.path) != []:
            get_files(path_, file_ls)
        elif item.is_file() and ext in valid_types and did_not_move:
            file_ls.append(item)
            write_to_inode_data(inode_id)


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

    # organize_files displays unexpected behaviour if called inside get_files()
    organize_files(file_ls)


if __name__ == "__main__": 
    main()
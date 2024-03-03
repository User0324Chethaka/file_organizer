from datetime import datetime
import os
import json
import shutil


def read_input(path_) -> dict:
    '''read the content of json files and return it'''

    rtrn = None
    abs_path = os.path.abspath(path_)
    with open(abs_path, "r") as jf:
        rtrn = json.load(jf)

    return rtrn


def move_files_2_back(path_, category, value, time_, *args):
    ''' move files according to the structure  '''

    main_file_name = time_ 
    main_file_path = os.path.join(path_, main_file_name)
    if not os.path.exists(main_file_path):
        os.makedirs(main_file_path)

    category_file_name = category.upper()
    category_file_path = os.path.join(main_file_path, category_file_name)
    if not os.path.exists(category_file_path):
        os.makedirs(category_file_path)

    for v in value:
        shutil.copy2(v.path, category_file_path)


def move_files_1_back(file_dict, *args):
    '''move files to either custom or default location
       user_input["save_location"] acts as default location '''

    user_input = read_input(r"../organizer_user_input.json")
    time_ = str(datetime.now())
    
    for category, value in file_dict.items():
        if category in user_input["custom"].keys():
            move_files_2_back(user_input["custom"][category],
                         category, 
                         value, 
                         time_)
        else:
            move_files_2_back(user_input["save_location"],
                         category, 
                         value, 
                         time_)
    

def organize_files(file_list):
    ''' organize files into a dictionary '''

    file_dict = {}

    for file in file_list:
        ext = file.name.split(".")[-1]
        if ext not in file_dict.keys():
            file_dict[ext] = []

        file_dict[ext].append(file)

    move_files_1_back(file_dict)


def get_files(path_, all_files):
    '''load all the files in the given file path into memory'''

    user_input = read_input(r"../organizer_user_input.json") 

    for item in os.scandir(path=path_):

        if item.name not in user_input["dont_move"]:
            if item.is_dir() and os.listdir(item.path) != []:
                get_files(path_=item.path, all_files=all_files)
            elif not item.is_dir():
                all_files.append(item)
    

def main():
    user_input = read_input(r"../organizer_user_input.json") 
    src_file_paths = list(user_input["file_locations"])

    for fp in src_file_paths:

        # load all the files that need to be moved to a list
        all_files = [] 

        # check if the dir is empty
        if os.listdir(fp) != []:
            get_files(path_=fp, all_files=all_files)

        organize_files(all_files)

        if user_input["move_and_delete"].lower() == 'y':
            os.rmdir(fp)


if __name__ == '__main__':
    main()

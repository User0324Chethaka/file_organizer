from datetime import datetime
import os
import json
import shutil


def read_input(path) -> dict:
    rtrn = None
    with open(path, "r") as jf:
        rtrn = json.load(jf)

    return rtrn


def move_files_2(path_, category, value, time_):
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


def move_files_1(file_dict):
    user_input = read_input(r"../../organizer_user_input.json")
    time_ = datetime.now()
    
    for category, value in file_dict.itmes():
        if category in user_input["custom"].keys():
            move_files_2(user_input["custom"][category],
                         category, 
                         value, 
                         time_)
        else:
            move_files_2(user_input["save_location"],
                         category, 
                         value, 
                         time_)
    

def organize_files(file_list):
    # organize files into a dictionary
    file_dict = {}

    for file in file_list:
        ext = file.name.split(".")[-1]
        if ext not in file_dict.keys():
            file_dict[ext] = []
            file_dict[ext].append(file)
        else:
            file_dict[ext].append(file)

    move_files_1(file_dict)


def get_files(path_, dont_move):
    # load all the files that need to be moved to a list
    all_files = [] 

    for item in os.scandir(path=path_):
        print(all_files)
        print(item.name, '\n\n\n')
        if item.is_dir():
            if os.listdir(item.path) != []: # chekc whether file is empty
                get_files(item.path, dont_move)
        else:
            if item not in dont_move:
                all_files.append(item)
    
    #remove duplicates
    user_input = read_input(r"../../organizer_user_input.json") 
    if user_input["move_duplicates"].lower() == 'n':
        all_files = set(all_files)

    organize_files(all_files)


def main():
    user_input = read_input(r"../../organizer_user_input.json") 
    file_paths = list(user_input["file_locations"])
    print(file_paths)

    for fp in file_paths:
        print(fp)
        print(os.listdir(fp))
        if os.listdir(fp) != []:
            get_files(fp, user_input["dont_move"])

        if user_input["move_and_delete"].lower() == 'y':
            os.rmdir(fp)


if __name__ == '__main__':
    main()
import os
import json

def get_files(file_list, dir_path):
    file_list = file_list
    elements = os.scandir(path=dir_path)
    for element in elements:
        if elements.is_dir():
            get_files(file_list=file_list, 
                      dir_path=element.path)
        else:
            file_list.append(element.name)

def main():
    file_path = r"../organizer_user_input.json"
    user_input = None
    with open(file_path, "r") as jf:
        user_input = json.load(jf)
    
    all_files = []

    get_files(file_list=all_files,
              dir_path=user_input["file_location"])

if __name__ == '__main__':
    main()
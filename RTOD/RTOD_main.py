import os
import json

def read_input(path_) -> dict:
    '''read the content of json files and return it'''

    rtrn = None
    abs_path = os.path.abspath(path_) # get the absolute path
    with open(abs_path, "r") as jf:
        rtrn = json.load(jf)

    return rtrn

def main():
    pass


if __name__ == "__main__": 
    main()
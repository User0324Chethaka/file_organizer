from datetime import timedelta, datetime
import json
import subprocess
import platform
import os


def get_abs_path(path_: str) -> str:
    return os.path.abspath(path_)

def read_input(path_: str) -> dict:
    '''read the content of json files and return it'''

    abs_path: str = get_abs_path(path_) 
    with open(abs_path, "r") as jf:
        rtrn: dict = json.load(jf)

    return rtrn


def calculate_delta() -> timedelta:
    user_input: dict = read_input(r"../activate.json")
    time_info: dict = user_input["RTOD"]["run_within"]

    for key, val in time_info.items():
        if val and val.isdigit():
            time_info[key] = float(val)
        else:
            time_info[key] = float(0)

    delta = timedelta(hours=time_info["hrs"],
                      minutes=time_info["mins"],
                      seconds=time_info["secs"])

    return delta


def run_RTOD(path_: str, RTOD_info: dict, command: str) -> None:

    if RTOD_info["automate"] == 'y':
        while True: 

            now_time: datetime = datetime.now()
            subprocess.run([command, path_])

            if datetime.now() >= now_time + calculate_delta():
                subprocess.run([command, path_])

            # if the value changed while program runs
            user_input: dict = read_input(r"../activate.json")
            if user_input["RTOD"]["automate"] != 'y':
                print("automated RTOD stopped")
                break

    else:
        subprocess.run([command, path_])


def get_python_command() -> str:

    operating_system: str = platform.system()
    p: str|None = None

    if operating_system.lower() == 'windows':
        p = 'python'
    else:
        p = 'python3'

    return p
    

def main() -> None:

    user_input: dict = read_input(r"../activate.json")

    run_command: str = get_python_command()

    organizer_file_path: str = get_abs_path(r"./organizer/organizer_main.py")
    RTOD_file_path: str = get_abs_path(r"./RTOD/RTOD_main.py")

    if user_input["organizer"].lower() == 'y':
        subprocess.run([run_command, organizer_file_path])

    if user_input["RTOD"]["activate"].lower() == 'y':
        run_RTOD(RTOD_file_path, user_input["RTOD"], run_command)


if __name__ == "__main__": 
    main()


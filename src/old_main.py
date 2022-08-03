"""
File monitoring system
"""
import json
import os
import time


def parse_settings():
    config = {}
    with open('src/settings.json', 'r') as file:
        config = json.load(file)
    return config


def get_current_stats(files:list) -> dict:
    current_stat = {}
    for file in files:
        file_stat = os.stat(file)
        file_stat_dict = {
            "mode": file_stat.st_mode,
            "ino": file_stat.st_ino,
            "dev": file_stat.st_dev,
            "nlink": file_stat.st_nlink,
            "uid": file_stat.st_uid,
            "gid": file_stat.st_gid,
            "size": file_stat.st_size,
            "atime": file_stat.st_atime,
            "mtime": file_stat.st_mtime,
            "ctime": file_stat.st_ctime,
        }
        current_stat[file] = file_stat_dict
    return current_stat


def log_change(log_msg: dict) -> None:
    log_file_path = settings.get("log_file")
    with open(log_file_path, 'a') as log_file:
        log_file.write(json.dumps(log_msg) + "\n")


def monitor_files(files:list) -> None:
    # logging the first state of files 
    previous_stat = get_current_stats(files)
    for file in files:
        log_data = {"log_ts": time.strftime("%Y-%m-%d %I:%M:%S %p %z"), 'file': file, "file_stat": previous_stat[file]}
        log_change(log_data)
    # monitoring the current state of files
    while True:
        current_stat = get_current_stats(files)
        if current_stat != previous_stat:
            for file in files:
                if current_stat[file] != previous_stat[file]:
                    log_data = {"log_ts": time.strftime("%Y-%m-%d %I:%M:%S %p %z"), 'file': file, "file_stat": current_stat[file]}
                    log_change(log_data)
            previous_stat = current_stat

        time.sleep(2)


def check_file_existance(files):
    return all(os.path.exists(file) for file in files)

def main():
    if settings.get("input_files"):
        files = settings.get("input_files")
        if check_file_existance(files):
            monitor_files(files)
        else:
            print("No such files in files/ directory")
    else:
        print("No files to monitor...")

if __name__ == "__main__":
    print("Strting main")
    settings = parse_settings()
    main()
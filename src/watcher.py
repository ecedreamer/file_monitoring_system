"""
File monitoring system
"""
import json
import os
import time


class FileWatcher:
    def __init__(self, settings_path) -> None:
        print("Initializing file watcher...")
        self.settings_path = settings_path
        self.settings = self.parse_settings()
        self.files = self.get_files()
        self.verify_initial_condition()

    def parse_settings(self):
        print("Parsing settings from settings.json file...")
        settings = {}
        with open(self.settings_path, 'r') as file:
            settings = json.load(file)
        return settings

    def verify_initial_condition(self):
        print("Verifying initial conditions...")
        if not self.check_file_existance(self.files):
            raise FileNotFoundError("Input file/s not found.")

    def get_files(self):
        all_files = []
        for location in self.settings.get("input_files"):
            if os.path.isfile(location):
                all_files.append(location)
            elif os.path.isdir(location):
                all_files.extend(f"{location}{file}" for file in os.listdir(
                    location) if os.path.isfile(f"{location}{file}"))
        return all_files

    @staticmethod
    def check_file_existance(files):
        return all(os.path.exists(file) for file in files)

    def get_current_stats(self):
        current_stat = {}
        for file in self.files:
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

    def log_change(self, log_msg: dict) -> None:
        log_file_path = self.settings.get("log_file")
        with open(log_file_path, 'a') as log_file:
            log_file.write(json.dumps(log_msg) + "\n")

    def start_monitoring(self):
        print("Starting to monitor files...")
        files = self.files
        # logging the first state of files
        previous_stat = self.get_current_stats()
        for file in files:
            log_data = {
                "log_ts": time.strftime("%Y-%m-%d %I:%M:%S %p %z"), 'file': file, "remarks": "Initial file stats before monitoring.", "file_stat": previous_stat[file]
            }
            self.log_change(log_data)
        # monitoring the current state of files
        while True:
            current_stat = self.get_current_stats()
            if current_stat != previous_stat:
                for file in files:
                    if current_stat[file] != previous_stat[file]:
                        print(f"File: {file} modified...")
                        log_data = {
                            "log_ts": time.strftime("%Y-%m-%d %I:%M:%S %p %z"), 'file': file, "remarks": "file modified.",          "file_stat": current_stat[file]
                        }
                        self.log_change(log_data)
                previous_stat = current_stat

            # default to 1 second.
            time.sleep(self.settings.get("monitor_delay", 1))


if __name__ == "__main__":
    watcher = FileWatcher(settings_path="src/settings.json")
    watcher.start_monitoring()

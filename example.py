from src.watcher import FileWatcher


def main():
    setting_file_path = "src/settings.json"
    file_watcher = FileWatcher(settings_path=setting_file_path)
    file_watcher.start_monitoring()


if __name__ == "__main__":
    main()
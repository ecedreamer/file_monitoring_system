## File Monitoring System ##

This module can be used to monitor specific files or files inside a folder. When specified file is modified, it detects that and logs the new stat of the file so that the change is tracked properly for future analysis. 

### Usage ###

Uses is very simple.

* First define a settings.json file in your suitable project directory. 

#### sample settings.json file ####
```
{
    "input_files": [
        "files/sample_input_file1.txt",
        "files/sample_input_file2.txt",
        "files/logs/"
    ],
    "log_file": "logs/default_log.txt",
    "monitor_delay": 0.5
}

```
Setting file Description:
    
    input_files: valid files and folder list, only put valid path
    log_file: watcher uses this path to log changes
    monitor_delay: delay in second for file monitoring, default 1 second

* Code example

```
# import FileWatcher
from src.watcher import FileWatcher


def main():
    # define settings.json file location
    setting_file_path = "src/settings.json"
    # make a FileWatcher instance
    file_watcher = FileWatcher(settings_path=setting_file_path)
    # call start_monitoring method to start monitoring
    file_watcher.start_monitoring()


if __name__ == "__main__":
    main()
```

Enjoy! Happy Coding !!
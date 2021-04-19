import sys
import logging
import win32api
import wmi
from lib.watchdog.observers import Observer
from lib.watchdog.events import LoggingEventHandler


# 다중 옵저버 띄우기 테스트(리스트)_windows_테스트 완료
if __name__ == "__main__":
    logging.basicConfig(filename='./pc_log',
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    paths = list(win32api.GetLogicalDriveStrings().split('\000')[:-1])
    event_handler = LoggingEventHandler()
    cdDrive = wmi.WMI()

    for path in paths:
        for cdrom in cdDrive.Win32_CDROMDrive():
            if path == cdrom.Drive+'\\':
                paths.remove(cdrom.Drive + '\\')

    for path in paths:
        observer = Observer()
        observer.schedule(event_handler, path + '\\', recursive=True)
        observer.start()

    try:
        while observer.isAlive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# 단일 옵저버 띄우기 테스트 완료
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s - %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S')
#     path = 'C:\\' # sys.argv[1] if len(sys.argv) > 1 else '.'
#     event_handler = LoggingEventHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path, recursive=True)
#     observer.start()
#     try:
#         while observer.isAlive():
#             observer.join(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()

# 다중 옵저버 띄우기 테스트(하드코딩)
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s - %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S')
#     path1 = 'C:\\' # sys.argv[1] if len(sys.argv) > 1 else '.'
#     path2 = 'D:\\'
#     event_handler = LoggingEventHandler()
#     observer1 = Observer()
#     observer1.schedule(event_handler, path1, recursive=True)
#     observer1.start()
#     observer2 = Observer()
#     observer2.schedule(event_handler, path2, recursive=True)
#     observer2.start()
#     try:
#         while observer1.isAlive():
#             observer1.join(1)
#     except KeyboardInterrupt:
#         observer1.stop()
#     observer1.join()




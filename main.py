import sys
import logging
import win32api
import wmi
import lib.fileIO.readFile as readFile
from lib.watchdog.observers import Observer
from lib.watchdog.events import LoggingEventHandler
import os

current_location = str(os.path.abspath(os.path.dirname(sys.argv[0])))
fileMaxByte = 1024 * 1024 * 10
readFile.readFile() # 변경파일 리드 프로세스 실행


# 다중 옵저버 띄우기 테스트(리스트)_windows_테스트 완료
if __name__ == "__main__":
    logging.basicConfig(filename=current_location+'\\pc_log.txt',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        # format='%(asctime)s - %(message)s',
                        format='%(message)s'
                        ) # 로깅
    paths = list(win32api.GetLogicalDriveStrings().split('\000')[:-1])
    event_handler = LoggingEventHandler()
    cdDrive = wmi.WMI() # CD롬 드라이브 저장

    for path in paths: # CD롬 드라이브 제거
        for cdrom in cdDrive.Win32_CDROMDrive():
            if path == cdrom.Drive+'\\':
                paths.remove(cdrom.Drive + '\\')

    for path in paths: # 각 드라이브 별 옵저버 실행
        observer = Observer()
        observer.schedule(event_handler, path + '\\', recursive=True)
        observer.start()

    try:
        while observer.isAlive():

            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

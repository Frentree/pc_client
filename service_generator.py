import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
import time
import subprocess
import os
import psutil

# 프로세스가 실행중인지 확인
def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# 서비스 생성 및 관리
class ServiceGenerator(win32serviceutil.ServiceFramework):
    _svc_name_ = "erwatch"
    _svc_display_name_ = "erwatch"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = False

    def SvcStop(self):
        # Main.exe Process Kill
        subprocess.Popen("taskkill /im Main.exe /f", shell=True) # 서비스 중지 시 Main.exe 프로세스 taskkill 명령어로 중지
        time.sleep(1)

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False # is_running을 False로 바꿔 줌으로써 Main.exe 주기적 호출 막기
        win32event.SelfEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.is_running = True
        current_location = str(os.path.abspath(os.path.dirname(sys.argv[0]))) # 현재 위치 체크
        subprocess.Popen([current_location + "\\Main.exe"])

        while self.is_running:
            is_main = checkIfProcessRunning("Main")
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
            if rc == win32event.WAIT_OBJECT_0:
                break
            elif not is_main:
                subprocess.Popen([current_location + "\\Main.exe"])
            time.sleep(55)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ServiceGenerator)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ServiceGenerator)


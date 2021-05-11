# exe 생성(exe만 생성해선 안되고 서비스로 생성해야함)
pyinstaller -F main.py

# 서비스 파일 생성 명령어
pyinstaller -F --hidden-import=win32timezone -n service.exe service_generator.py
# psutil을 히든으로 임포트 해줘야 빌드 시 라이브러리 적용됨
pyinstaller -F --hidden-import=win32timezone --hidden-import=psutil -n service.exe service_generator.py

# 서비스 생성 명령어(cmd에서 관리자로 실행)
service.exe --startup=auto install

# 서비스 삭제 명령어(cmd에서 관리자로 실행)
service.exe remove

# 서비스 실행 시 오류로 인한 조치(서비스를 실행할 수 없습니다. 오류 5: 엑세스 거부)

HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control
ServicesPipeTimeout 생성 후 DWORD Decimal 60000 설정 후 재부팅
-> 해당값 6000000까지 설정해 보았으나 영향 업성서 해당 레지스트리 제거 

# 하기는 그룹에 네트워크 퍼미션 추가하는데 해도 적용 안됨
https://serverfault.com/questions/469944/how-to-add-network-service-to-users-permission-group

https://stackoverflow.com/questions/18569611/how-to-create-a-windows-service-in-python

sc create "[YourService]" binPath= "C:\Program Files\Windows Resource Kits\srvany.exe"

HKEY_LOCAL_MACHINE > SYSTEM > CurrentControlSet > Services > [YourService]

HKEY_LOCAL_MACHINE > SYSTEM > CurrentControlSet > Services > [YourService]





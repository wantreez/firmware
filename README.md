# firmware
RaspberryPi3에서 FHD영상을 재생하는 python 기반의 펌웨어 입니다.
MusicSignature앱과 연동하여 wifi를 컨트롤 할 수 있습니다.

## 1. how to use
### 1.1 블루투스 세팅하기
```
sudo apt update
sudo apt install -y bluetooth bluez phython-bluez vim
  
sudo vi /etc/systemd/system/dbus-org.bluez.service
    edit : ExecStart=/usr/lib/bluetooth/bluetooth -C
```
### 1.2 플레이어 설치
```
  sudo install apt -y install omxplayer
```

### 1.3 디렉토리 생성
```
  cd /home/pi
  mkdir job log firmware movie cm
```

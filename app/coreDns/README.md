# coreDns 셋업

### 설치

```
# raspberry pi 3은 arm7(32bit) 을 사용하므로 해당 arch 전용으로 빌드된 바이너리를 사용해야 한다 
wget https://github.com/coredns/coredns/releases/download/v1.9.0/coredns_1.9.0_linux_arm.tgz
tar -xvzf coredns_1.9.0_linux_arm.tgz
```

### 서비스 등록

```
# core-dns.service 파일을 아래 경로에 복사해준다.
sudo cp ./core-dns.service /etc/systemd/system/core-dns.service

# 서비스 시작, status 로 정상 실행되었는지 확인, enable로 서비스 등록
sudo systemctl start core-dns

sudo systemctl status core-dns
    > ● core-dns.service - CoreDns
    >      Loaded: loaded (/etc/systemd/system/core-dns.service; disabled; vendor p>
    >      Active: active (running) since Mon 2022-02-21 03:46:06 KST; 5s ago
    >    Main PID: 3050 (start.sh)
    >       Tasks: 12 (limit: 1597)
    >         CPU: 154ms
    >      CGroup: /system.slice/core-dns.service
    >              ├─3050 /bin/bash /home/pi/app/coreDns/start.sh
    >              ├─3051 sudo /home/pi/app/coreDns/coredns -conf /home/pi/app/core>
    >              └─3052 /home/pi/app/coreDns/coredns -conf /home/pi/app/coreDns/C>
    > 
    >  2월 21 03:46:06 raspberry1 systemd[1]: Started CoreDns.
    >  2월 21 03:46:06 raspberry1 sudo[3051]:     root : PWD=/ ; USER=root ; COMMAN>
    >  2월 21 03:46:06 raspberry1 sudo[3051]: pam_unix(sudo:session): session opene>
    >  2월 21 03:46:06 raspberry1 start.sh[3052]: .:53
    >  2월 21 03:46:06 raspberry1 start.sh[3052]: sans.:53
    >  2월 21 03:46:06 raspberry1 start.sh[3052]: CoreDNS-1.9.0
    >  2월 21 03:46:06 raspberry1 start.sh[3052]: linux/arm, go1.17.6, ace3dcb

sudo systemctl enable core-dns
```
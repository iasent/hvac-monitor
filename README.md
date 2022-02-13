# hvac-monitor

라즈베리파이에 co2, 온습도, 미세먼지 센서를 연결하고, flask 서버를 열어 값을 http로 확인할 수 있다.

센서는 다음 3개를 사용한다. 아래 링크의 코드와 예제를 참조했다.
- senseAir s8 이산화탄소 센서 : http://co2meters.com/Documentation/AppNotes/AN168-S8-raspberry-pi-uart.pdf
- dht-22 온습도센서 : https://github.com/adafruit/Adafruit_Python_DHT (https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22 가이드 참고)
- pms7003 미세먼지 센서 : https://github.com/eleparts/PMS7003 (연결 가이드 포함)

### 구성

센서와 통신 포트는 다음과 같이 연결해준다.
- senseAir s8: /dev/serial0 (tx, rx 핀)
- pms7003: /dev/ttySOFT0 (gpio 17, 27번 핀)
- dht-22: gpio 4번 핀

라즈베리파이를 최신으로 업데이트해준다.(이유는 아래 설명)

```
sudo apt update
sudo apt full-upgrade
sudo reboot
```

setup.sh 를 실행한다.
```
sudo ./setup.sh
```

동작은 각 센서명.py 을 직접 실행해서 확인할 수도 있다.

start.sh 스크립트는 플라스크 서버를 실행시킨다.
```
./start.sh
```

서비스로 등록하고자 하면 다음과 같이 한다.

```
# /etc/systemd/system/hvac-monitor.service 파일 생성

[Unit]
Description=hvac-monitor

[Service]
Type=simple
User=pi
ExecStart=/home/pi/Documents/Github/hvac-monitor/start.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
```
sudo systemctl start hvac-monitor
sudo systemctl enable hvac-monitor
```

### soft_uart

s8 센서와 pms7003 센서는 시리얼 통신을 사용한다.

라즈베리파이의 gpio 에는 한 쌍의 tx, rx 핀만 있으므로 남는 gpio 핀을 시리얼 통신에 사용하기 위해 추가 모듈이 필요하다.

https://github.com/adrianomarto/soft_uart

gpio 17, 27 번 핀을 추가적으로 시리얼 통신에 사용할 수 있도록 해준다.
성능 이슈로 4800 bps 이상의 통신 속도를 사용하지 않기를 권장하나, 테스트 해 보니 3b+ 에서는 문제가 없었다.
이제 시리얼 통신에 ttySOFT0 포트를 추가로 사용할 수 있다.

모듈의 README.md 를 따라하다 보면, sudo apt-get install raspberrypi-kernel-headers 로 설치되는 header 버전이 os와 맞지않아 컴파일이 제대로 안 되는 경우가 있는데
라즈베리파이를 최신 버전으로 업데이트해주면 된다.
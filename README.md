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

### 업데이트

2025년 기준 내장 스크립트들이 먹통이고 docker 도 arm32v7 이미지로 만들어진데다(64bit os가 나와서 aarch64 로 가야됨)
라이브러리들도 최신버전과 호환 문제가 있다.

해당 내용을 정리한다.

##### Adafruit_Python_DHT
해당 모듈 os 확인이 바로 되지 않아 install 시 --force-pi 옵션이 필요하다.

dht-22.py 에서 import 하는 모듈 이름을 변경해야 한다.
```
# import Adafruit_DHT.Raspberry_Pi_2_Driver as driver 
import Adafruit_DHT.Raspberry_Pi_Driver as driver
```

##### soft_uart
헤더파일의 함수 시그니쳐가 바뀌었다.

``` module.c
# old: static int soft_uart_write(struct tty_struct* tty, const unsigned char* buffer, int buffer_size)
static ssize_t soft_uart_write(struct tty_struct* tty, const u8* buffer, size_t buffer_size);

# old: static int soft_uart_write(struct tty_struct* tty, const unsigned char* buffer, int buffer_size)
static void soft_uart_set_termios(struct tty_struct* tty, const struct ktermios* termios);
```
해당 함수의 헤더 선언부와 메소드 구현부, 2벌을 각각 바꿔줘야 한다. (총 4라인)

``` raspberry_soft_uart.c
# old: gpio_set_debounce(gpio_rx, 1000 / baudrate / 2);

struct gpio_desc *desc = gpio_to_desc(gpio_rx);
if (desc)
    gpiod_set_debounce(desc, 1000 / baudrate / 2);
```
gpio_set_debounce 함수의 이름이 gpiod_set_debounce 로 바뀌었다. 해당 부분 수정이 필요하다.

soft_uart 라이브러리는 기본 gpio 포트를 17, 27을 사용하는데
라즈베리파이 6.6. 버전부터 물리 gpio 포트와, os 내부에서 사용하는 gpio 포트가 바뀌었다.
[https://stackoverflow.com/questions/78452048/not-able-to-access-gpio-pins-on-my-raspberry-pi-5/78888765#78888765]

```
cat /sys/kernel/debug/gpio | grep 17 // os 에서 사용하는 물리 gpio 17 포트의 주소 확인
```

위 명령어로 확인시, 지금 기준 17-529, 27-539 로 확인되었다.
확인한 이름으로 insmod 시에 적용해준다.

``` soft_uart.sh
sudo insmod /home/sans/Documents/Github/hvac-monitor/soft_uart/soft_uart.ko gpio_tx=529 gpio_rx=539
```

명령이 오류없이 잘 수행되었는지 dmesg 로 꼭 확인해준다.

```
dmesg | tail -n 50
```

##### hvac_monitor

호기롭게 pip install -r requirements.txt 를 실행하고 싶겠지만
라즈베리파이 최신버전에선 전역 python 에 pip install 을 때릴수가 없다.

해당 환경용 venv 를 만들어준다.

```
python -m venv hvac-env
source hvac-env/bin/activate
pip install -r requirements.txt
```

이러고 나서 모듈 설치도 하고 위 변경사항들도 반영해주고 한다.


### soft_uart

s8 센서와 pms7003 센서는 시리얼 통신을 사용한다.

라즈베리파이의 gpio 에는 한 쌍의 tx, rx 핀만 있으므로 남는 gpio 핀을 시리얼 통신에 사용하기 위해 추가 모듈이 필요하다.

https://github.com/adrianomarto/soft_uart

gpio 17, 27 번 핀을 추가적으로 시리얼 통신에 사용할 수 있도록 해준다.
성능 이슈로 4800 bps 이상의 통신 속도를 사용하지 않기를 권장하나, 테스트 해 보니 3b+ 에서는 문제가 없었다.
이제 시리얼 통신에 ttySOFT0 포트를 추가로 사용할 수 있다.

모듈의 README.md 를 따라하다 보면, sudo apt-get install raspberrypi-kernel-headers 로 설치되는 header 버전이 os와 맞지않아 컴파일이 제대로 안 되는 경우가 있는데
라즈베리파이를 최신 버전으로 업데이트해주면 된다.

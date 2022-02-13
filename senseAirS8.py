import serial
import time

#RPi pin connections:
#pin 6 GND
#pin 4 5v
#pin 8 TXD: UART data to S8
#pin 10 RXD: UART data from S8

class SenseAirS8:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def get(self):
        self.ser.flushInput()
        self.ser.write(b"\xFE\x44\x00\x08\x02\x9F\x25")

        response = self.ser.read(7)

        if len(response) < 4:
            raise Exception('illegal response from senseAir S8')

        high = response[3]
        low = response[4]

        return {
            'co2': (high * 256) + low
        }


# example
if __name__=='__main__':
    s8 = SenseAirS8('/dev/serial0')
    time.sleep(0.1)

    print(s8.get())

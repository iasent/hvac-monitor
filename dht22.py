import sys
import Adafruit_DHT.Raspberry_Pi_2_Driver as driver

DHT_SUCCESS        =  0
DHT_ERROR_TIMEOUT  = -1
DHT_ERROR_CHECKSUM = -2
DHT_ERROR_ARGUMENT = -3
DHT_ERROR_GPIO     = -4
TRANSIENT_ERRORS = [DHT_ERROR_CHECKSUM, DHT_ERROR_TIMEOUT]

class DHT22:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        result, humidity, temp = driver.read(22, int(self.pin))

        if result in TRANSIENT_ERRORS:
            return (None, None)
        elif result == DHT_ERROR_GPIO:
            raise RuntimeError('Error accessing GPIO.')
        elif result != DHT_SUCCESS:
            raise RuntimeError('Error calling DHT test driver read: {0}'.format(result))

        return {
            'humidity': humidity, 
            'temperature': temp 
        }

    def get(self, retries=5, delay_seconds=1, platform=None):
        for i in range(retries):
            try:
                return self.read()
            except Exception as e:
                time.sleep(delay_seconds)

        raise Exception('illegal response from dht22')


# example
if __name__=='__main__':
    dht = DHT22(4)
    print(dht.get())

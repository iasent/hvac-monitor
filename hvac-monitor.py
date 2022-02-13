from flask import Flask, make_response
from dht22 import DHT22
from pms7003 import PMS7003
from senseAirS8 import SenseAirS8

app = Flask(__name__)

dht22 = DHT22(4)
pms7003 = PMS7003('/dev/ttySOFT0')
s8 = SenseAirS8('/dev/serial0')

@app.route('/dht22', methods = ["GET"])
def dht_22():
    return make_response(
        dht22.get(),
        200
    )

@app.route('/pms7003', methods = ["GET"])
def pms_7003():
    return make_response(
        pms7003.get(),
        200
    )


@app.route('/s8', methods = ["GET"])
def sense_air_s8():
    return make_response(
        s8.get(),
        200
    )

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)

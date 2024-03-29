from flask import Flask, make_response
from dht22 import DHT22
from pms7003 import PMS7003
from senseAirS8 import SenseAirS8

from werkzeug.datastructures import Headers

app = Flask(__name__)

dht22 = DHT22(4)
pms7003 = PMS7003('/hvac/dev/ttySOFT0')
s8 = SenseAirS8('/hvac/dev/serial0')

header = Headers()
header.add('Content-Type', 'text/plain')

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

ht = {"humidity":0, "temperature":0}
co2 = {"co2":0}
pms = {"pm1.0":0, "pm2.5":0, "pm10.0":0, "0.3um_in_0.1L_of_air":0, "0.5um_in_0.1L_of_air":0, "1.0um_in_0.1L_of_air":0, "2.5um_in_0.1L_of_air":0, "5.0um_in_0.1L_of_air":0, "10.0um_in_0.1L_of_air":0}

@app.route('/hvac', methods = ["GET"])
def hvac_monitor():
    global dht22, pms7003, s8, header, ht, co2, pms
    try:
        nht = dht22.get()
        if type(nht) is not dict:
            raise
        ht = nht
    except:
        pass

    try:
        nco2 = s8.get()
        co2 = nco2
    except:
        pass

    try:
        npms = pms7003.get()
        pms = npms
    except:
        pass

    result = f"""humidity {ht["humidity"]:.1f}
                temperature {ht["temperature"]:.1f}
                co2 {co2["co2"]}
                particulate_matter{{pm="1.0"}} {pms["pm1.0"]}
                particulate_matter{{pm="2.5"}} {pms["pm2.5"]}
                particulate_matter{{pm="10.0"}} {pms["pm10.0"]}
                in_0_1L_of_air{{size="0.3"}} {pms["0.3um_in_0.1L_of_air"]}
                in_0_1L_of_air{{size="0.5"}} {pms["0.5um_in_0.1L_of_air"]}
                in_0_1L_of_air{{size="1.0"}} {pms["1.0um_in_0.1L_of_air"]}
                in_0_1L_of_air{{size="2.5"}} {pms["2.5um_in_0.1L_of_air"]}
                in_0_1L_of_air{{size="5.0"}} {pms["5.0um_in_0.1L_of_air"]}
                in_0_1L_of_air{{size="10.0"}} {pms["10.0um_in_0.1L_of_air"]}
            """.replace("    ", "")

    return make_response(
        result,
        200,
        header
    )

@app.route('/health', methods = ["GET"])
def health():
    return make_response(
        "alive",
        200,
        header
    )   

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)

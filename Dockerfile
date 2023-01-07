FROM arm32v7/python:3.11-alpine3.17

RUN apk add gcc libc-dev && \
    mkdir -p /hvac/dev
COPY . /hvac

WORKDIR /hvac

RUN pip install -r requirements.txt && \
    python ./Adafruit_Python_DHT/setup.py install

ENTRYPOINT ["python", "hvac-monitor.py"]

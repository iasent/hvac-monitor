#!/bin/bash
docker rm -f prometheus

docker run \
    --name prometheus \
    -p 9090:9090 \
    -v /home/pi/app/prometheus:/etc/prometheus \
    -v /mnt/ssd/prometheus:/data \
    prom/prometheus-linux-armv7
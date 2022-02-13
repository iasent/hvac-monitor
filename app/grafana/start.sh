#!/bin/bash
# https://github.com/grafana/grafana/issues/43002 이슈로 8.2.7 사용
docker rm -f grafana

docker run \
    --name grafana \
    --user 1000 \
    -p 3000:3000 \
    -v /home/pi/app/grafana:/etc/grafana \
    -v /mnt/ssd/grafana:/var/lib/grafana \
    grafana/grafana:8.2.7
#!/bin/bash
docker run -d -p 8080:8080 -v /dev/ttySOFT0:/hvac/dev/ttySOFT0 -v /dev/serial0:/hvac/dev/serial0 --privileged giutgiutdev/hvac-monitor:latest

#!/bin/bash
SCRIPT_PATH=`dirname "$0"`
cd $SCRIPT_PATH

cd soft_uart
sudo insmod soft_uart.ko
cd ..

python hvac-monitor.py > /dev/null 2>&1
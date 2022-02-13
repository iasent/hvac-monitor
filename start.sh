#!/bin/bash
SCRIPT_PATH=`dirname "$0"`

sudo insmod $SCRIPT_PATH/soft_uart/soft_uart.ko
python $SCRIPT_PATH/hvac-monitor.py > /dev/null 2>&1
#!/bin/bash
EXECUTION_PATH=`pwd -P`
SCRIPT_PATH=`dirname "$0"`
cd $SCRIPT_PATH

sudo apt-get install raspberrypi-kernel-headers

git submodule update --init --recursive
sudo pip install -r requirements.txt
cp -r ./Adafruit_Python_DHT/source .
sudo python ./Adafruit_Python_DHT/setup.py install

cd soft_uart
make
sudo make install

cd $EXECUTION_PATH
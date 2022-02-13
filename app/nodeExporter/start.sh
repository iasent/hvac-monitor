#!/bin/bash

BASE_DIR=/home/pi/app
APP_DIR=$BASE_DIR/nodeExporter

$APP_DIR/node_exporter/node_exporter --collector.systemd --collector.processes
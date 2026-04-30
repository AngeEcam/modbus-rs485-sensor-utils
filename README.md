# modbus-rs485-sensor-utils
## About this repository

This repository provides lightweight Python utilities to read and configure RS485 Modbus RTU sensors commonly used in environmental monitoring (temperature, humidity, pressure).

Each sensor has its own dedicated folder containing ready-to-use scripts to scan the bus, read data and change the Slave ID if needed. The tools are cross-platform (macOS, Linux, Windows) and require no additional software beyond Python and two pip packages.

## Download a single sensor folder

If you only need a specific sensor, you can download just its folder without cloning the entire repository:

1. Go to **https://download-directory.github.io/**
2. Paste the URL of the sensor folder you want

**Example for the S-THP-01A sensor:**
https://github.com/AngeEcam/modbus-rs485-sensor-utils/tree/master/sensors/sthp01a
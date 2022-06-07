<h1 align=center>
Airview-Cars-InfluxDB
</h1>

**Contact**: CaderIdrisGH@outlook.com

---

Unofficial Python3 script that reads measurement files output by two AirView cars used in the Breathe London Pilot Scheme, decodes the measurements and exports them to an InfluxDB 2.x database.

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#requirements">Requirements</a> •
  <a href="#operational-procedure">Operational Procedure</a> •
  <a href="#airview-data-files">AirView Data Files</a> •
  <a href="#settings">Settings</a> •
  <a href="#api">API</a> •
  <a href="#license">License</a>
</p>

---

## Key Features

- Parses raw measurement files from AirView cars into a human readable format
- Uploads the measurements to an InfluxDB 2.x database

---

## Requirements

- This program was developed with Python 3.9.7 for an Ubuntu 20.04 LTS machine
	- Earlier versions of Python 3 and different linux distributions may work but are untested
- python3-pip and python3-venv are required for creating the virtual environment for the program to run in
- Dependencies listed in requirements.txt (automatically installed with [venv_setup.sh](./venv_setup.sh))
- Raw data output from AirView cars used in the Breathe London Pilot Scheme (Not provided)

---

## AirView Data Files

### Raw CSV File

The AirView cars were measuring data every second across 9 devices, each measuring multiple variables. Up to 87 parameters were measured per car, every second. The measurements were recorded to a csv formatted file and uploaded to a cloud server, with a new file being generated every 5 minutes. A abridged set of measurements from one of the files is provided below:

|Timestamp|Instrument Number:Parameter Name|Paramater ID|Instrument Status Code|Measurement Value|Measurement Index|
|---|---|---|---|---|---|
|2019-08-25_04-16-28.000000|Devices:5:BC ch1|57|00010000|4464.000000|827636731|
|2019-08-25_04-16-28.000000|Devices:5:BC ch2|58|00010000|4451.000000|827636732|
|2019-08-25_04-16-28.000000|Devices:5:BC ch3|59|00010000|4075.000000|827636733|
|2019-08-25_04-16-28.000000|Devices:5:BC ch4|60|00010000|3538.000000|827636734|
|2019-08-25_04-16-28.000000|Devices:5:BC ch5|61|00010000|3872.000000|827636735|
|2019-08-25_04-16-28.000000|Devices:5:BC ch6|62|00010000|4170.000000|827636736|
|2019-08-25_04-16-28.000000|Devices:5:BC ch7|63|00010000|3974.000000|827636737|
|2019-08-25_04-16-28.000000|Devices:1:air humidity|17|00000000|83.417274|827636738|
|2019-08-25_04-16-28.000000|Devices:1:air pres|16|00000000|1015.961548|827636739|
|2019-08-25_04-16-28.000000|Devices:1:air temp|15|00000000|17.448870|827636740|
|2019-08-25_04-16-28.000000|Devices:1:cn|1|00000000|1728.834595|827636741|
|2019-08-25_04-16-28.000000|Devices:1:pm1|2|00000000|0.052846|827636743|
|2019-08-25_04-16-28.000000|Devices:1:pm10|5|00000000|0.057256|827636744|
|2019-08-25_04-16-28.000000|Devices:1:pm2.5|3|00000000|0.055745|827636745|
|2019-08-25_04-16-28.000000|Devices:1:pm4|4|00000000|70.242000|827636746|
|2019-08-25_04-16-28.000000|Devices:1:pmt|6|00000000|0.057371|827636747|
|2019-08-25_04-16-28.000000|Devices:8:RH|142||55.000000|827636748|
|2019-08-25_04-16-28.000000|Devices:8:pm|140||75.690000|827636749|
|2019-08-25_04-16-28.000000|Devices:8:pressure|143||764.000000|827636750|
|2019-08-25_04-16-28.000000|Devices:8:temperature|141||26.300000|827636751|
|2019-08-25_04-16-28.000000|Devices:7:no2|133|10104|24.953000|827636755|
|2019-08-25_04-16-28.000000|Devices:9:altitude|146|A|8.400000|827636705|
|2019-08-25_04-16-28.000000|Devices:9:latitude|144|A|51.425507|827636709|
|2019-08-25_04-16-28.000000|Devices:9:longitude|145|A|-0.345400|827636710|
|2019-08-25_04-16-28.000000|Devices:9:speed|147|A|0.000000|827636712|
|2019-08-25_04-16-28.000000|Devices:2:LDSA|21|00000102|6.200000|827636720|
|2019-08-25_04-16-28.000000|Devices:2:RH|23|00000102|38.100000|827636721|
|2019-08-25_04-16-28.000000|Devices:2:Temperature|22|00000102|30.600000|827636722|
|2019-08-25_04-16-28.000000|Devices:4:gas flow|49|00000040|0.638964|827636725|
|2019-08-25_04-16-28.000000|Devices:4:no|45|00000040|-0.013167|827636726|
|2019-08-25_04-16-28.000000|Devices:3:Flow module output|41|00001fff|11.117000|827636727|
|2019-08-25_04-16-28.000000|Devices:3:co2|32|00001fff|489.125000|827636728|
|2019-08-25_04-16-28.000000|Devices:3:co2 dry|33|00001fff|496.963000|827636729|
|2019-08-25_04-16-28.000000|Devices:3:h2o|34|00001fff|15.770300|827636730|

### Understanding the Measurements

This program uses at the following values recorded to the csv file:
- Timestamp
	- Denotes when the measurement was made
- Device Number
	- It used this value to look up the name of the device
- Parameter ID
	- Used to find the name of the parameter and the units of the measurement in (metadata.json)[./metadata/metadata.json] and (carq_parameters.csv)[./metadata/car1_parameters.csv] respectively. The name is found by using the parameter ID instead of Parameter Name to improve formatting
- Measurement
	- The value of the parameter measured at that time
- Instrument Status Code
	- Instruments 1-7 output status codes that inform of of the conditions the measurements were made in
	- Instruments 1-6 output a 8 nibble hex representation of the status code, Instrument 7 output a 5 digit quinary
	- These had to be decoded, full details can be found in (statuses.pdf)[./metadata/statuses.pdf]

---

## Operational Procedure

```
# Clone this repository
$ git clone https://github.com/CaderIdris/AirView-Cars-InfluxDB.git

# Go in to repository
$ cd AirView-Cars-InfluxDB

# Setup the virtual environment
$ ./venv_setup.sh

# Configure settings.json with file path and InfluxDB configuration

# Add auth token data to auth.json

# Run software
$ ./run.sh
```

---

## Settings

---

## API

---

## License

GNU General Public License v3

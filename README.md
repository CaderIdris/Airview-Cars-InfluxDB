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

### config.json

|Key|Type|Description|Options|
|---|---|---|---|
||||
|**Influx**|Subcategory|Contains all config info relevant to InfluxDB 2.x database|-|
|*Bucket*|`str`|Bucket to export data to|Any valid bucket|
|*IP*|`str`|IP address of InfluxDB 2.x database|IP of database, localhost if hosted on same machine|
|*Port*|`str`|Port of InfluxDB 2.x database|Port of database (usually 8086)|
|*Token*|`str`|Auth token for InfluxDB 2.x database|Auth token provided by your admin|
|*Organisation*|`str`|Organisation your token is associated with|Organisation associated with auth token|
|||||
|**Settings**|Subcategory|Contains all other settings|-|
|*File Path*|`str`|Path to folder contianing directories for AirView car data|Any valid path|
|*Cars*|`list` of `str`|Names of AirView cars, name should match subdirectory that measurements can be found in|A list of any valid name for an AirView Car|
|*Debug Stats*|`bool`|Print debug stats?|true/false|


---

## API

### [main.py](./main.py)
The main script for running the program, utilises modules found in [modules](./modules/) using config specified in [Settings](./Settings)

#### Command line arguments:

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|-c / --config|`str`|Alternate path to config file, use `/` in place of `\`|N|Settings/config.json|
|-m / --metadata|`str`|Alternate path to metadata file, use `/` in place of `\`|N|metadata/metadata.json|
|-p / --parameters|`str`|Alternate path to parameters file, use `/` in place of `\`|N|metadata/car1_parameters.csv|

### [airview.py](./modules/airview.py)
Contains classes and methods that read raw measurements from AirView cars and reformat them in preparation for upload to an InfluxDB 2.x database. All status codes are read and converted in to a human readable format.

#### Classes

##### AcoemRequest
Handles raw measurements, converting metadata to human readable format and formatting the data

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*car*|`str`|Which AirView car were the measurements made by|Y|None|
|*metadata*|`dict`|Enables translation of status codes to human readable format|Y|None|
|*paramaters*|`DataFrame`|Contains name and units of measured parameters, used to convert from parameter id to human readable name|Y|None|


###### Attributes

| Attribute | Type | Description |
|---|---|---|
|*car*|`str`|Which AirView car were the measurements made by|
|*measurements*|`list`|List of dicts, each representing measurements made at a point in time|
|*metadata*|`dict`|Enables translation of status codes to human readable format|
|*parameters*|`DataFrame`|Contains name and units of measured parameters, used to convert from parameter id to human readable name|
|*previous_date*|`datetime`|The date the previous measurement was made. If the date of the row being read is greater than the *previous_date* attribute, a new data container is made and the current one is added to the *measurements* attribute|
|*data_container*|`dict` or `None`|Contains all measurement info for a single point in time in a format suitable for upload to an InfluxDB 2.x database|

###### Methods

**read_file**

Reads a csv file generated by AirView cars

- Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*file_path*|`str`|Path to the csv file being analysed|Y|None|


**read_row**

Reads a row from a csv file generated by an AirView car and parses the information provided

- Keyword arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*row*|`Series`|Row from a csv file|Y|None|

**read_status**

Reads a status string from the csv file and converts it to a human readable name 

- Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*raw_code*|`str`|Raw status code in the form of either an 8 nibble hex or a 5 digit quinary number|Y|None|
|*instrument*|`str`|What instrument the status code corresponds to|Y|None|
|*number*|`str`|The instrument number|Y|None|

**get_measurements**

Returns list of measurements formatted for InfluxDB 2.x database 

- Keyword Arguments

None

- Returns 

List of measurements formatted for InfluxDB 2.x database (**measurements** attribute)

**clear_measurements**

Clears all measurements from memory 

- Keyword Arguments 

None

- Returns 

None

### [influxwrite.py](./modules/influxwrite.py)

Contains functions and classes pertaining to writing data to InfluxDB 2.x database

#### Classes

##### InfluxWriter

Handles connection and export to InfluxDB 2.x database

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*influx_config*|`dict`|Contains all info relevant to connecting to InfluxDB database|

###### Attributes

| Attribute | Type | Description |
|---|---|---|
|*config*|`dict`|Config info for InfluxDB 2.x database|
|*client*|`InfluxDBClient`|Client object for InfluxDB 2.x database|
|*write_client*|`InfluxDBClient.write_api`|Write client object for InfluxDB 2.x database|

###### Methods

**write_container_list

Writes list of measurement containers to InfluxDB 2.x database, synchronous write used as asynchronous write caused memory issues on a 16 GB machine.

- Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*list_of_containers*|`list`|Exports list of data containers to InfluxDB 2.x database|

Containers must have the following keys:
|Key|Description|
|---|---|
|*time*|Measurement time in datetime format|
|*measurement*|Name of measurement in the bucket|
|*fields*|Measurements made at *time*|
|*tags*|Metadata for measurements made at *time*|

- Returns
None

### [idristools.py](./modules/idristools.py)

#### Methods

Set of tools I find useful in all my programs

##### fancy_print

Makes a nicer output to the console

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*str_to_print*|`str`|String that gets printed to console|Y|None|
|*length*|`int`|Character length of output|N|70|
|*form*|`str`|Output type (listed below)|N|NORM|
|*char*|`str`|Character used as border, should only be 1 character|N|\U0001F533 (White box emoji)|
|*end*|`str`|Appended to end of string, generally should be `\n` unless output is to be overwritten, then use `\r`|N|\r|
|*flush*|`bool`|Flush the output stream?|N|False|

**Valid options for _form_**
| Option | Description |
|---|---|
|TITLE|Centres the string, one char at start and end|
|NORM|Left aligned string, one char at start and end|
|LINE|Prints line of *char* of specified *length*|

##### get_json

Open json file and return as dict

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*path_to_json*|`str`|The path to the json file, can be relative e.g Settings/config.json|Y|None|

###### Returns

`dict` containing contents of json file

###### Raises

|Error Type|Cause|
|---|---|
|`FileNotFoundError`|File is not present|
|`ValueError`|Formatting error in json file, such as ' used instead of " or comma after last item|

##### save_to_file 

Saves data to file in specified path. Format agnostic will write what is passed if it is in string format (e.g json, csv, txt)

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*write_data*|`str`|Data to be written to file|Y|None|
|*path_to_file*|`str`|Path to save file to|Y|None|
|*filename*|`str`|Name of file to write data to, file format should be included (e.g \*.csv)|Y|None|

##### debug_stats

Prints out a json file/dictionary nicely. Prints nested dicts up to a depth of *max_level*

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*stats*|`dict`|Dict to print to console|Y|None|
|*line_length*|`int`|Number of columns that can be printed before the string is wrapped to the next line|N|120|
|*level*|`int`|How far dict is already nested|N|1|
|*max_level*|`int`|How deep in to a nested dict the function will print|N|3|

##### unread_files

Scans a directory for a list of files and then removes any files if they are present in the *read_list* variable

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*path*|`str`|Path to directory containing files to be read|Y|None|
|*read_list*|`str`|Path to file containing a list of all previously read files|Y|None|
|*return_stats*|`bool`|Returns stats with the list of unread files if true|N|False|

###### Returns 

if *return_stats* is True:
- `dict` contaning "*Unread File List*" `list`, "*Total Files*" `int` representing the total number of files in *path* and "*Read Files*" `int` representing the number of unread files in *path*

else:
- `list` of all unread files in *path*

##### append_to_file 

Appends a line to a file

###### Keyword Arguments 

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*line*|`str`|What to append to the file (newline character is added by the function)|Y|None|
|*file*|`str`|Path to the file to append to|Y|None|


---

## License

GNU General Public License v3

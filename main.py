#!/bin/python3

""" Reads raw data files recorded by a trial version of AirView cars used in
the first iteration of the Breathe London Network and writes the measurements
to an InfluxDB 2.0 database

As part of the first iteration of the Breathe London Network, two AirView cars
drove around London recording the concentrations of many different air
pollutants as well as environmental variables. This program reads the raw files
generated by these cars, converts the metadata in to a human readable form and
writes the data to an InfluxDB 2.0 database.

    Command Line Arguments:
        -c/--config (str) [OPTIONAL]: Alternate path to config file

        -m/--metadata (str) [OPTIONAL]: Alternate path to metadata file

        -p/--parameters (str) [OPTIONAL]: Alternate path to parameters file

    Parameters:
        
"""

__author__ = "Idris Hayward"
__copyright__ = "2021, University of Surrey & National Physical Laboratory"
__credits__ = ["Idris Hayward"]
__license__ = "GNU General Public License v3.0"
__version__ = "0.4"
__maintainer__ = "Idris Hayward"
__email__ = "j.d.hayward@surrey.ac.uk"
__status__ = "Beta"

import argparse
import json
import datetime as dt
import pandas as pd

from modules.idristools import fancy_print, debug_stats, get_json
from modules.idristools import unread_files, append_to_file
from modules.airview import AirView
from modules.influxwrite import InfluxWriter

if __name__ == "__main__":
    # Parse incoming arguments
    arg_parser = argparse.ArgumentParser(
            description = "Reads raw data files from first iteration of "
            "AirView cars, converts metadata to human readable format and "
            "writes measurements to InfluxDB 2.0 database"
            )
    arg_parser.add_argument(
            "-c",
            "--config",
            type = str,
            help = "Alternate location for config json file (Defaults to "
            "./Settings/config.json)",
            default = "Settings/config.json"
            )
    arg_parser.add_argument(
            "-m",
            "--metadata",
            type = str,
            help = "Alternate location for metadata json file (Defaults to "
            "./metadata/metadata.json)",
            default = "metadata/metadata.json"
            )
    arg_parser.add_argument(
            "-p",
            "--parameters",
            type = str,
            help = "Alternate location for parameters csv file (Defaults to "
            "./metadata/car1_parameters.csv)",
            default = "metadata/car1_parameters.csv"
            )
    args = vars(arg_parser.parse_args())
    config_path = args["config"]
    meta_path = args["metadata"]
    para_path = args["parameters"]

    # Opening blurb
    fancy_print("", form="LINE")
    fancy_print("AirView Car Data Tool", form="TITLE")
    fancy_print(f"Author: {__author__}")
    fancy_print(f"Contact: {__email__}")
    fancy_print(f"Version: {__version__}")
    fancy_print(f"Status: {__status__}")
    fancy_print(f"License: {__license__}")
    fancy_print("", form="LINE")

    # Get config files
    config_json = get_json(config_path)
    fancy_print(f"Imported settings from {config_path}")

    # Debug stats
    if config_json["Settings"]["Debug Stats"]:
        debug_stats(config_json)
    fancy_print("", form="LINE")

    # Import metadata json and parameter csv
    fancy_print("Importing metadata files", end="\r", flush=True)
    meta_json = get_json(meta_path)
    para_csv = pd.read_csv(
            header=None,
            filepath_or_buffer=para_path,
            usecols=[0, 1, 2]
            )
    fancy_print("Metadata imported")
    fancy_print("", form="LINE")

    # Connect to influx
    fancy_print("Connecting to InfluxDB database")
    influx_writer = InfluxWriter(config_json["Influx"])
    fancy_print("Connected")
    fancy_print("", form="LINE")

    # Main loop
    for car in config_json["Settings"]["Cars"]:
        files_processed = list()
        airview = AirView(car, meta_json, para_csv)
        fancy_print(f"Importing measurements from {car}")
        files_path = f"{config_json['Settings']['File Path']}/{car}/"
        files_dict = unread_files(
                files_path,
                f"{config_json['Settings']['File Path']}/{car}.txt",
                return_stats=True
                )
        unread_files = files_dict["Unread File List"]
        fancy_print(f"{files_dict['Total Files']} available")
        fancy_print(f"{files_dict['Read Files']} already read")
        prev_file_date = dt.datetime(1970, 1, 1, 0, 0, 0)
        t_start = dt.datetime.now()
        for file_index, airview_file in enumerate(unread_files):
            file_date_string = airview_file[14:]
            try:
                file_date = dt.datetime.strptime(
                        file_date_string, 
                        "%Y-%m-%d_%H-%M-%S"
                        )
            except ValueError:
                file_date = prev_file_date
            file_date = file_date.replace(minute=0, second=0, microsecond=0)
            if file_date != prev_file_date and len(airview.measurements) > 0:
                files_left = len(unread_files) - (file_index + 1)
                fancy_print(
                        f"Uploading measurements for " \
                                f"{prev_file_date.strftime('%Y-%m-%d %H:%M:%S')}",
                        end="\r", flush=True
                        )
                measurements_to_send = airview.get_measurements()
                # print(*measurements_to_send, sep="\n")
                influx_writer.write_container_list(measurements_to_send)
                finish_time = (dt.datetime.now() - t_start).seconds
                fancy_print(
                        f"Measurements for " \
                        f"{prev_file_date.strftime('%Y-%m-%d %H:%M:%S')} " \
                        f"uploaded ({finish_time} seconds, " \
                        f"{len(measurements_to_send)} measurements, " \
                        f"{files_left} remaining)"
                        )
                airview.clear_measurements()
                for processed_file in files_processed:
                    append_to_file(
                            f"{processed_file}",
                            f"{config_json['Settings']['File Path']}/{car}.txt"
                            )
                files_processed = list()
                t_start = dt.datetime.now()
            fancy_print(f"Reading {airview_file}", end="\r", flush=True)
            airview.read_file(f"{files_path}{airview_file}")
            prev_file_date = file_date
            files_processed.append(airview_file)
        fancy_print(f"Uploading final measurements for {car}", 
                end="\r", flush=True
                )
        measurements_to_send = airview.get_measurements()
        influx_writer.write_container_list(measurements_to_send)
        airview.clear_measurements()
        fancy_print(f"Final measurements for {car} uploaded")
        fancy_print("", form="LINE")


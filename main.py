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
__version__ = "0.1"
__maintainer__ = "Idris Hayward"
__email__ = "j.d.hayward@surrey.ac.uk"
__status__ = "Indev"

import argparse
import json

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

    # Main loop
    for car in config_json["Settings"]["Cars"]:
        pass


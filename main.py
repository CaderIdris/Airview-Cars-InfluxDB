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
    args = vars(arg_parser.parse_args())
    config_path = args["config"]

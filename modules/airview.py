#!/bin/python3

""" Contains classes and methods that read raw measurements from AirView cars

This module contains classes and methods to read raw measurements from AirView
cars, convert the metadata to a human readable format and format the
measurements so they can be saved as a file or written to a database.

    Classes: 
        AirView: Handles reading raw measurements, converting metadata to human
        readable format and formatting the data
        
"""

__author__ = "Idris Hayward"
__copyright__ = "2021, University of Surrey & National Physical Laboratory"
__credits__ = ["Idris Hayward"]
__license__ = "GNU General Public License v3.0"
__version__ = "0.3"
__maintainer__ = "Idris Hayward"
__email__ = "j.d.hayward@surrey.ac.uk"
__status__ = "Alpha"

import pandas as pd
import datetime as dt
from collections import defaultdict as dd

class AirView:
    """ Handles raw measurements, converting metadata to human readable format
    and formatting the data

    Attributes:
        car (str): Serial number of the car

        measurements (list): List of containers, each representing measurements
        made at a point in time
        
        metadata (dict): Contains info on how to convert status codes in to
        human readable forms

        parameters (dataframe): Contains name and units of measured paramters,
        used to convert from parameter to id to human readable name

    Methods:
    __init__: Initialises class

    """

    def __init__(self, car, metadata, parameters):
        """ Initialises class
        """
        self.car = car
        self.measurements = list()
        self.metadata = metadata
        self.parameters = parameters
        self.previous_date = dt.datetime(1970, 1, 1, 0, 0, 0)
        self.data_container = None

    def read_file(self, file_path):
        """ Reads a csv file generated by the AirView cars

        Keyword arguments:
            file_path (str): path to file to be analysed
        """
        # Open and format file
        file_data_raw = pd.read_csv(
                filepath_or_buffer=file_path,
                header=None,
                names=[
                    "Datetime",
                    "Device",
                    "Parameter ID",
                    "Status",
                    "Measurement",
                    "Measurement Number"
                    ],
                on_bad_lines='skip',
                )
        file_data = file_data_raw.drop_duplicates()
        file_data["Datetime"] = pd.to_datetime(
                file_data["Datetime"],
                format="%Y-%m-%d_%H-%M-%S.%f",
                )


        # Read csv 
        for index, row in file_data.iterrows():
            if self.previous_date != row["Datetime"]:
                if self.data_container is not None:
                    self.measurements.append(self.data_container)
                self.data_container = {
                        "measurement": "AirView",
                        "time": row["Datetime"],
                        "fields": dict(),
                        "tags": {"Car": self.car}
                        }
                self.read_row(row)
            else:
                self.read_row(row)
        self.measurements.append(self.data_container)

    def read_row(self, row):
        instrument_number = str(row["Device"]).split(":")[1]
        instrument_name = self.metadata["Devices"][instrument_number]
        measurement = str(self.parameters.iloc[int(row["Parameter ID"]) - 1, 1])
        units = str(self.parameters.iloc[int(row["Parameter ID"]) - 1, 2])
        measurement_name = f"{instrument_name} {measurement} {units}"
        self.data_container["fields"][measurement_name] = float(
                row["Measurement"]
                )
        if int(instrument_number) <= 7:
            self.read_status(row["Status"], instrument_name, instrument_number)

    def read_status(self, raw_code, instrument, number):
        status_string = ""
        separator = ""
        if int(number) <= 6:
            # The trigger bit corresponds to whatever bit corresponds to a
            # particular status code e.g if the 16th bit of instrument 1's
            # status code is 1, that means there is a sensor flow error.
            # The trigger bit is 0 for some instruments and 1 for others.
            status_data = self.metadata["Status"]["8 Nibble Hex"][number]
            trigger_bit = status_data["Trigger"]
            code = f"{int(status, 16):0>32b}"[::-1]
            for bit, status in list(status_data.items()):
                if bit is not 'Trigger':
                    if code[int(bit)] == trigger_bit:
                        status_string = f"{status_string}{separator}{status}"
                        separator = ", "
            if status_string == "":
                status_string = "5x5"
        elif int(number) == 7:
            status_data = self.metadata["Status"]["5 Digit Quinary"][number]
            for quit in list(status_data.keys()):
                status_string = f"{status_string}{separator}{status_data[quit][raw_code[int(quit)]]}"
                separator = ", "
        self.data_container["tags"][f"{instrument} Status"] = status_string

        def get_measurements(self):
            return self.measurements

        def clear_measurements(self):
            self.measurements = list()


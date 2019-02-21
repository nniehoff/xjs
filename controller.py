#!/usr/bin/env python3

import pendulum
import re


class Controller:
    zerodate = pendulum.from_format("0", "x", tz="UTC")

    def __init__(self, controllerinfo={}):
        """
        Create a Controller object with basic information from controller
        object in a juju status output
        """
        # Default Values
        self.notes = []
        self.models = []

        # Required Variables
        self.timestampprovided = False
        self.timestamp = Controller.zerodate

        # Calculated Values
        if "timestamp" in controllerinfo:
            self.timestampprovided = True
            if re.match(r"Z$", controllerinfo["timestamp"]):
                self.timestamp = pendulum.from_format(
                    "01 Jan 1970 " + controllerinfo["timestamp"],
                    "DD MMM YYYY HH:mm:ss",
                    tz="UTC",
                )
            else:
                self.timestamp = pendulum.from_format(
                    "01 Jan 1970 " + controllerinfo["timestamp"],
                    "DD MMM YYYY HH:mm:ssZ",
                )

    def update_timestamp(self, date):
        """
        Timestamps from juju status for controllers only contain a time but all
        other timestamps in the juju status contain dates and times.  We need
        to "guess" and get as close as possible to an accurate date for a
        controller.  For some versions of juju there is no timestamp, so we
        will "guess" at a time as well.
        """
        # if the timestamp was not provided use the latest date
        # if it was provided we only have a time but no date, we should use
        # the latest date from any other status gathered
        if self.timestampprovided:
            # Hard Case - Get the time from the existing timestamp:
            # Goal Format %d %b %Y %H:%M:%S%z
            str_time = self.timestamp.format('HH:mm:ssZ')
            # Get the date from the passed in date
            str_date = date.format("DD MMM YYYY")
            # create a tempdate:
            temp_date = pendulum.from_format(
                str_date + " " + str_time, "DD MMM YYYY HH:mm:ssZ"
            )
            if temp_date > self.timestamp:
                self.timestamp = temp_date
        else:
            if date > self.timestamp:
                self.timestamp = date

    def add_model(self, model):
        """Add a model to a controller"""
        self.models.append(model)

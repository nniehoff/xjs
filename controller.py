#!/usr/bin/env python3

from datetime import datetime
import requests


class Controller:
    zerodate = datetime.strptime("00:00:00Z", "%H:%M:%SZ")

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
            self.timestamp = datetime.strptime(
                controllerinfo["timestamp"], "%H:%M:%SZ"
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
            # Goal Format %d %b %Y %H:%M:%SZ
            str_time = self.timestamp.strftime("%H:%M:%SZ")
            # Get the date from the passed in date
            str_date = date.strftime("%d %b %Y")
            # create a tempdate:
            temp_date = datetime.strptime(
                str_date + " " + str_time, "%d %b %Y %H:%M:%SZ"
            )
            if temp_date > self.timestamp:
                self.timestamp = temp_date
        else:
            if date > self.timestamp:
                self.timestamp = date

    def add_model(self, model):
        """Add a model to a controller"""
        self.models.append(model)

    def update_app_version_info(self):
        """
        Connect to the Juju Charms API and get the latest version of charms
        """
        url = "https://api.jujucharms.com/v4/meta/id?"
        data = {}

        # https://api.jujucharms.com/v4/meta/id?id=cs:xenial/hacluster&id=cs:~containers/bionic/easyrsa&id=nick
        for model in self.models:
            for app in model.applications:
                if app.charmorigin == "jujucharms":
                    url += "id=" + app.charmid + "&"

        response = None
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

        for model in self.models:
            for app in model.applications:
                if app.charmorigin == "jujucharms":
                    if app.charmid in data and "Revision" in data[app.charmid]:
                        app.charmlatestrev = data[app.charmid]["Revision"]
                        app.notes.append(
                            "Stable Rev (" + str(app.charmlatestrev) + ")"
                        )

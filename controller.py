#!/usr/bin/env python3
# This file is part of xjs a tool used to disply offline juju status
# Copyright 2019 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.


import re
import pendulum
import requests


class Controller:
    zerodate = pendulum.from_format("0", "x", tz="UTC")

    def __init__(self, controllername, controllerinfo={}):
        """
        Create a Controller object with basic information from controller
        object in a juju status output
        """
        # Default Values
        self.notes = []
        self.models = {}
        self.name = controllername

        # Required Variables
        self.timestampprovided = False
        self.timestamp = Controller.zerodate

        # Calculated Values
        if "timestamp" in controllerinfo:
            self.timestampprovided = True
            if re.match(r".*Z$", controllerinfo["timestamp"]):
                self.timestamp = pendulum.from_format(
                    "01 Jan 1970 " + controllerinfo["timestamp"],
                    "DD MMM YYYY HH:mm:ss",
                    tz="UTC",
                )
            else:
                self.timestamp = pendulum.from_format(
                    "01 Jan 1970 " + controllerinfo["timestamp"],
                    "DD MMM YYYY HH:mm:ss",
                )

    def __dict__(self):
        return {self.name: self}

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
            str_time = self.timestamp.format("HH:mm:ssZ")
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
        self.models[model.name] = model

    def update_app_version_info(self):
        """
        Connect to the Juju Charms API and get the latest version of charms
        """
        url = "https://api.jujucharms.com/v4/meta/id?"
        data = {}

        for modelname, model in self.models.items():
            for appname, app in model.applications.items():
                if app.charmorigin == "jujucharms":
                    url += "id=" + app.charmid + "&"

        response = None
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
        except:
            print("WARNING: Unable to reach jujucharms.com")

        for modelname, model in self.models.items():
            for appname, app in model.applications.items():
                if app.charmorigin == "jujucharms":
                    if app.charmid in data and "Revision" in data[app.charmid]:
                        app.charmlatestrev = data[app.charmid]["Revision"]
                        if app.charmrev < app.charmlatestrev:
                            app.notes.append(
                                "Stable Rev (" + str(app.charmlatestrev) + ")"
                            )
                        elif app.charmrev > app.charmlatestrev:
                            app.notes.append("Using Non-Stable Rev")

    def filter_dictionary(self, dictionary, key_filter):
        return {
            key: value
            for (key, value) in dictionary.items()
            if key_filter in key
        }

    def filter_models(self, model_filter):
        self.models = self.filter_dictionary(self.models, model_filter)

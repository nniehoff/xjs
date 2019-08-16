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
from colors import Color
import pendulum
from unit import Unit


class Application:
    column_names = [
        "App",
        "Version",
        "Status",
        "Scale",
        "Charm",
        "Store",
        "Rev",
        "OS",
        "Series",
        "Notes",
    ]

    def __init__(self, appname, appinfo, model):
        """
        Create an Application object with basic information from an application
        object from a juju status output
        """
        # Default Values
        self.notes = []
        self.units = {}
        self.subordinates = {}
        self.version = ""
        self.message = ""
        self.relations = {}
        self.endpointbindings = {}
        self.charmlatestrev = -1

        # Required Variables
        self.name = appname
        self.model = model
        self.charm = appinfo["charm"]
        if "series" in appinfo:
            self.series = appinfo["series"]
        else:
            self.series = "NA"

        if "os" in appinfo:
            self.os = appinfo["os"]
        else:
            self.os = "NA"

        isv1 = False
        if "charm-origin" in appinfo:
            self.charmorigin = appinfo["charm-origin"]
        else:
            self.charmorigin = "NA"
            isv1 = True

        if "charm-name" in appinfo:
            self.charmname = appinfo["charm-name"]
        else:
            self.charmname = "NA"
            isv1 = True

        if "charm-rev" in appinfo:
            self.charmrev = int(appinfo["charm-rev"])
        else:
            self.charmrev = -1
            isv1 = True

        # Handle v1 Charm info:
        if isv1:
            match = re.match(r"(.*):(.*)-(\d+)", self.charm)
            if match:
                charmsource = match.group(1)
                if charmsource == "cs":
                    self.charmorigin = "jujucharms"
                else:
                    self.charmorigin = match.group(1)
                self.charmname = match.group(2)
                self.charmrev = int(match.group(3))
                seriesmatch = re.match(
                    r"^(~[^/]+/)*([^/]+)/[^/]+", match.group(2)
                )
                if seriesmatch:
                    self.series = seriesmatch.group(2)

        self.exposed = appinfo["exposed"]

        if "application-status" in appinfo:
            statuskey = "application-status"
        elif "service-status" in appinfo:
            statuskey = "service-status"
        else:
            statuskey = "none"

        if statuskey in appinfo and "current" in appinfo[statuskey]:
            self.status = appinfo[statuskey]["current"]
        else:
            self.status = "NA"

        # Required Dates

        if statuskey in appinfo and "since" in appinfo[statuskey]:
            if re.match(r".*Z$", appinfo[statuskey]["since"]):
                self.since = pendulum.from_format(
                    appinfo[statuskey]["since"],
                    "DD MMM YYYY HH:mm:ss",
                    tz="UTC",
                )
            else:
                self.since = pendulum.from_format(
                    appinfo[statuskey]["since"], "DD MMM YYYY HH:mm:ssZ"
                )
            model.controller.update_timestamp(self.since)

        # Optional Variables
        if "message" in appinfo[statuskey]:
            self.message = appinfo[statuskey]["message"]
        if "version" in appinfo:
            self.version = appinfo["version"]
        if "relations" in appinfo:
            self.relations = appinfo["relations"]
        if "endpoint-bindings" in appinfo:
            self.endpointbindings = appinfo["endpoint-bindings"]
        if "can-upgrade-to" in appinfo:
            match = re.match(r"\D+(\d+)$", appinfo["can-upgrade-to"])
            if match:
                self.charmlatestrev = int(match.group(1))
            self.canupgradeto = appinfo["can-upgrade-to"]

        # Calculated Values
        if self.exposed:
            self.notes.append("exposed")
        self.charmid = ""
        match = re.match(r"(cs:~[^/]+)\/([^/]+/)*([^/]+)-\d+$", self.charm)
        if match:
            self.charmid = (
                match.group(1) + "/" + self.series + "/" + match.group(3)
            )
        else:
            match = re.match(r"cs:(.*)-\d+$", self.charm)
            if match:
                self.charmid = "cs:" + self.series + "/" + match.group(1)
        if self.charmorigin != "jujucharms":
            self.notes.append("Not from Charm Store")

        # Handle Units
        if "units" in appinfo:
            for unitname, unitinfo in appinfo["units"].items():
                unit = Unit(unitname, unitinfo, self)
                self.units[unitname] = unit

    def __dict__(self):
        return {self.name: self}

    def add_subordinate(self, subunit):
        """Add a subordinate relationship"""
        self.subordinates[subunit.name] = subunit

    def get_scale(self):
        """
        Return the scale of an application which is the number of units and/or
        subordinate units
        """
        return len(self.units) + len(self.subordinates)

    # TODO These colors should return a color not a string
    def get_status_color(self):
        """Return a status string with correct colors based on status"""
        if self.status == "active":
            return Color.Fg.Green + self.status + Color.Reset
        elif self.status in ("error", "blocked"):
            return Color.Fg.Red + self.status + Color.Reset
        elif self.status == "waiting":
            return self.status
        elif self.status == "maintenance":
            return Color.Fg.Orange + self.status + Color.Reset
        else:
            return Color.Fg.Yellow + self.status + Color.Reset

    def get_scale_color(self):
        """Return a scale string with correct colors based on scale"""
        scale = self.get_scale()
        if scale == 0:
            return Color.Fg.Red + str(scale) + Color.Reset
        else:
            return str(scale)

    def get_charmrev_color(self):
        """
        Return a charm revision string with correct colors based on the
        revision
        """
        if self.charmlatestrev == -1:
            return str(self.charmrev)
        if self.charmrev < self.charmlatestrev:
            return Color.Fg.Yellow + str(self.charmrev) + Color.Reset
        elif self.charmrev == self.charmlatestrev:
            return Color.Fg.Green + str(self.charmrev) + Color.Reset
        else:
            return Color.Fg.Red + str(self.charmrev) + Color.Reset

    def get_charmorigin_color(self):
        """
        Return a charm origin string with correct colors based on the origin
        """
        if self.charmorigin != "jujucharms":
            return Color.Fg.Yellow + self.charmorigin + Color.Reset
        else:
            return self.charmorigin

    def get_row(
        self, color, include_controller_name=False, include_model_name=False
    ):
        """Return a list which can be used for a row in a table."""

        row = []
        if color:
            row = [
                self.name,
                self.version,
                self.get_status_color(),
                self.get_scale_color(),
                self.charm,
                self.get_charmorigin_color(),
                self.get_charmrev_color(),
                self.os,
                self.series,
                ", ".join(self.notes),
            ]
        else:
            row = [
                self.name,
                self.version,
                self.status,
                str(self.get_scale()),
                self.charm,
                self.charmorigin,
                str(self.charmrev),
                self.os,
                self.series,
                ", ".join(self.notes),
            ]
        if include_model_name:
            row.insert(0, self.model.name)
        if include_controller_name:
            row.insert(0, self.model.controller.name)
        return row

    def get_column_names(
        self, include_controller_name=False, include_model_name=False
    ):
        """Append the controller name and/or model name as necessary"""
        if include_model_name:
            self.column_names.insert(0, "Model")
        if include_controller_name:
            self.column_names.insert(0, "Controller")
        return self.column_names

    def filter_dictionary(self, dictionary, key_filter):
        return {
            key: value
            for (key, value) in dictionary.items()
            if key_filter in key
        }

    def filter_units(self, unit_filter):
        self.units = self.filter_dictionary(self.units, unit_filter)

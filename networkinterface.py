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

from colors import Color


class NetworkInterface:
    column_names = [
        "Machine",
        "Interface",
        "IP",
        "MAC",
        "Gateway",
        "Space",
        "Up",
        "Notes",
    ]

    def __init__(self, interfacename, interfaceinfo, parent, model):
        """
        Create a NetworkInterface object with basic information from a network
        interface object from a juju status output
        """
        # Default Values
        self.space = ""
        self.notes = []
        self.gateway = ""

        # Required Variables
        self.name = interfacename
        self.parent = parent
        self.ipaddresses = interfaceinfo["ip-addresses"]
        self.macaddress = interfaceinfo["mac-address"]
        self.up = interfaceinfo["is-up"]
        self.model = model

        # Optional Variables
        if "space" in interfaceinfo:
            self.space = interfaceinfo["space"]
        if "gateway" in interfaceinfo:
            self.gateway = interfaceinfo["gateway"]

    def __dict__(self):
        return {self.name: self}

    def get_isup_color(self):
        """Return a is up string with correct colors based on juju status"""
        if self.up:
            return Color.Fg.Green + str(self.up) + Color.Reset
        else:
            return Color.Fg.Red + str(self.up) + Color.Reset

    def get_row(
        self, color, include_controller_name=False, include_model_name=False
    ):
        """Return a list which can be used for a row in a table."""
        row = []
        notesstr = ", ".join(self.notes)
        ipstr = ",".join(self.ipaddresses)
        if color:
            row = [
                self.parent.name,
                self.name,
                ipstr,
                self.macaddress,
                self.gateway,
                self.space,
                self.get_isup_color(),
                notesstr,
            ]
        else:
            row = [
                self.parent.name,
                self.name,
                ipstr,
                self.macaddress,
                self.gateway,
                self.space,
                str(self.up),
                notesstr,
            ]

        if include_model_name:
            row.insert(0, self.model.name)
        if include_controller_name:
            row.insert(0, self.model.controller.name)
        return row

    def get_column_names(
        self, include_controller_name=False, include_model_name=False
    ):
        if include_model_name:
            self.column_names.insert(0, "Model")
        if include_controller_name:
            self.column_names.insert(0, "Controller")
        return self.column_names

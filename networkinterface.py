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

    def __init__(self, interfacename, interfaceinfo, parent):
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

        # Optional Variables
        if "space" in interfaceinfo:
            self.space = interfaceinfo["space"]
        if "gateway" in interfaceinfo:
            self.gateway = interfaceinfo["gateway"]

    def get_isup_color(self):
        """Return a is up string with correct colors based on juju status"""
        if self.up:
            return Color.Fg.Green + str(self.up) + Color.Reset
        else:
            return Color.Fg.Red + str(self.up) + Color.Reset

    def get_row(self, color):
        """Return a list which can be used for a row in a table."""
        notesstr = ", ".join(self.notes)
        ipstr = ",".join(self.ipaddresses)
        if color:
            return [
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
            return [
                self.parent.name,
                self.name,
                ipstr,
                self.macaddress,
                self.gateway,
                self.space,
                str(self.up),
                notesstr,
            ]

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
from networkinterface import NetworkInterface
import pendulum


class BasicMachine:
    """
    A BasicMachine Object is inherited by Machines and Containers so common
    attributes and functions remain here
    """

    column_names = [
        "Machine",
        "Agent",
        "Status",
        "DNS",
        "Inst id",
        "Series",
        "AZ",
        "Arch",
        "Cores",
        "Memory",
        "Message",
        "Notes",
    ]

    def __init__(self, name, info, controller):
        """
        Create a BasicMachine object with basic information from a machine or
        container object from a juju status output
        """
        # Default Values
        self.notes = []
        self.networkinterfaces = {}

        # Required Variables
        self.name = name
        self.jujustatus = info["juju-status"]["current"]
        self.jujuversion = info["juju-status"]["version"]
        self.dnsname = info["dns-name"]
        self.ipaddresses = info["ip-addresses"]
        self.instanceid = info["instance-id"]
        self.machinestatus = info["machine-status"]["current"]
        self.machinemessage = info["machine-status"]["message"]
        self.series = info["series"]

        # Required Dates
        if re.match(r".*Z$", info["juju-status"]["since"]):
            self.jujusince = pendulum.from_format(
                info["juju-status"]["since"], "DD MMM YYYY HH:mm:ss", tz="UTC"
            )
        else:
            self.jujusince = pendulum.from_format(
                info["juju-status"]["since"], "DD MMM YYYY HH:mm:ssZ"
            )
        controller.update_timestamp(self.jujusince)
        if re.match(r".*Z$", info["machine-status"]["since"]):
            self.machinesince = pendulum.from_format(
                info["machine-status"]["since"],
                "DD MMM YYYY HH:mm:ss",
                tz="UTC",
            )
        else:
            self.machinesince = pendulum.from_format(
                info["machine-status"]["since"], "DD MMM YYYY HH:mm:ssZ"
            )
        controller.update_timestamp(self.machinesince)

        # Handle Network Interfaces
        if "network-interfaces" in info:
            for interfacename, interfaceinfo in info[
                "network-interfaces"
            ].items():
                self.networkinterfaces[interfacename] = NetworkInterface(
                    interfacename, interfaceinfo, self
                )

    def __dict__(self):
        return {self.name: self}

    def get_jujustatus_color(self):
        """Return a status string with correct colors based on juju status"""
        if self.jujustatus == "started":
            return Color.Fg.Green + self.jujustatus + Color.Reset
        elif self.jujustatus in ("error", "down"):
            return Color.Fg.Red + self.jujustatus + Color.Reset
        elif self.jujustatus == "pending":
            return Color.Fg.Orange + self.jujustatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.jujustatus + Color.Reset

    def get_machinestatus_color(self):
        """
        Return a status string with correct colors based on machine status
        """
        if self.machinestatus == "running":
            return Color.Fg.Green + self.machinestatus + Color.Reset
        elif self.machinestatus == "pending":
            return Color.Fg.Orange + self.machinestatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.machinestatus + Color.Reset

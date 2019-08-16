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

from basicmachine import BasicMachine
from container import Container


class Machine(BasicMachine):
    iscontainer = False

    def __init__(self, machinename, machineinfo, model):
        """
        Create a Machine object with basic information from a machine object
        from a juju status output
        """
        # Setup the BasicMachine
        BasicMachine.__init__(self, machinename, machineinfo, model)

        # Default Values
        self.containers = {}
        self.constraints = ""
        self.hardware = {}
        self.hardware["arch"] = ""
        self.hardware["cores"] = ""
        self.hardware["mem"] = ""
        self.hardware["root-disk"] = ""
        self.hardware["availability-zone"] = ""

        # Required Variables
        self.model = model

        # Optional Variables
        if "constraints" in machineinfo:
            self.constraints = machineinfo["constraints"]

        # Calculated Values
        if "hardware" in machineinfo:
            for hardwarepair in machineinfo["hardware"].split(" "):
                key, value = hardwarepair.split("=")
                self.hardware[key] = value

        # Handle Containers if any
        if "containers" in machineinfo:
            for containername, containerinfo in machineinfo[
                "containers"
            ].items():
                container = Container(
                    containername, containerinfo, self, model
                )
                model.add_container(container)
                self.containers[container.name] = container

    # TODO: Shouldn't handle color logic at this level
    def get_row(
        self, color, include_controller_name=False, include_model_name=False
    ):
        row = []
        """Return a list which can be used for a row in a table."""
        notesstr = ", ".join(self.notes)

        if color:
            row = [
                self.name,
                self.get_jujustatus_color(),
                self.get_machinestatus_color(),
                self.dnsname,
                self.instanceid,
                self.series,
                self.hardware["availability-zone"],
                self.hardware["arch"],
                self.hardware["cores"],
                self.hardware["mem"],
                self.machinemessage,
                notesstr,
            ]
        else:
            row = [
                self.name,
                self.jujustatus,
                self.machinestatus,
                self.dnsname,
                self.instanceid,
                self.series,
                self.hardware["availability-zone"],
                self.hardware["arch"],
                self.hardware["cores"],
                self.hardware["mem"],
                self.machinemessage,
                notesstr,
            ]

        if include_model_name:
            row.insert(0, self.model.name)
        if include_controller_name:
            row.insert(0, self.model.controller.name)
        return row

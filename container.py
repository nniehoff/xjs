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
from colors import Color


class Container(BasicMachine):
    iscontainer = True

    def __init__(self, containername, containerinfo, machine, model):
        """
        Create a Container object with basic information from a container
        object from a juju status output
        """
        # Setup the BasicMachine
        BasicMachine.__init__(self, containername, containerinfo, model)

        # Required Variables
        self.machine = machine

    def get_machinemessage_color(self):
        """
        Return a message string with correct colors based on the machine status
        """
        if self.machinemessage == "Container started":
            return Color.Fg.Green + self.machinemessage + Color.Reset
        else:
            return Color.Fg.Yellow + self.machinemessage + Color.Reset

    def get_row(
        self, color, include_controller_name=False, include_model_name=False
    ):
        """Return a list which can be used for a row in a table."""
        row = []
        notesstr = ", ".join(self.notes)

        if color:
            row = [
                self.name,
                self.get_jujustatus_color(),
                self.get_machinestatus_color(),
                self.dnsname,
                self.instanceid,
                self.series,
                "",
                "",
                "",
                "",
                self.get_machinemessage_color(),
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
                "",
                "",
                "",
                "",
                self.machinemessage,
                notesstr,
            ]

        if include_model_name:
            row.insert(0, self.machine.model.name)
        if include_controller_name:
            row.insert(0, self.machine.model.controller.name)
        return row

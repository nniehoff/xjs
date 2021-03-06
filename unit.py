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
from basicunit import BasicUnit
from subordinateunit import SubordinateUnit


class Unit(BasicUnit):
    issubordinate = False

    def __init__(self, unitname, unitinfo, application):
        """
        Create a Unit object with basic information from a unit object from a
        juju status output
        """
        # Setup the BasicUnit
        BasicUnit.__init__(
            self, unitname, unitinfo, application.model.controller
        )

        # Required Variables
        self.application = application
        if "machine" in unitinfo:
            match = re.match(r"(\d+)\/(lx[cd]|kvm)\/(\d+)$", unitinfo["machine"])
            if match:
                self.machine = application.model.get_container(unitinfo["machine"])
            else:
                self.machine = application.model.get_machine(unitinfo["machine"])
        else:
            self.machine = None

        # Handle Subordinate Charms if any
        if "subordinates" in unitinfo:
            for subunitname, subunitinfo in unitinfo["subordinates"].items():
                self.subordinates[subunitname] = SubordinateUnit(
                    subunitname, subunitinfo, self
                )

    def get_row(
        self, color, include_controller_name=False, include_model_name=False
    ):
        """Return a list which can be used for a row in a table."""
        row = []
        notesstr = ", ".join(self.notes)
        namestr = self.name
        portsstr = ",".join(self.openports)
        if self.machine:
            machinename = self.machine.name
        else:
            machinename = "PENDING"

        if self.leader:
            namestr += "*"

        if color:
            row = [
                namestr,
                self.get_workloadstatus_color(),
                self.get_jujustatus_color(),
                machinename,
                self.publicaddress,
                portsstr,
                self.message,
                notesstr,
            ]
        else:
            row = [
                namestr,
                self.workloadstatus,
                self.jujustatus,
                machinename,
                self.publicaddress,
                portsstr,
                self.message,
                notesstr,
            ]

        if include_model_name:
            row.insert(0, self.application.model.name)
        if include_controller_name:
            row.insert(0, self.application.model.controller.name)
        return row

    def filter_dictionary(self, dictionary, key_filter):
        return {
            key: value
            for (key, value) in dictionary.items()
            if key_filter in key
        }

    def filter_subordinates(self, subunit_filter):
        self.subordinates = self.filter_dictionary(
            self.subordinates, subunit_filter
        )

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


class SubordinateUnit(BasicUnit):
    issubordinate = True

    def __init__(self, subunitname, subunitinfo, unit):
        """
        Create a SubordinateUnit object with basic information from a
        subordinate unit object from a juju status output
        """
        # Setup the BasicUnit
        BasicUnit.__init__(
            self, subunitname, subunitinfo, unit.application.model.controller
        )

        # Required Variables
        self.unit = unit
        self.upgradingfrom = subunitinfo["upgrading-from"]
        self.machine = unit.machine

    def create_application_relation(self):
        appname = re.sub(r"\/\d+$", "", self.name)
        self.application = self.unit.application.model.get_application(appname)
        if self.application is not None:
            self.application.add_subordinate(self)

    def get_row(
        self, color, include_controller_name=False, include_model_name=False
    ):
        """Return a list which can be used for a row in a table."""
        row = []
        notesstr = ", ".join(self.notes)
        namestr = "  " + self.name
        portsstr = ",".join(self.openports)

        if self.leader:
            namestr += "*"

        if color:
            row = [
                namestr,
                self.get_workloadstatus_color(),
                self.get_jujustatus_color(),
                "",
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
                "",
                self.publicaddress,
                portsstr,
                self.message,
                notesstr,
            ]

        if include_model_name:
            row.insert(0, self.unit.application.model.name)
        if include_controller_name:
            row.insert(0, self.unit.application.model.controller.name)
        return row

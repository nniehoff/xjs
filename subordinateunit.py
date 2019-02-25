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
        appname = re.sub(r"\/\d+$", "", subunitname)
        application = unit.application.model.get_application(appname)
        if application is not None:
            application.add_subordinate(self)

    def get_row(self, color):
        """Return a list which can be used for a row in a table."""
        notesstr = ", ".join(self.notes)
        namestr = "  " + self.name
        portsstr = ",".join(self.openports)

        if self.leader:
            namestr += "*"

        if color:
            return [
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
            return [
                namestr,
                self.workloadstatus,
                self.jujustatus,
                "",
                self.publicaddress,
                portsstr,
                self.message,
                notesstr,
            ]

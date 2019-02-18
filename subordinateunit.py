#!/usr/bin/env python3

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

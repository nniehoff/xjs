#!/usr/bin/env python3

from basicunit import BasicUnit


class SubordinateUnit(BasicUnit):
    def __init__(self, subunitname, subunitinfo, unit):
        # Setup the BasicUnit
        BasicUnit.__init__(
            self, subunitname, subunitinfo, unit.application.model.controller
        )

        # Required Variables
        self.unit = unit
        self.upgradingfrom = subunitinfo["upgrading-from"]

    def get_row(self, color):
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

#!/usr/bin/env python3

import re
from basicunit import BasicUnit
from subordinateunit import SubordinateUnit


class Unit(BasicUnit):
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
        if re.match(r"\d+\/lxd\/(\d+)$", unitinfo["machine"]):
            self.machine = application.model.get_container(unitinfo["machine"])
        else:
            self.machine = application.model.get_machine(unitinfo["machine"])

        # Handle Subordinate Charms if any
        if "subordinates" in unitinfo:
            for subunitname, subunitinfo in unitinfo["subordinates"].items():
                self.subordinates.append(
                    SubordinateUnit(subunitname, subunitinfo, self)
                )

    def get_row(self, color):
        """Return a list which can be used for a row in a table."""
        notesstr = ", ".join(self.notes)
        namestr = self.name
        portsstr = ",".join(self.openports)

        if self.leader:
            namestr += "*"

        if color:
            return [
                namestr,
                self.get_workloadstatus_color(),
                self.get_jujustatus_color(),
                self.machine.name,
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
                self.machine.name,
                self.publicaddress,
                portsstr,
                self.message,
                notesstr,
            ]

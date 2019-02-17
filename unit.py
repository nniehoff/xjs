#!/usr/bin/env python3

import re
from datetime import datetime
from colors import Color


class SubordinateUnit:
    column_names = [
        "Unit",
        "Workload",
        "Agent",
        "Machine",
        "Public address",
        "Ports",
        "Message",
        "Notes",
    ]

    def __init__(self, subunitname, subunitinfo, unit):
        # Default Values
        self.notes = []
        self.openports = []
        self.message = ""
        self.leader = False

        # Required Variables
        self.name = subunitname
        self.unit = unit
        self.workloadstatus = subunitinfo["workload-status"]["current"]
        self.jujustatus = subunitinfo["juju-status"]["current"]
        self.jujuversion = subunitinfo["juju-status"]["version"]
        self.upgradingfrom = subunitinfo["upgrading-from"]
        self.publicaddress = subunitinfo["public-address"]

        # Required Dates
        self.workloadsince = datetime.strptime(
            subunitinfo["workload-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        unit.application.model.controller.update_timestamp(self.workloadsince)
        self.jujusince = datetime.strptime(
            subunitinfo["juju-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        unit.application.model.controller.update_timestamp(self.jujusince)

        # Optional Variables
        if "message" in subunitinfo["workload-status"]:
            self.message = subunitinfo["workload-status"]["message"]
        if "open-ports" in subunitinfo:
            self.openports = subunitinfo["open-ports"]
        if "leader" in subunitinfo:
            self.leader = subunitinfo["leader"]

    def get_workloadstatus_color(self):
        if self.workloadstatus == "active":
            return Color.Fg.Green + self.workloadstatus + Color.Reset
        if self.workloadstatus in ("error", "blocked"):
            return Color.Fg.Red + self.workloadstatus + Color.Reset
        if self.workloadstatus == "waiting":
            return self.workloadstatus
        if self.workloadstatus == "maintenance":
            return Color.Fg.Orange + self.workloadstatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.workloadstatus + Color.Reset

    def get_jujustatus_color(self):
        if self.jujustatus in ("idle", "executing"):
            return Color.Fg.Green + self.jujustatus + Color.Reset
        if self.jujustatus == "error":
            return Color.Fg.Red + self.jujustatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.jujustatus + Color.Reset

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


class Unit:
    column_names = [
        "Unit",
        "Workload",
        "Agent",
        "Machine",
        "Public address",
        "Ports",
        "Message",
        "Notes",
    ]

    def __init__(self, unitname, unitinfo, application):
        # Default Values
        self.notes = []
        self.openports = []
        self.subordinates = []
        self.message = ""
        self.leader = False

        # Required Variables
        self.name = unitname
        self.application = application
        self.workloadstatus = unitinfo["workload-status"]["current"]
        if re.match(r"\d+\/lxd\/(\d+)$", unitinfo["machine"]):
            self.machine = application.model.get_container(unitinfo["machine"])
        else:
            self.machine = application.model.get_machine(unitinfo["machine"])
        self.jujustatus = unitinfo["juju-status"]["current"]
        self.jujuversion = unitinfo["juju-status"]["version"]
        self.publicaddress = unitinfo["public-address"]

        # Required Dates
        self.workloadsince = datetime.strptime(
            unitinfo["workload-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        application.model.controller.update_timestamp(self.workloadsince)
        self.jujusince = datetime.strptime(
            unitinfo["juju-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        application.model.controller.update_timestamp(self.jujusince)

        # Optional Variables
        if "message" in unitinfo["workload-status"]:
            self.message = unitinfo["workload-status"]["message"]
        if "open-ports" in unitinfo:
            self.openports = unitinfo["open-ports"]
        if "leader" in unitinfo:
            self.leader = unitinfo["leader"]

        # Handle Subordinate Charms if any
        if "subordinates" in unitinfo:
            for subunitname, subunitinfo in unitinfo["subordinates"].items():
                self.subordinates.append(
                    SubordinateUnit(subunitname, subunitinfo, self)
                )

    def get_workloadstatus_color(self):
        if self.workloadstatus == "active":
            return Color.Fg.Green + self.workloadstatus + Color.Reset
        if self.workloadstatus in ("error", "blocked"):
            return Color.Fg.Red + self.workloadstatus + Color.Reset
        if self.workloadstatus == "waiting":
            return self.workloadstatus
        if self.workloadstatus == "maintenance":
            return Color.Fg.Orange + self.workloadstatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.workloadstatus + Color.Reset

    def get_jujustatus_color(self):
        if self.jujustatus in ("idle", "executing"):
            return Color.Fg.Green + self.jujustatus + Color.Reset
        if self.jujustatus == "error":
            return Color.Fg.Red + self.jujustatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.jujustatus + Color.Reset

    def get_row(self, color):
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

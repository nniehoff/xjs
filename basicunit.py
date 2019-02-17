#!/usr/bin/env python3

from datetime import datetime
from colors import Color


class BasicUnit:
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

    def __init__(self, name, info, controller):
        # Default Values
        self.notes = []
        self.openports = []
        self.subordinates = []
        self.message = ""
        self.leader = False

        # Required Variables
        self.name = name
        self.workloadstatus = info["workload-status"]["current"]
        self.jujustatus = info["juju-status"]["current"]
        self.jujuversion = info["juju-status"]["version"]
        self.publicaddress = info["public-address"]

        # Required Dates
        self.workloadsince = datetime.strptime(
            info["workload-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        controller.update_timestamp(self.workloadsince)
        self.jujusince = datetime.strptime(
            info["juju-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        controller.update_timestamp(self.jujusince)

        # Optional Variables
        if "message" in info["workload-status"]:
            self.message = info["workload-status"]["message"]
        if "open-ports" in info:
            self.openports = info["open-ports"]
        if "leader" in info:
            self.leader = info["leader"]

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

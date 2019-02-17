#!/usr/bin/env python3

from datetime import datetime
from colors import Color
from networkinterface import NetworkInterface


class BasicMachine:
    column_names = [
        "Machine",
        "Agent",
        "Status",
        "DNS",
        "Inst id",
        "Series",
        "AZ",
        "Arch",
        "Cores",
        "Memory",
        "Message",
        "Notes",
    ]

    def __init__(self, name, info, controller):
        # Default Values
        self.notes = []
        self.networkinterfaces = []

        # Required Variables
        self.name = name
        self.jujustatus = info["juju-status"]["current"]
        self.jujuversion = info["juju-status"]["version"]
        self.dnsname = info["dns-name"]
        self.ipaddresses = info["ip-addresses"]
        self.instanceid = info["instance-id"]
        self.machinestatus = info["machine-status"]["current"]
        self.machinemessage = info["machine-status"]["message"]
        self.series = info["series"]

        # Required Dates
        self.jujusince = datetime.strptime(
            info["juju-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        controller.update_timestamp(self.jujusince)
        self.machinesince = datetime.strptime(
            info["machine-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        controller.update_timestamp(self.machinesince)

        # Handle Network Interfaces
        for interfacename, interfaceinfo in info["network-interfaces"].items():
            self.networkinterfaces.append(
                NetworkInterface(interfacename, interfaceinfo, self)
            )

    def get_jujustatus_color(self):
        if self.jujustatus == "started":
            return Color.Fg.Green + self.jujustatus + Color.Reset
        if self.jujustatus in ("error", "down"):
            return Color.Fg.Red + self.jujustatus + Color.Reset
        if self.jujustatus == "pending":
            return Color.Fg.Orange + self.jujustatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.jujustatus + Color.Reset

    def get_machinestatus_color(self):
        if self.machinestatus == "running":
            return Color.Fg.Green + self.machinestatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.machinestatus + Color.Reset

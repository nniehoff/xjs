#!/usr/bin/env python3

from datetime import datetime
from colors import Color


class NetworkInterface:
    column_names = [
        "Machine",
        "Interface",
        "IP",
        "MAC",
        "Gateway",
        "Space",
        "Up",
        "Notes",
    ]

    def __init__(self, interfacename, interfaceinfo, parent):
        # Default Values
        self.space = ""
        self.notes = []
        self.gateway = ""

        # Required Variables
        self.name = interfacename
        self.parent = parent
        self.ipaddresses = interfaceinfo["ip-addresses"]
        self.macaddress = interfaceinfo["mac-address"]
        self.up = interfaceinfo["is-up"]

        # Optional Variables
        if "space" in interfaceinfo:
            self.space = interfaceinfo["space"]
        if "gateway" in interfaceinfo:
            self.gateway = interfaceinfo["gateway"]

    def get_isup_color(self):
        if self.up:
            return Color.Fg.Green + str(self.up) + Color.Reset
        else:
            return Color.Fg.Red + str(self.up) + Color.Reset

    def get_row(self, color):
        notesstr = ", ".join(self.notes)
        ipstr = ",".join(self.ipaddresses)
        if color:
            return [
                self.parent.name,
                self.name,
                ipstr,
                self.macaddress,
                self.gateway,
                self.space,
                self.get_isup_color(),
                notesstr,
            ]
        else:
            return [
                self.parent.name,
                self.name,
                ipstr,
                self.macaddress,
                self.gateway,
                self.space,
                str(self.up),
                notesstr,
            ]


class Container:
    iscontainer = True
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

    def __init__(self, containername, containerinfo, machine):
        # Default Values
        self.notes = []
        self.networkinterfaces = []

        # Required Variables
        self.name = containername
        self.machine = machine
        self.jujustatus = containerinfo["juju-status"]["current"]
        self.jujuversion = containerinfo["juju-status"]["version"]
        self.dnsname = containerinfo["dns-name"]
        self.ipaddresses = containerinfo["ip-addresses"]
        self.instanceid = containerinfo["instance-id"]
        self.machinestatus = containerinfo["machine-status"]["current"]
        self.machinemessage = containerinfo["machine-status"]["message"]
        self.series = containerinfo["series"]

        # Required Dates
        self.jujusince = datetime.strptime(
            containerinfo["juju-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        machine.model.controller.update_timestamp(self.jujusince)
        self.machinesince = datetime.strptime(
            containerinfo["machine-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        machine.model.controller.update_timestamp(self.machinesince)

        # Handle Network Interfaces
        for interfacename, interfaceinfo in containerinfo[
            "network-interfaces"
        ].items():
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

    def get_machinemessage_color(self):
        if self.machinemessage == "Container started":
            return Color.Fg.Green + self.machinemessage + Color.Reset
        else:
            return Color.Fg.Yellow + self.machinemessage + Color.Reset

    def get_row(self, color):
        notesstr = ", ".join(self.notes)

        if color:
            return [
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
            return [
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


class Machine:
    iscontainer = False
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

    def __init__(self, machinename, machineinfo, model):
        # Default Values
        self.notes = []
        # Todo Add Units to Machines
        self.units = []
        self.containers = []
        self.networkinterfaces = []
        self.constraints = ""
        self.hardware = {}
        self.hardware["arch"] = ""
        self.hardware["cores"] = ""
        self.hardware["mem"] = ""
        self.hardware["root-disk"] = ""
        self.hardware["availability-zone"] = ""

        # Required Variables
        self.name = machinename
        self.model = model
        self.jujustatus = machineinfo["juju-status"]["current"]
        self.jujuversion = machineinfo["juju-status"]["version"]
        self.dnsname = machineinfo["dns-name"]
        self.ipaddresses = machineinfo["ip-addresses"]
        self.instanceid = machineinfo["instance-id"]
        self.machinestatus = machineinfo["machine-status"]["current"]
        self.machinemessage = machineinfo["machine-status"]["message"]
        self.series = machineinfo["series"]

        # Required Dates
        self.jujusince = datetime.strptime(
            machineinfo["juju-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        model.controller.update_timestamp(self.jujusince)
        self.machinesince = datetime.strptime(
            machineinfo["machine-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        model.controller.update_timestamp(self.machinesince)

        # Optional Variables
        if "constraints" in machineinfo:
            self.constraints = machineinfo["constraints"]

        # Calculated Values
        for hardwarepair in machineinfo["hardware"].split(" "):
            key, value = hardwarepair.split("=")
            self.hardware[key] = value

        # Handle Containers if any
        if "containers" in machineinfo:
            for containername, containerinfo in machineinfo[
                "containers"
            ].items():
                container = Container(containername, containerinfo, self)
                model.add_container(container)
                self.containers.append(container)

        # Handle Network Interfaces
        for interfacename, interfaceinfo in machineinfo[
            "network-interfaces"
        ].items():
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

    def get_row(self, color):
        notesstr = ", ".join(self.notes)

        if color:
            return [
                self.name,
                self.get_jujustatus_color(),
                self.get_machinestatus_color(),
                self.dnsname,
                self.instanceid,
                self.series,
                self.hardware["availability-zone"],
                self.hardware["arch"],
                self.hardware["cores"],
                self.hardware["mem"],
                self.machinemessage,
                notesstr,
            ]
        else:
            return [
                self.name,
                self.jujustatus,
                self.machinestatus,
                self.dnsname,
                self.instanceid,
                self.series,
                self.hardware["availability-zone"],
                self.hardware["arch"],
                self.hardware["cores"],
                self.hardware["mem"],
                self.machinemessage,
                notesstr,
            ]

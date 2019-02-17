#!/usr/bin/env python3

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

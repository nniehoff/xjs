#!/usr/bin/env python3

from datetime import datetime


class Application:
    def __init__(self, appname, appinfo, model):
        self.notes = []
        self.units = []
        self.version = ""
        self.message = ""
        self.relations = {}
        self.endpointbindings = {}
        self.charmlatestrev = -1

        self.name = appname
        self.charm = appinfo["charm"]
        self.series = appinfo["series"]
        self.os = appinfo["os"]
        # TODO Figure out how to compare app versions and get latest from the
        # charm store
        if "version" in appinfo:
            self.version = appinfo["version"]
        self.charmorigin = appinfo["charm-origin"]
        self.charmname = appinfo["charm-name"]
        self.charmrev = int(appinfo["charm-rev"])
        self.exposed = appinfo["exposed"]
        self.status = appinfo["application-status"]["current"]
        if "message" in appinfo["application-status"]:
            self.message = appinfo["application-status"]["message"]
        self.since = datetime.strptime(
            appinfo["application-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        if "relations" in appinfo:
            self.relations = appinfo["relations"]
        if "endpoint-bindings" in appinfo:
            self.endpointbindings = appinfo["endpoint-bindings"]
        if "can-upgrade-to" in appinfo:
            self.charmlatestrev = appinfo["can-upgrade-to"]
        self.model = model

        if self.exposed:
            self.notes.append("exposed")

    def get_scale(self):
        return len(self.units)

    def add_unit(self, unit):
        self.units.append(unit)

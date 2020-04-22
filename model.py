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
from colors import Color
from packaging import version
import pendulum


class Model:
    # TODO get latest juju version dynamically
    latest_juju_version = version.parse("2.6.8")
    column_names = [
        "Model",
        "Controller",
        "Cloud/Region",
        "Version",
        "SLA",
        "Timestamp",
        "Model-Status",
        "Meter-Status",
        "Message",
        "Notes",
    ]

    def __init__(self, modelinfo, controller, juju1env=None):
        """
        Create a Model object with basic information from a model object
        from a juju status output
        """
        # Default Values
        self.notes = []
        self.applications = {}
        self.relations = {}
        self.machines = {}
        self.containers = {}
        self.meterstatus = ""
        self.message = ""
        self.upgradeavailable = ""

        # Required Variables
        if "name" in modelinfo:
            self.name = modelinfo["name"]
        else:
            self.name = "NA"

        if "type" in modelinfo:
            self.type = modelinfo["type"]
        else:
            self.type = "NA"
        self.controller = controller

        if "controller" in modelinfo:
            self.controller.name = modelinfo["controller"]

        if "cloud" in modelinfo:
            self.cloud = modelinfo["cloud"]
        elif juju1env:
            self.cloud = juju1env
        else:
            self.cloud = "NA"

        if "version" in modelinfo:
            self.version = modelinfo["version"]
        else:
            self.version = "1.x.x"

        if "model-status" in modelinfo:
            self.modelstatus = modelinfo["model-status"]["current"]
        else:
            self.modelstatus = "NA"

        if "sla" in modelinfo:
            self.sla = modelinfo["sla"]
        else:
            self.sla = "NA"

        # Required Dates
        if "model-status" in modelinfo and "since" in modelinfo["model-status"]:
            if re.match(r".*Z$", modelinfo["model-status"]["since"]):
                modelinfo["model-status"]["since"] = re.sub(r"Z$", "", modelinfo["model-status"]["since"])
                self.since = pendulum.from_format(
                    modelinfo["model-status"]["since"],
                    "DD MMM YYYY HH:mm:ss",
                    tz="UTC",
                )
            else:
                self.since = pendulum.from_format(
                    modelinfo["model-status"]["since"], "DD MMM YYYY HH:mm:ssZ"
                )
            controller.update_timestamp(self.since)

        # Optional Variables
        if "meter-status" in modelinfo:
            self.meterstatus = modelinfo["meter-status"]["color"]
            self.message = modelinfo["meter-status"]["message"]
        if "upgrade-available" in modelinfo:
            self.upgradeavailable = modelinfo["upgrade-available"]
            self.notes.append("upgrade available: " + self.upgradeavailable)

    def __dict__(self):
        return {self.name: self}

    def add_application(self, application):
        """Add an Application to this model"""
        self.applications[application.name] = application

    def add_machine(self, machine):
        """Add a machine to this model"""
        self.machines[machine.name] = machine

    def add_container(self, container):
        """Add a container to this model"""
        self.containers[container.name] = container

    def add_relation(self, relation):
        if relation is not None:
            """Add a relation if it doesn't already exist"""
            if not relation.name in self.relations:
                self.relations[relation.name] = []
                self.relations[relation.name].append(relation)
                return
            else:
                if not self.get_relation(relation.name, relation.application.name, 
                    relation.partner.name):
                    self.relations[relation.name].append(relation)

    def get_relation(self, name, app_name, partner_name):
        if name in self.relations:
            for relation in self.relations[name]:
                if ((relation.application.name == app_name
                        and relation.partner.name == partner_name) or
                        (relation.partner.name == app_name and 
                        relation.application.name == partner_name)):
                    return relation
            return None
        else:
            return None

    def get_application(self, searchappname):
        """Get an Application by name"""
        for appname, application in self.applications.items():
            if appname == searchappname:
                return application
        return None

    def get_machine(self, machinename):
        """Get a machine by name"""
        if machinename in self.machines:
            return self.machines[machinename]
        else:
            return None

    def get_container(self, containername):
        """Get a container by name"""
        if containername in self.containers:
            return self.containers[containername]
        else:
            return None

    def get_version_color(self):
        """Return a version string with correct colors based on version"""
        model_version = version.parse(self.version)
        if (
            model_version < version.parse("2.0.0")
            or model_version > Model.latest_juju_version
        ):
            return Color.Fg.Red + self.version + Color.Reset
        elif model_version < Model.latest_juju_version:
            return Color.Fg.Yellow + self.version + Color.Reset
        else:
            return Color.Fg.Green + self.version + Color.Reset

    # TODO Figure out all possible values of all options and color accordingly
    def get_modelstatus_color(self):
        """Return a status string with correct colors based on status"""
        if self.modelstatus == "available":
            return Color.Fg.Green + self.modelstatus + Color.Reset
        else:
            return Color.Fg.Red + self.modelstatus + Color.Reset

    def get_meterstatus_color(self):
        """
        Return a meter status string with correct colors based on meter
        status
        """
        if not self.meterstatus:
            return ""
        if self.meterstatus == "green":
            return Color.Fg.Green + self.meterstatus + Color.Reset
        elif self.meterstatus == "red":
            return Color.Fg.Red + self.meterstatus + Color.Reset
        elif self.meterstatus == "amber":
            return Color.Fg.Orange + self.meterstatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.meterstatus + Color.Reset

    def get_row(
        self, color, include_controller_name=True, include_model_name=True
    ):
        """Return a list which can be used for a row in a table."""
        if not self.controller.timestampprovided:
            if color:
                self.notes.append(
                    Color.Fg.Yellow + "Guessing at timestamp" + Color.Reset
                )
            else:
                self.notes.append("Guessing at timestamp")
        notesstr = ", ".join(self.notes)
        timestampstr = self.controller.timestamp.strftime("%H:%M:%SZ")
        if color:
            return [
                self.name,
                self.controller.name,
                self.cloud,
                self.get_version_color(),
                self.sla,
                timestampstr,
                self.get_modelstatus_color(),
                self.get_meterstatus_color(),
                self.message,
                notesstr,
            ]
        else:
            return [
                self.name,
                self.controller.name,
                self.cloud,
                self.version,
                self.sla,
                timestampstr,
                self.modelstatus,
                self.meterstatus,
                self.message,
                notesstr,
            ]

    def get_column_names(
        self, include_controller_name=True, include_model_name=True
    ):
        """Append the controller name and/or model name as necessary"""
        return self.column_names

    def filter_dictionary(self, dictionary, key_filter):
        return {
            key: value
            for (key, value) in dictionary.items()
            if key_filter in key
        }

    def filter_applications(self, app_filter):
        apps = self.filter_dictionary(self.applications, app_filter)
        parent_apps = {}
        for appname, appinfo in apps.items():
            for subname, subinfo in appinfo.subordinates.items():
                parent_apps[
                    subinfo.unit.application.name
                ] = subinfo.unit.application
        self.applications = {**apps, **parent_apps}
        self.reset_machines()

    def reset_machines(self):
        machines = {}
        containers = {}
        for appname, appinfo in self.applications.items():
            for unitname, unitinfo in appinfo.units.items():
                if unitinfo.machine.iscontainer:
                    containers[unitinfo.machine.name] = unitinfo.machine
                    machines[
                        unitinfo.machine.machine.name
                    ] = unitinfo.machine.machine
                else:
                    machines[unitinfo.machine.name] = unitinfo.machine
            for subunitname, subunitinfo in appinfo.subordinates.items():
                if subunitinfo.machine.iscontainer:
                    containers[subunitinfo.machine.name] = subunitinfo.machine
                    machines[
                        subunitinfo.machine.machine.name
                    ] = subunitinfo.machine.machine
                else:
                    machines[subunitinfo.machine.name] = subunitinfo.machine
        for machinename, machine in machines.items():
            oldcontainers = machine.containers.keys() - containers.keys()
            for containername in oldcontainers:
                del machine.containers[containername]
        self.machines = machines
        self.containers = containers

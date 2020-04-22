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


from application import Application

class Relation:
    """
    A Relation is a juju relation between 2 juju applications, juju status
    does not provide much information.
    """

    column_names = [
        "Application A",
        "Application B"
    ]

    def __init__(self, model, name, partnername, applicationname):
        """
        Create a Relation object from a juju status output
        """
        # Default Values
        self.name = name
        self.application = model.get_application(applicationname)
        if model.get_application(partnername):
            self.partner = model.get_application(partnername)
        else:
            self.partner = Application(partnername)
        # self.partner = self.application.model.get_application(partner)
        # if not self.partner:
        #     self.partner = partner

    def __dict__(self):
        return {self.name: self}

    def get_row(
        self, color, include_controller_name=False, include_model_name=False
    ):
        """Return a list which can be used for a row in a table."""

        row = []
        if color:
            row = [
                self.application.name + ':' + self.name,
                self.partner.name + ':' + self.name,
            ]
        else:
            row = [
                self.application.name + ':' + self.name,
                self.partner.name + ':' + self.name,
            ]
        if include_model_name:
            row.insert(0, self.application.model.name)
        if include_controller_name:
            row.insert(0, self.application.model.controller.name)
        return row

    def get_column_names(
        self, include_controller_name=False, include_model_name=False
    ):
        """Append the controller name and/or model name as necessary"""
        if include_model_name:
            self.column_names.insert(0, "Model")
        if include_controller_name:
            self.column_names.insert(0, "Controller")
        return self.column_names

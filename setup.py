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

import setuptools

# requirements = [
#     'PyYAML>=3.13',
#     'prettytable>=0.7.2',
#     'click>=7.0',
#     'packaging>=19.0',
#     'requests>=2.21.0',
#     'pendulum>=2.0.4'
# ]

setuptools.setup(
    name="xjs",
    version="0.1",
    scripts=[
        "xjs",
    ],
)

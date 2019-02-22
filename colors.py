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


# TODO color logic needs to be adjusted, this should handle colors for more
# than just the console
class Color:
    """
    An object with console colors
    """

    Reset = "\033[0m"
    Bold = "\033[01m"
    Disable = "\033[02m"
    Underline = "\033[04m"
    Reverse = "\033[07m"
    Strikethrough = "\033[09m"
    Invisible = "\033[08m"

    class Fg:
        Black = "\033[30m"
        Red = "\033[31m"
        Green = "\033[32m"
        Orange = "\033[33m"
        Blue = "\033[34m"
        Purple = "\033[35m"
        Cyan = "\033[36m"
        LightGrey = "\033[37m"
        DarkGrey = "\033[90m"
        LightRed = "\033[91m"
        LightGreen = "\033[92m"
        Yellow = "\033[93m"
        LightBlue = "\033[94m"
        Pink = "\033[95m"
        LightCyan = "\033[96m"

    class Bg:
        Black = "\033[40m"
        Red = "\033[41m"
        Green = "\033[42m"
        Orange = "\033[43m"
        Blue = "\033[44m"
        Purple = "\033[45m"
        Cyan = "\033[46m"
        LightGrey = "\033[47m"

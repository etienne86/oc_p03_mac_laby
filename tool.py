#! /usr/bin/env python3
# coding: utf-8

"""This module contains the 'Tool' class."""


class Tool:
    """This class is used to represent a tool (e.g. tube, ether, needle)."""

    TOOLS_NAMES = ["ether", "needle", "tube"]

    def __init__(self, name, x_pos, y_pos):
        """This special method is the class constructor."""
        self.found = False
        self.name = name  # type is str
        self.x_pos = x_pos  # type is int
        self.y_pos = y_pos  # type is int

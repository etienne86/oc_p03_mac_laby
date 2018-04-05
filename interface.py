#! /usr/bin/env python3
# coding: utf-8

"""This module contains the 'Interface' class.
This includes both edit mode interface and game mode interface possibilities.
This module uses pygame as main support.
"""

import pygame
from pygame.locals import *

from labyrinth import Labyrinth

class Interface:
    """This class allows to create and modify an interface."""

    def __init__(self, width, height, back, title):
        """This special method is the class constructor."""
        self.size = (width, height) # this is a tuple (int, int)
        self.back = back
        self.title = title # type is str
        self.sub_elements = {"pictures": []}
        self.logic_light = "green" # possible values: "red", "yellow", "green"

    def position_labyrinth(self, x, y, labyrinth):
        """This method positions the labyrinth on the interface."""
        self.sub_elements["laby"] = (x, y, labyrinth)

    def position_sprite(self, x, y, picture):
        """This method positions a picture on the interface."""
        self.sub_elements["pictures"].append((x, y, picture))

    def position_title(self, x, y):
        """This method positions the title on the interface."""
        self.sub_elements["title"] = (x, y, self.title)
#! /usr/bin/env python3
# coding: utf-8

"""This module contains the 'Interface' class.
This includes both edit mode interface and game mode interface possibilities.
This module uses pygame as main support.
"""

import pygame
from pygame.locals import *


class Interface:
    """This class allows to create and modify an interface."""

    SPRITE_SIZE = 30  # this is the square sprite width/height in pixels
    SCREEN_WIDTH = 800  # number of pixels
    SCREEN_HEIGHT = 550  # number of pixels
    SCREEN_ORIGIN = (0, 0)
    LABY_ORIGIN = (50, 50)
    DASHBOARD_ORIGIN = (550, 50)

    def __init__(self, back, laby_viewer, dashboard):
        """This special method is the class constructor."""
        self.back = back  # type is pygame.Surface
        self.screen = self.initialize_interface()  # type is pygame.Surface
        self.laby_viewer = laby_viewer  # type is <class 'LabyViewer'>
        self.dashboard = dashboard  # type is <class 'Dashboard'>

    def display_dashboard(self, screen, tools=[]):
        """This method displays the dashboard."""
        self.dashboard.display(screen, tools)

    def display_labyrinth_with_tools(self, screen, sprites_dict):
        """This method displays the labyrinth with the tools.
        We assume that pygame has been initialized."""
        self.laby_viewer.display_labyrinth(screen, sprites_dict)
        self.laby_viewer.display_tools_in_labyrinth(screen)

    @classmethod
    def initialize_interface(cls):
        """This method initialize the interface."""
        screen = pygame.display.set_mode((cls.SCREEN_WIDTH, cls.SCREEN_HEIGHT))
        return screen

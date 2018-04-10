#! /usr/bin/env python3
# coding: utf-8

"""This module contains the 'Interface' class.
This includes both edit mode interface and game mode interface possibilities.
This module uses pygame as main support.
"""

import os

import pygame
from pygame.locals import *

from labyrinth import Labyrinth

class Interface:
    """This class allows to create and modify an interface."""

    # LABY_SIZE = 15 # this is the square labyrinth side size
    #                # (number of sprites per side)
    SPRITE_SIZE = 30 # this is the square sprite width/height in pixels
    SCREEN_WIDTH = 800 # number of pixels
    SCREEN_HEIGHT = 550 # number of pixels
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    SCREEN_ORIGIN = (0,0)
    LABY_ORIGIN = (50,50)
    DASHBOARD_ORIGIN = (550,50)


    def __init__(self, back, laby_viewer, dashboard):
        """This special method is the class constructor."""
        self.back = back # type is pygame.Surface
        self.screen = self.initialize_interface()
        self.laby_viewer = laby_viewer # type is <class 'LabyViewer'>
        self.dashboard = dashboard # type is <class 'Dashboard'>
        self.bottom = "Press 'Esc' to quit"

    @classmethod
    def display_dashboard(cls):
        """This method displays the dashboard."""
        pass

    @classmethod
    def display_labyrinth(cls, labyrinth, screen, sprites):
        """This method displays the labyrinth.
        We assume that pygame has been initialized."""
        x0 = cls.LABY_ORIGIN[0]
        y0 = cls.LABY_ORIGIN[1]
        for j in range(cls.LABY_SIZE): # iteration over columns
            for i in range(cls.LABY_SIZE): # iteration over rows
                x = x0 + (j * cls.SPRITE_SIZE)
                y = y0 + (i * cls.SPRITE_SIZE)
                item = labyrinth.grid.iloc[i,j]
                if item == 0:
                    sprite = sprites["sand_path"]
                elif item == 1:
                    sprite = sprites["wall"]
                elif item == 2:
                    sprite = sprites["sand_path"]
                    screen.blit(sprite, (x,y))
                    sprite = sprites["guard"]
                elif item == 3:
                    sprite = sprites["sand_path"]
                    screen.blit(sprite, (x,y))
                    sprite = sprites["mac_gyver"]
                screen.blit(sprite, (x,y))
        pygame.display.flip()

    @classmethod
    def display_title(cls, title):
        """This method displays the title."""
        pass

    @classmethod
    def display_tools_in_labyrinth(cls, tools, screen):
        """This method displays the tools in the labyrinth.
        We assume that the labyrinth is already displayed.
        We assume that pygame has been initialized."""
        x0 = cls.LABY_ORIGIN[0]
        y0 = cls.LABY_ORIGIN[1]
        for tool in tools:
            x_tool = x0 + tool.x_pos * cls.SPRITE_SIZE
            y_tool = y0 + tool.y_pos * cls.SPRITE_SIZE
            sprite_png = tool.name + ".png"
            sprite_path = os.path.join("sprites", sprite_png)
            sprite = pygame.image.load(sprite_path).convert()
            sprite.set_colorkey((255,255,255)) # set white as transparent
            screen.blit(sprite, (x_tool, y_tool))
        pygame.display.flip()

    @classmethod
    def initialize_interface(cls):
        """This method initialize the interface."""
        screen = pygame.display.set_mode((cls.SCREEN_SIZE))
        return screen

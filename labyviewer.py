#! /usr/bin/env python3
# coding: utf-8

"""This module contains the 'LabyViewer' class.
This allows to display a labyrinth.
This module uses pygame as main support.
"""

import os

import pygame
from pygame.locals import *

from labyrinth import Labyrinth

class LabyViewer:
    """This class allows to create and modify an labyrinth viewer."""

    LABY_SIZE = 15 # this is the square labyrinth side size
                   # (number of sprites per side)

    def __init__(self, origin, labyrinth, tools, sprite_size):
        """This special method is the class constructor."""
        self.labyrinth = labyrinth # type is <class 'Labyrinth'>
        # 'self.tools' type is list containing items of <class 'Tool'>
        self.tools = tools
        self.sprite_size = sprite_size # type is int
        self.origin = origin # type is tuple (int,int)

    def display_labyrinth(self, screen, sprites_dict):
        """This method displays the labyrinth.
        We assume that pygame has been initialized."""
        x0 = self.origin[0]
        y0 = self.origin[1]
        for j in range(self.LABY_SIZE): # iteration over columns
            for i in range(self.LABY_SIZE): # iteration over rows
                x = x0 + (j * self.sprite_size)
                y = y0 + (i * self.sprite_size)
                item = self.labyrinth.grid.iloc[i,j]
                if item == 0:
                    sprite = sprites_dict["sand_path"]
                elif item == 1:
                    sprite = sprites_dict["wall"]
                elif item == 2:
                    sprite = sprites_dict["sand_path"]
                    screen.blit(sprite, (x,y))
                    sprite = sprites_dict["guard"]
                elif item == 3:
                    sprite = sprites_dict["sand_path"]
                    screen.blit(sprite, (x,y))
                    sprite = sprites_dict["mac_gyver"]
                screen.blit(sprite, (x,y))
        pygame.display.flip()

    def display_tools_in_labyrinth(self, screen):
        """This method displays the tools in the labyrinth.
        We assume that the labyrinth is already displayed.
        We assume that pygame has been initialized."""
        x0 = self.origin[0]
        y0 = self.origin[1]
        for tool in self.tools:
            if not tool.found:
                x_tool = x0 + (tool.x_pos * self.sprite_size)
                y_tool = y0 + (tool.y_pos * self.sprite_size)
                sprite_png = tool.name + ".png"
                try:
                    sprite_path = os.path.join("sprites", sprite_png)
                    sprite = pygame.image.load(sprite_path).convert()
                    sprite.set_colorkey((255,255,255)) # set white as transparent
                    screen.blit(sprite, (x_tool, y_tool))
                except:
                    raise NameError("{}.png introuvable".format(tool.name))
        pygame.display.flip()

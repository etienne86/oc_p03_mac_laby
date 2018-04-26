#! /usr/bin/env python3
# coding: utf-8

"""This module contains the 'LabyViewer' class.
This allows to display a labyrinth.
This module uses pygame as main support.
"""

import os

import pygame
from pygame.locals import *

from interface import Interface


class LabyViewer:
    """This class allows to create and modify an labyrinth viewer."""

    LABY_WIDTH = 15  # this is the labyrinth width in sprites
    #                 (number of sprites per side)
    LABY_HEIGHT = 15  # this is the labyrinth height in sprites
    #                 (number of sprites per side)

    def __init__(self, labyrinth):
        """This special method is the class constructor."""
        self.labyrinth = labyrinth  # type is <class 'Labyrinth'>

    def display_labyrinth(self, screen, sprites_dict):
        """This method displays the labyrinth.
        We assume that pygame has been initialized."""
        x_0 = Interface.LABY_ORIGIN[0]
        y_0 = Interface.LABY_ORIGIN[1]
        for j in range(self.LABY_WIDTH):  # iteration over columns
            for i in range(self.LABY_HEIGHT):  # iteration over rows
                x_pos = x_0 + (j * Interface.SPRITE_SIZE)
                y_pos = y_0 + (i * Interface.SPRITE_SIZE)
                item = self.labyrinth.grid.iloc[i, j]
                if item == 0:
                    sprite = sprites_dict["sand_path"]
                elif item == 1:
                    sprite = sprites_dict["wall"]
                elif item == 2:
                    sprite = sprites_dict["sand_path"]
                    screen.blit(sprite, (x_pos, y_pos))
                    sprite = sprites_dict["guard"]
                elif item == 3:
                    sprite = sprites_dict["sand_path"]
                    screen.blit(sprite, (x_pos, y_pos))
                    sprite = sprites_dict["m_gyver"]
                elif str(item).isalpha():
                    pass
                else:
                    raise ValueError(item)
                if not str(item).isalpha():
                    screen.blit(sprite, (x_pos, y_pos))
        pygame.display.flip()

    def display_tools_in_labyrinth(self, screen):
        """This method displays the tools in the labyrinth.
        We assume that the labyrinth is already displayed.
        We assume that pygame has been initialized."""
        x_0 = Interface.LABY_ORIGIN[0]
        y_0 = Interface.LABY_ORIGIN[1]
        for tool in self.labyrinth.tools:
            if not tool.found:
                x_tool = x_0 + (tool.x_pos * Interface.SPRITE_SIZE)
                y_tool = y_0 + (tool.y_pos * Interface.SPRITE_SIZE)
                sprite_png = tool.name + ".png"
                try:
                    sprite_path = os.path.join("sprites", "tools", sprite_png)
                    sprite = pygame.image.load(sprite_path).convert()
                    # set white as transparent
                    sprite.set_colorkey((255, 255, 255))
                    screen.blit(sprite, (x_tool, y_tool))
                except pygame.error:
                    raise NameError("{}.png introuvable".format(tool.name))
        pygame.display.flip()

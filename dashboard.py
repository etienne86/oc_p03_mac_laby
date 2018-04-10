#! /usr/bin/env python3
# coding: utf-8

"""This module contains the 'Dashboard' class.
This allows to display a labyrinth.
This module uses pygame as main support.
"""

import os

import pygame
from pygame.locals import *

from labyrinth import Labyrinth

class Dashboard:
    """This class allows to create and modify a dashoard."""

    def __init__(self, origin, mode, sprite_size):
        """This special method is the class constructor."""
        self.origin = origin # type is tuple (int,int)
        self.mode = mode # type is str
        self.sprite_size = sprite_size # type is int
        self.logic_light = "yellow" # possible values: "red", "yellow", "green"

    def display_dashboard(self, screen, tools):
        """This method displays the dashboard.
        We assume that pygame has been initialized."""
        if self.mode == "game":
            self._display_game_dashboard(screen, tools)
        elif self.mode == "edit":
            self._display_edit_dashboard(screen)
        else:
            raise ValueError("This mode is not permitted!")

    def _display_game_dashboard(self, screen, tools):
        """This method displays the dashboard in game mode.
        We assume that pygame has been initialized."""
        x0 = self.origin[0]
        y0 = self.origin[1]
        side = self.sprite_size
        # Our fonts
        black = (0, 0, 0)
        font_arial_12_bold = pygame.font.SysFont('Arial', 12, bold=True)
        font_arial_10 = pygame.font.SysFont('Arial', 10)
        # 1. First section
        # 1.1. Title
        title1_str = 'Tools found until now:'
        title1 = font_arial_12_bold.render(title1_str, False, black)
        screen.blit(title1,(x0,y0))
        # 1.2. Items
        for i, tool in enumerate(tools):
            x_tool = x0
            y_tool = y0 + 2 * i * side
            # We draw an "empty" square
            self._display_transparent_square(screen, x_tool, y_tool)
            # We display the tool name
            x_tool_name = x_tool + side + 10
            y_tool_name = y_tool + 10
            tool_text = font_arial_10.render(tool.name, False, black)
            screen.blit(tool_text, (x_tool_name, y_tool_name))
            # We fill the square with the sprite if the tool is found
            if tool.found:
                sprite_png = tool.name + ".png"
                sprite_path = os.path.join("sprites", sprite_png)
                sprite = pygame.image.load(sprite_path).convert()
                screen.blit(sprite, (x_tool, y_tool))
        # 2. Second section
        # 2.1. Title
        title2 = font_arial_12_bold.render('Status:', False, black)
        screen.blit(title2,(x0, y0 + 8 * side))
        # 2.2. Logic light (red/yellow/green)
        x_light = x0
        y_red = y0 + 10 * side
        y_yellow = y0 + 12 * side
        y_green = y0 + 14 * side
        if self.logic_light == "red":
            y_light = y_red
            color = (255, 0, 0)
        elif self.logic_light == "yellow":
            y_light = y_yellow
            color = (255, 242, 0)
        elif self.logic_light == "green":
            y_light = y_green
            color = (0, 255, 0)
        else:
            raise ValueError(self.logic_light)
        pygame.draw.rect(screen, color, (x_light, y_light, side, side))
        self._display_transparent_square(screen, x_light, y_red)
        self._display_transparent_square(screen, x_light, y_yellow)
        self._display_transparent_square(screen, x_light, y_green)
        # 2.3. Logic light description
        red_msg = "You lose... your life, sorry!"
        yellow_msg = "You are still alive, good luck!"
        green_msg = "You win, congratulations!"
        red_text = font_arial_10.render(red_msg, False, black)
        yellow_text = font_arial_10.render(yellow_msg, False, black)
        green_text = font_arial_10.render(green_msg, False, black)
        screen.blit(red_text, (x_light + side + 10, y_red + 10))
        screen.blit(yellow_text, (x_light + side + 10, y_yellow + 10))
        screen.blit(green_text, (x_light + side + 10, y_green + 10))
        # screen refresh
        pygame.display.flip()

    def _display_edit_dashboard(self, screen):
        """This method displays the dashboard in edit mode.
        We assume that pygame has been initialized."""
        x0 = self.origin[0]
        y0 = self.origin[1]
        side = self.sprite_size
        # Our fonts
        black = (0, 0, 0)
        font_arial_12_bold = pygame.font.SysFont('Arial', 12, bold=True)
        font_arial_10 = pygame.font.SysFont('Arial', 10)
        # 1. First section
        # 1.1. Title
        title1_str = 'Left click to select, right click to release:'
        title1 = font_arial_12_bold.render(title1_str, False, black)
        screen.blit(title1, (x0, y0))
        # 1.2. Items
        for i in range(3):
            x_sprite = x0
            y_sprite = y0 + (2 * (i+1) * side)
            # We fill the square with the sprite if the tool is found
            if i == 0:
                sprite = pygame.image.load("sprites\\wall.png").convert()
                sprite_name = "Wall"
            if i == 1:
                sprite = pygame.image.load("sprites\\mac_gyver.png").convert()
                sprite_name = "Start"
            if i == 2:
                sprite = pygame.image.load("sprites\\guard.png").convert()
                sprite_name = "Exit"
            screen.blit(sprite, (x_sprite, y_sprite))
            # We draw a square
            self._display_transparent_square(screen, x_sprite, y_sprite)
            # We display the sprite name
            x_sprite_name = x_sprite + side + 10
            y_sprite_name = y_sprite + 10
            sprite_text = font_arial_10.render(sprite_name, False, black)
            screen.blit(sprite_text, (x_sprite_name, y_sprite_name))
        # 2. Second section
        # 2.1. Title
        title2 = font_arial_12_bold.render('Status:', False, black)
        screen.blit(title1,(x0, y0 + 8 * side))
        # 2.2. Logic light (red/yellow/green)
        x_light = x0
        y_red = y0 + 10 * side
        y_yellow = y0 + 12 * side
        y_green = y0 + 14 * side
        if self.logic_light == "red":
            y_light = y_red
            color = (255, 0, 0)
        elif self.logic_light == "yellow":
            y_light = y_yellow
            color = (255, 242, 0)
        elif self.logic_light == "green":
            y_light = y_green
            color = (0, 255, 0)
        else:
            raise ValueError(self.logic_light)
        pygame.draw.rect(screen, color, (x_light, y_light, side, side))
        self._display_transparent_square(screen, x_light, y_red)
        self._display_transparent_square(screen, x_light, y_yellow)
        self._display_transparent_square(screen, x_light, y_green)
        # 2.3. Logic light description
        red_msg = "This labyrinth is wrong!"
        yellow_msg = "This labyrinth may be playable."
        green_msg = "This labyrinth is playable!"
        red_text = font_arial_10.render(red_msg, False, black)
        yellow_text = font_arial_10.render(yellow_msg, False, black)
        green_text = font_arial_10.render(green_msg, False, black)
        screen.blit(red_text, (x_light + side + 10, y_red + 10))
        screen.blit(yellow_text, (x_light + side + 10, y_yellow + 10))
        screen.blit(green_text, (x_light + side + 10, y_green + 10))
        # screen refresh
        pygame.display.flip()

    def _display_transparent_square(self, screen, x, y):
       """This method displays a transparent square,
       with the same size as the sprites.
       The top left angle is located at (x,y).
       We assume that pygame has been initialized."""
       # We draw an "empty" square by drawing only the sides
       black = (0,0,0)
       side = self.sprite_size
       pygame.draw.rect(screen, black, (x, y, side, 1)) # top side
       pygame.draw.rect(screen, black, (x, y + side, side, 1)) # bottom side
       pygame.draw.rect(screen, black, (x, y, 1, side)) # left side
       pygame.draw.rect(screen, black, (x + side, y, 1, side)) # right side
       # screen refresh
       pygame.display.flip()

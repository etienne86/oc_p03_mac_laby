#! /usr/bin/env python3
# coding: utf-8

"""This module contains the 'Dashboard' class.
This allows to display a labyrinth.
This module uses pygame as main support.
"""

import os

import pygame
from pygame.locals import *

from interface import Interface


class Dashboard:
    """This class allows to create and modify a dashoard."""

    def __init__(self, mode):
        """This special method is the class constructor."""
        self.mode = mode  # type is str
        self.logic_light = "yellow"  # possible values: "red"/"yellow"/"green"

    def display(self, screen, tools=[]):
        """This method displays the dashboard.
        We assume that pygame has been initialized."""
        side = Interface.SPRITE_SIZE
        # Our fonts
        font_title = pygame.font.SysFont('Arial', 16, bold=True)
        font_txt = pygame.font.SysFont('Arial', 14)
        fonts = (font_title, font_txt)
        # 1. First section
        # 1.1. Title
        title_1 = ""
        if self.mode == "game":
            title_1 = "Tools found until now:"
        elif self.mode == "edit":
            title_1 = "Left click to select, right click to release:"
        else:
            raise ValueError("This mode is not permitted!")
        screen.blit(fonts[0].render(title_1, False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0],
                     Interface.DASHBOARD_ORIGIN[1]))
        # 1.2. Items
        # This depends on mode (cf. _game_display and _edit_display)
        # 2. Second section
        # 2.1. Title
        screen.blit(fonts[0].render('Status:', False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0],
                     Interface.DASHBOARD_ORIGIN[1] + 7 * side))
        # Draw the black squares
        pygame.draw.rect(screen, (0, 0, 0),
                         (Interface.DASHBOARD_ORIGIN[0],
                          Interface.DASHBOARD_ORIGIN[1] + 8 * side,
                          side, side))
        pygame.draw.rect(screen, (0, 0, 0),
                         (Interface.DASHBOARD_ORIGIN[0],
                          Interface.DASHBOARD_ORIGIN[1] + 9.5 * side,
                          side, side))
        pygame.draw.rect(screen, (0, 0, 0),
                         (Interface.DASHBOARD_ORIGIN[0],
                          Interface.DASHBOARD_ORIGIN[1] + 11 * side,
                          side, side))
        # 2.2. Logic light (red/yellow/green)
        if self.logic_light == "red":
            y_light = Interface.DASHBOARD_ORIGIN[1] + 8 * side
            colour = (255, 0, 0)
        elif self.logic_light == "yellow":
            y_light = Interface.DASHBOARD_ORIGIN[1] + 9.5 * side
            colour = (255, 242, 0)
        elif self.logic_light == "green":
            y_light = Interface.DASHBOARD_ORIGIN[1] + 11 * side
            colour = (0, 255, 0)
        else:
            raise ValueError(self.logic_light)
        # Draw the logic light
        pygame.draw.rect(screen, colour, (Interface.DASHBOARD_ORIGIN[0],
                                          y_light, side, side))
        display_transparent_square(screen, Interface.DASHBOARD_ORIGIN[0],
                                   Interface.DASHBOARD_ORIGIN[1] + 8 * side)
        display_transparent_square(screen, Interface.DASHBOARD_ORIGIN[0],
                                   Interface.DASHBOARD_ORIGIN[1] + 9.5 * side)
        display_transparent_square(screen, Interface.DASHBOARD_ORIGIN[0],
                                   Interface.DASHBOARD_ORIGIN[1] + 11 * side)
        # 2.3. Logic light description
        # This depends on mode (cf. _game_display and _edit_display)
        # 3. Third section
        screen.blit(fonts[0].render("Press 'Esc' to quit",
                                              False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0],
                     Interface.DASHBOARD_ORIGIN[1] + 14 * side))
        # We call the protected methods
        if self.mode == "game":
            self._game_display(screen, tools, side, fonts)
        elif self.mode == "edit":
            self._edit_display(screen, side, fonts)
        else:
            raise ValueError("This mode is not permitted!")
        # Screen refresh
        pygame.display.flip()

    def _game_display(self, screen, tools, side, fonts):
        """This protected method displays the dashboard in game mode.
        This method can be only called by the method "game_display".
        We assume that pygame has been initialized."""
        # 1.2. Items
        for i, tool in enumerate(tools):
            y_tool = Interface.DASHBOARD_ORIGIN[1]\
                    + ((2*i + (1 - 0.5*i)) * side)
            # We draw an "empty" square
            display_transparent_square(screen,
                                       Interface.DASHBOARD_ORIGIN[0], y_tool)
            # We display the tool name
            screen.blit(fonts[1].render(tool.name, False, (0, 0, 0)),
                        (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                         y_tool + 10))
            # We fill the square with the sprite if the tool is found
            if tool.found:
                sprite_path = os.path.join("sprites", "tools",
                                           tool.name + ".png")
                screen.blit(pygame.image.load(sprite_path).convert(),
                            (Interface.DASHBOARD_ORIGIN[0], y_tool))
        # 2. Second section
        # 2.3. Logic light description
        screen.blit(fonts[1].render("=> You lose... The guard kills you!",
                                         False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                     Interface.DASHBOARD_ORIGIN[1] + 8 * side + 10))
        screen.blit(fonts[1].render("=> You are alive, good luck!",
                                         False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                     Interface.DASHBOARD_ORIGIN[1] + 9.5 * side + 10))
        screen.blit(fonts[1].render("=> You win! Congratulations!",
                                         False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                     Interface.DASHBOARD_ORIGIN[1] + 11 * side + 10))

    def _edit_display(self, screen, side, fonts):
        """This protected method displays the dashboard in edit mode.
        This method can be only called by the method "game_display".
        We assume that pygame has been initialized."""
        # 1.2. Items
        for i in range(3):
            y_sprite = Interface.DASHBOARD_ORIGIN[1]\
                    + ((2*i + (1 - 0.5*i)) * side)
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
            screen.blit(sprite, (Interface.DASHBOARD_ORIGIN[0], y_sprite))
            # We draw a square
            display_transparent_square(screen, Interface.DASHBOARD_ORIGIN[0],
                                       y_sprite)
            # We display the sprite name
            screen.blit(fonts[1].render(sprite_name, False, (0, 0, 0)),
                        (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                         y_sprite + 10))
        # 2.3. Logic light description
        screen.blit(fonts[1].render("=> This labyrinth is wrong!",
                                         False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                     Interface.DASHBOARD_ORIGIN[1] + 8 * side + 10))
        screen.blit(fonts[1].render("=> This labyrinth may be playable.",
                                         False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                     Interface.DASHBOARD_ORIGIN[0] + 9.5 * side + 10))
        screen.blit(fonts[1].render("=> This labyrinth is playable!",
                                         False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                     Interface.DASHBOARD_ORIGIN[1] + 11 * side + 10))


def display_transparent_square(screen, x_pos, y_pos):
    """This function displays a transparent square,
    with the same size as the sprites.
    The top left angle is located at (x_pos, y_pos).
    We assume that pygame has been initialized."""
    # We draw an "empty" square by drawing only the sides
    black = (0, 0, 0)
    side = Interface.SPRITE_SIZE
    # top side
    pygame.draw.rect(screen, black, (x_pos, y_pos, side, 1))
    # bottom side
    pygame.draw.rect(screen, black, (x_pos, y_pos + side, side, 1))
    # left side
    pygame.draw.rect(screen, black, (x_pos, y_pos, 1, side))
    # right side
    pygame.draw.rect(screen, black, (x_pos + side, y_pos, 1, side))
    # Screen refresh
    pygame.display.flip()

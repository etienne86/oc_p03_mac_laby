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
        if self.mode == "game":
            self._game_display(screen, tools)
        elif self.mode == "edit":
            self._edit_display(screen)
        else:
            raise ValueError("This mode is not permitted!")

    def _game_display(self, screen, tools):
        """This method displays the dashboard in game mode.
        We assume that pygame has been initialized."""
        side = Interface.SPRITE_SIZE
        # Our fonts
        font_arial_16_bold = pygame.font.SysFont('Arial', 16, bold=True)
        font_arial_14 = pygame.font.SysFont('Arial', 14)
        # 1. First section
        # 1.1. Title
        screen.blit(font_arial_16_bold.render('Tools found until now:',
                                              False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0],
                     Interface.DASHBOARD_ORIGIN[1]))
        # 1.2. Items
        for i, tool in enumerate(tools):
            y_tool = Interface.DASHBOARD_ORIGIN[1]\
                    + ((2*i + (1 - 0.5*i)) * side)
            # We draw an "empty" square
            display_transparent_square(screen,
                                       Interface.DASHBOARD_ORIGIN[0], y_tool)
            # We display the tool name
            screen.blit(font_arial_14.render(tool.name, False, (0, 0, 0)),
                        (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                         y_tool + 10))
            # We fill the square with the sprite if the tool is found
            if tool.found:
                sprite_path = os.path.join("sprites", "tools",
                                           tool.name + ".png")
                screen.blit(pygame.image.load(sprite_path).convert(),
                            (Interface.DASHBOARD_ORIGIN[0], y_tool))
        # 2. Second section
        # 2.1. Title
        screen.blit(font_arial_16_bold.render('Status:', False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0],
                     Interface.DASHBOARD_ORIGIN[1] + 7 * side))
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
        screen.blit(font_arial_14.render("=> You lose... The guard kills you!",
                                         False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                     Interface.DASHBOARD_ORIGIN[1] + 8 * side + 10))
        screen.blit(font_arial_14.render("=> You are alive, good luck!",
                                         False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                     Interface.DASHBOARD_ORIGIN[1] + 9.5 * side + 10))
        screen.blit(font_arial_14.render("=> You win! Congratulations!",
                                         False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                     Interface.DASHBOARD_ORIGIN[1] + 11 * side + 10))
        # 3. Third section
        screen.blit(font_arial_16_bold.render("Press 'Esc' to quit",
                                              False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0],
                     Interface.DASHBOARD_ORIGIN[1] + 14 * side))
        # Screen refresh
        pygame.display.flip()

    def _edit_display(self, screen):
        """This method displays the dashboard in edit mode.
        We assume that pygame has been initialized."""
        side = Interface.SPRITE_SIZE
        # Our fonts
        font_arial_16_bold = pygame.font.SysFont('Arial', 16, bold=True)
        font_arial_14 = pygame.font.SysFont('Arial', 14)
        # 1. First section
        # 1.1. Title
        instruction = "Left click to select, right click to release:"
        screen.blit(font_arial_16_bold.render(instruction, False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0],
                     Interface.DASHBOARD_ORIGIN[1]))
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
            screen.blit(font_arial_14.render(sprite_name, False, (0, 0, 0)),
                        (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                         y_sprite + 10))
        # 2. Second section
        # 2.1. Title
        screen.blit(font_arial_16_bold.render('Status:', False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0],
                     Interface.DASHBOARD_ORIGIN[1] + 7 * side))
        # 2.2. Logic light (red/yellow/green)
        if self.logic_light == "red":
            y_light = Interface.DASHBOARD_ORIGIN[1] + 8 * side
            colour = (255, 0, 0)
        elif self.logic_light == "yellow":
            y_light = Interface.DASHBOARD_ORIGIN[0] + 9.5 * side
            colour = (255, 242, 0)
        elif self.logic_light == "green":
            y_light = Interface.DASHBOARD_ORIGIN[1] + 11 * side
            colour = (0, 255, 0)
        else:
            raise ValueError(self.logic_light)
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
        # Draw the logic light
        pygame.draw.rect(screen, colour, (Interface.DASHBOARD_ORIGIN[0],
                                          y_light, side, side))
        display_transparent_square(screen, Interface.DASHBOARD_ORIGIN[0],
                                   Interface.DASHBOARD_ORIGIN[1] + 8 * side)
        display_transparent_square(screen, Interface.DASHBOARD_ORIGIN[0],
                                   Interface.DASHBOARD_ORIGIN[0] + 9.5 * side)
        display_transparent_square(screen, Interface.DASHBOARD_ORIGIN[0],
                                   Interface.DASHBOARD_ORIGIN[1] + 11 * side)
        # 2.3. Logic light description
        screen.blit(font_arial_14.render("=> This labyrinth is wrong!",
                                         False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                     Interface.DASHBOARD_ORIGIN[1] + 8 * side + 10))
        screen.blit(font_arial_14.render("=> This labyrinth may be playable.",
                                         False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                     Interface.DASHBOARD_ORIGIN[0] + 9.5 * side + 10))
        screen.blit(font_arial_14.render("=> This labyrinth is playable!",
                                         False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0] + side + 10,
                     Interface.DASHBOARD_ORIGIN[1] + 11 * side + 10))
        # 3. Third section
        screen.blit(font_arial_16_bold.render("Press 'Esc' to quit",
                                              False, (0, 0, 0)),
                    (Interface.DASHBOARD_ORIGIN[0],
                     Interface.DASHBOARD_ORIGIN[1] + 14 * side))
        # Screen refresh
        pygame.display.flip()


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

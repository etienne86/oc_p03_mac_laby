#! /usr/bin/env python3
# coding: utf-8

"""This module contains the 'Player' class."""


class Player:
    """This class is used to represent the player in the labyrinth."""

    def __init__(self, x_pos, y_pos):
        """This special method is the class constructor."""
        self.is_alive = True
        self.wins = False
        self.x_pos = x_pos # type is int
        self.y_pos = y_pos # type is int
        self.authorized_movements = {"up": False, "down": False,
                                     "left": False, "right": False}

    def move(self, direction):
        """This method moves the player one step into 'direction',
        if authorized."""
        if direction == "up":
            self.y_pos -= 1
        elif direction == "down":
            self.y_pos += 1
        elif direction == "left":
            self.x_pos -= 1
        elif direction == "right":
            self.x_pos += 1
        else:
            raise ValueError(direction)

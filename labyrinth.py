#! /usr/bin/env python3
# coding: utf-8

"""This module contains the 'Labyrinth' class.

The game grid is represented with a pandas.Dataframe object,
containing integers:
'0' are paths, where we can possibly see the player or the tools
'1' are walls
'2' is the labyrinth exit, i.e. the guard location (unique occurrence)
'3' is the start point, i.e. the initial player location (unique occurrence),
and has the same role as a path during the game

We assume that each labyrinth side (top & bottom rows, left & right columns)
is composed with walls, except a unique location which is the labyrinth exit.
"""

import math
import random

#import numpy as np
import pandas as pd

from player import Player
from tool import Tool


class Labyrinth:
    """This class allows to create and modify a labyrinth."""

    def __init__(self, width, height, csv_file):
        """This special method is the class constructor."""
        self.height = height # type is int
        self.width = width # type is int
        self.player = Player(-1,-1) # initialization out of the labyrinth
        # 'initialize_grid_from_file' method assignes the real player location
        # 'self.grid' type is pandas.Dataframe
        self.grid = self.initialize_grid_from_file(csv_file)
        # 'self.tools' type is list containing items of <class 'Tool'>
        self.tools = self.position_tools_randomly()

    @property
    def x_exit(self):
        """This property returns the exit location on X axis."""
        x = 0
        y = 0
        for row in self.grid.values:
            for val in row:
                if val == value:
                    break
                else:
                    y += 1
            if val == value:
                break
            else:
                x += 1
        return x

    @property
    def y_exit(self):
        """This property returns the exit location on Y axis."""
        x = 0
        y = 0
        for row in self.grid.values:
            for val in row:
                if val == value:
                    break
                else:
                    y += 1
            if val == value:
                break
            else:
                x += 1
        return y

    def analyze_game_status(self):
        """This method determins if the game continues
        (nothing special happens), or if the player wins or loses."""
        x2 = self.x_exit
        y2 = self.y_exit
        x3 = self.player.x_pos
        y3 = self.player.y_pos
        all_tools_found = True
        for i in range(len(tools)):
            all_tools_found = all_tools_found and self.tools[i].found 
        # if player and guard are neighbours on the grid
        if (x2 == x3 and math.fabs(y2 - y3) == 1)\
        or (math.fabs(x2 - x3) == 1 and y2 == y3):
            if all_tools_found:
                self.player_wins = True
            else:
                self.player_is_alive = False

    def authorize_player_movements():
        """This method updates the player authorized movements."""
        x = self.player.x_pos
        y = self.player.y_pos
        up = (x,y-1)
        down = (x,y+1)
        left = (x-1,y)
        right = (x+1,y)
        # Since the labyrinth sides are composed with walls and the exit,
        # 'up', 'down', 'left' and 'right' are well inside the grid.
        # If the neighbour location is a wall ('1'), the movement is forbidden.
        # Otherwise, the neighbour location is necessarily a path ('0' or '3'),
        # thus the movement is authorized.
        # The neighbour location cannot be the exit ('2') during the game.
        if self.grid.iloc[up] == 1:
            self.player.authorized_movements["up"] = False
        elif self.grid.iloc[up] in [0,3]:
            self.player.authorized_movements["up"] = True
        if self.grid.iloc[down] == 1:
            self.player.authorized_movements["down"] = False
        elif self.grid.iloc[down] in [0,3]:
            self.player.authorized_movements["down"] = True
        if self.grid.iloc[left] == 1:
            self.player.authorized_movements["left"] = False
        elif self.grid.iloc[left] in [0,3]:
            self.player.authorized_movements["left"] = True
        if self.grid.iloc[right] == 1:
            self.player.authorized_movements["right"] = False
        elif self.grid.iloc[right] in [0,3]:
            self.player.authorized_movements["right"] = True

    def count_paths(self):
        """This methods returns the number of '0' (paths) in the labyrinth."""
        counter = 0
        for row in self.grid.values: # iteration on row
            for val in row: # iteration on items
                if val == 0:
                    counter += 1
        return counter

    def find_tool():
        """This method switches to 'True' the 'found' tool attribute,
        if the tool is found by the player."""
        for tool in self.tools:
            # if the player and the tool are at the same place
            if self.player.x_pos == tool.x_pos\
            and self.player.y_pos == tool.y_pos:
                tool.found = True

    def initialize_grid_from_file(self, csv_file):
        """This method creates the labyrinth grid from an external CSV file."""
        # we create a pandas.DataFrame object
        grid_df = pd.read_csv(csv_file, sep=";") # grid initialization from CSV
        return grid_df

    def initialize_player_location(self):
        """This method assignes the real player location in the labyrinth."""
        for row in self.grid.values: # iteration on rows
            for i, val in enumerate(row): # iteration on items
                if val == 3: # if we are on the player location
                    self.player.x_pos = i
                    self.player.y_pos = row

    def position_tools_randomly(self):
        """This method randomly positions the tools in the labyrinth."""
        tools = []
        tools_names = Tool.TOOLS_NAMES # we import our tools names
        tools_qty = len(tools_names)
        paths_counter = self.count_paths()
        # random selection of samples among the paths locations
        random_list = random.sample(range(paths_counter), tools_qty)
        for k, tool_name in enumerate(tools_names): # iteration on tools
            k_random_counter = 0
            k_random_rank = random_list[k]
            for row in self.grid.values: # iteration on rows
                for i, val in enumerate(row): # iteration on items
                    if val == 0: # if we are on a path
                        # if we are on the randomly selected location
                        if k_random_counter == k_random_rank:
                            # we position the tool here
                            tool = Tool(tools_names[k], i, row)
                            # we add the tool in the list
                            tools.append(tool) 
                        else:
                            k_random_counter += 1
        return tools

    def save_grid_to_file(self, csv_file):
        """This method saves the labyrinth grid to an external CSV file.
        This is useful to modify the labyrinth in edit mode."""
        self.grid.to_csv(path_or_buf=csv_file, sep=';')
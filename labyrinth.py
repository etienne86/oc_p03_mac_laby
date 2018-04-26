#! /usr/bin/env python3
# coding: utf-8

"""This module contains the 'Labyrinth' class,
and a function used for initialization.

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

import pandas as pd

from player import Player
from tool import Tool


class Labyrinth:
    """This class allows to create and modify a labyrinth."""

    def __init__(self, width, height, csv_file):
        """This special method is the class constructor."""
        self.width = width  # type is int
        self.height = height  # type is int
        self.player = Player(-1, -1)  # initialization out of the labyrinth
        # 'initialize_grid_from_file' method assignes the real player location
        # 'self.grid' type is pandas.Dataframe
        self.grid = pd.read_csv(csv_file, sep=";")
        # 'self.tools' type is list containing items of <class 'Tool'>
        self.tools = self.position_tools_randomly()

    @property
    def x_exit(self):
        """This property returns the exit location on X axis."""
        x_guard = -1
        y_pos = 0
        for y_l in range(self.height):  # iteration over rows
            x_pos = 0
            for x_l in range(self.width):  # iteration over columns
                if self.grid.iloc[y_l, x_l] == 2:
                    x_guard = x_pos
                else:
                    x_pos += 1
            y_pos += 1
        return x_guard

    @property
    def y_exit(self):
        """This property returns the exit location on Y axis."""
        y_guard = -1
        y_pos = 0
        for y_l in range(self.height):  # iteration over rows
            x_pos = 0
            for x_l in range(self.width):  # iteration over columns
                if self.grid.iloc[y_l, x_l] == 2:
                    y_guard = y_pos
                else:
                    x_pos += 1
            y_pos += 1
        return y_guard

    def analyze_game_status(self):
        """This method determins if the game continues
        (nothing special happens), or if the player wins or loses."""
        x_2 = self.x_exit
        y_2 = self.y_exit
        x_3 = self.player.x_pos
        y_3 = self.player.y_pos
        all_tools_found = True
        # we check if all tools are found by the player
        for i in range(len(self.tools)):
            all_tools_found = all_tools_found and self.tools[i].found
        # if the player and the guard are neighbours on the grid
        if ((x_2 == x_3) and (math.fabs(y_2 - y_3) == 1))\
                or ((math.fabs(x_2 - x_3) == 1) and (y_2 == y_3)):
            # we modify two attributes
            self.player.wins = all_tools_found
            self.player.is_alive = all_tools_found

    def analyze_playability(self):
        """This method determins if the labyrinth is playable,
        i.e. returns 'True' if we can play with, otherwise 'False'.

        The rules for the labyrinth to be playable are the following:
        1. there is one, and only one, player
        2. there is one, and only one, guard
        3. each corner of the map is a wall
        4. each location on the edge of the map is a wall,
        except one which is the guard
        5. the player and the guard cannot be neighbours when starting the game
        6. we can reach the location next to the guard from only one direction,
        because of the random tools positioning (tools have to be reachable),
        i.e. the location next to the guard has four neighbours:
            - the guard (grid value: 2)
            - a path or the player (grid value: 0 or 3)
            - a wall (grid value: 1)
            - another wall (grid value: 1)
        7. there are at least 4 free locations for the tools and the player
        8. the player has to be able to reach the exit from each location,
        thus all the tools can be found in the labyrinth
        """
        result = True
        values_list = []
        for x_l in range(self.width):
            for y_l in range(self.height):
                values_list.append(self.grid.iloc[y_l, x_l])
        # we check if rule #1 is true
        if values_list.count(3) == 1:
            x_3 = self.player.x_pos
            y_3 = self.player.y_pos
        else:
            result = False
        # we check if rule #2 is true
        if values_list.count(2) == 1:
            x_2 = self.x_exit
            y_2 = self.y_exit
        else:
            result = False
        # we check if rule #3 is true
        result = result and self.grid.iloc[0, 0] == 1\
                and self.grid.iloc[self.height - 1, 0] == 1\
                and self.grid.iloc[0, self.width - 1] == 1\
                and self.grid.iloc[self.height - 1, self.width - 1] == 1
        # we check if rule #4 is true
        if result:
            # we collect each grid value which is on an edge in a list
            edge_list = []
            for y_l in range(self.height):
                for x_l in range(self.width):
                    if x_l in [0, self.width - 1]\
                            or y_l in [0, self.height - 1]:
                        edge_list.append(self.grid.iloc[y_l, x_l])
            try:
                len(edge_list) == self.width * 2 + self.height * 2 - 4
            except:
                raise ValueError(self.width * 2 + self.height * 2 - 4)
            result = result and (edge_list.count(1) == len(edge_list) - 1)\
                    and (edge_list.count(2) == 1)
        # we check if rule #5 is true
        if result:
            # if the player and the guard are neighbours on the grid
            if ((x_2 == x_3) and (math.fabs(y_2 - y_3) == 1))\
                    or ((math.fabs(x_2 - x_3) == 1) and (y_2 == y_3)):
                result = False
        # we check if rule #6 is true
        if result:
            # if the guard is on the left edge
            if x_2 == 0:
                # location to win
                x_win = x_2 + 1
                y_win = y_2
                # neighbours list of this "win location"
                neighbours = [self.grid.iloc[y_win, x_win + 1],
                              self.grid.iloc[y_win - 1, x_win],
                              self.grid.iloc[y_win + 1, x_win]
                             ]
            # if the guard is on the right edge
            elif x_2 == self.width - 1:
                # location to win
                x_win = x_2 - 1
                y_win = y_2
                # neighbours list of this "win location"
                neighbours = [self.grid.iloc[y_win, x_win - 1],
                              self.grid.iloc[y_win - 1, x_win],
                              self.grid.iloc[y_win + 1, x_win]
                             ]
            # if the guard is on the top edge
            elif y_2 == 0:
                # location to win
                x_win = x_2
                y_win = y_2 + 1
                # neighbours list of this "win location"
                neighbours = [self.grid.iloc[y_win + 1, x_win],
                              self.grid.iloc[y_win, x_win - 1],
                              self.grid.iloc[y_win, x_win + 1]
                             ]
            # if the guard is on the bottom edge
            elif y_2 == self.height - 1:
                # location to win
                x_win = x_2
                y_win = y_2 - 1
                # neighbours list of this "win location"
                neighbours = [self.grid.iloc[y_win - 1, x_win],
                              self.grid.iloc[y_win, x_win - 1],
                              self.grid.iloc[y_win, x_win + 1]
                             ]
            else:
                raise ValueError((x_2, y_2))
            # we sort the neighbours list
            neighbours.sort()
            # we update 'result'
            result = result and (self.grid.iloc[y_win, x_win] == 0) and\
                    neighbours in [[0, 1, 1], [1, 1, 3]]
        # we check if rule #7 is true
        result = result and (self.count_paths() >= 3)
        # we check if rule #8 is true
        if result:
            checked_loc = []
            # we initialize a 2D-matrix with 'False' as each item value
            bool_matr = []
            bool_list = []
            for i in range(self.height):
                bool_list.append(False)
            for j in range(self.width):
                bool_matr.append(bool_list)
            # we check each item in the grid
            for y_l in range(self.height):
                for x_l in range(self.width):
                    # if this is a path or the player location
                    if self.grid.iloc[y_l, x_l] in [0, 3]:
                        # we check if the exit is reachable
                        bool_matr[y_l][x_l] = self._reach_exit(x_l, y_l, x_win,
                                                               y_win,
                                                               checked_loc,
                                                               bool_matr)
                        result = result and bool_matr[y_l][x_l]
        return result

    def _reach_exit(self, x_l, y_l, x_win, y_win, checked_loc, bool_matr):
        """This protected method checks if we can reach the exit,
        from each location in the labyrinth.
        We use a recursive check."""
        result = bool(bool_matr[y_l][x_l])
        counter = 0
        # initial check
        if x_l == x_win and y_l == y_win:
            result = True
            bool_matr[y_l][x_l] = True
            checked_loc.append((x_l, y_l))
        # recursive check
        elif (x_l, y_l) not in checked_loc:
            checked_loc.append((x_l, y_l))
            # we build a list of neighbour paths
            neighbour_paths_list = []
            if self.grid.iloc[y_l - 1, x_l] in [0, 3]:
                neighbour_paths_list.append((x_l, y_l - 1))
            if self.grid.iloc[y_l + 1, x_l] in [0, 3]:
                neighbour_paths_list.append((x_l, y_l + 1))
            if self.grid.iloc[y_l, x_l - 1] in [0, 3]:
                neighbour_paths_list.append((x_l - 1, y_l))
            if self.grid.iloc[y_l, x_l + 1] in [0, 3]:
                neighbour_paths_list.append((x_l + 1, y_l))
            # we limitate the 'while' loop with a counter
            while counter <= (self.count_paths() + 1) and not result:
                for tup in neighbour_paths_list:
                    # if the neighbour location has not been checked yet
                    if tup not in checked_loc:
                        # if the matrix value of neighbour location is True
                        if bool_matr[tup[1]][tup[0]]:
                            # we can reach the exit
                            result = True
                        # if the neighbour location can reach the exit
                        elif self._reach_exit(tup[0], tup[1], x_win, y_win,
                                              checked_loc, bool_matr):
                            # we update the matrix for the neighbour location
                            bool_matr[tup[1]][tup[0]] = True
                            # we can reach the exit
                            result = True
                        # # we remove the neighbour from the checked list
                        # checked_loc.remove(tup)
                counter += 1
        return result

    def authorize_player_movements(self):
        """This method updates the player authorized movements."""
        x_player = self.player.x_pos
        y_player = self.player.y_pos
        # To use 'iloc' method with a DataFrame object (df),
        # we write df.iloc[row, col] with row = y and col = x,
        # i.e. this is equivalent to write df.iloc[y,x]
        up_in_df = (y_player - 1, x_player)
        down_in_df = (y_player + 1, x_player)
        left_in_df = (y_player, x_player - 1)
        right_in_df = (y_player, x_player + 1)
        # Since the labyrinth sides are composed with walls and the exit,
        # 'up', 'down', 'left' and 'right' are well inside the grid.
        # If the neighbour location is a wall ('1'), the movement is forbidden.
        # Otherwise, the neighbour location is necessarily a path ('0' or '3'),
        # thus the movement is authorized.
        # The neighbour location cannot be the exit ('2') during the game.
        if self.grid.iloc[up_in_df] == 1:
            self.player.authorized_movements["up"] = False
        elif self.grid.iloc[up_in_df] in [0, 3]:
            self.player.authorized_movements["up"] = True
        if self.grid.iloc[down_in_df] == 1:
            self.player.authorized_movements["down"] = False
        elif self.grid.iloc[down_in_df] in [0, 3]:
            self.player.authorized_movements["down"] = True
        if self.grid.iloc[left_in_df] == 1:
            self.player.authorized_movements["left"] = False
        elif self.grid.iloc[left_in_df] in [0, 3]:
            self.player.authorized_movements["left"] = True
        if self.grid.iloc[right_in_df] == 1:
            self.player.authorized_movements["right"] = False
        elif self.grid.iloc[right_in_df] in [0, 3]:
            self.player.authorized_movements["right"] = True

    def count_paths(self):
        """This methods returns the number of '0' (paths) in the labyrinth."""
        counter = 0
        for y_l in range(self.height):
            for x_l in range(self.width):
                if self.grid.iloc[y_l, x_l] == 0:
                    counter += 1
        return counter

    def find_tool(self):
        """This method switches to 'True' the 'found' tool attribute,
        if the tool is found by the player."""
        for tool in self.tools:
            # if the player and the tool are at the same place
            if self.player.x_pos == tool.x_pos\
                    and self.player.y_pos == tool.y_pos:
                tool.found = True

    def initialize_player_location(self):
        """This method assignes the real player location in the labyrinth."""
        for y_l in range(self.height):
            for x_l in range(self.width):
                if self.grid.iloc[y_l, x_l] == 3:  # if we are on the player location
                    self.player.x_pos = x_l
                    self.player.y_pos = y_l

    def position_tools_randomly(self):
        """This method randomly positions the tools in the labyrinth."""
        tools = []
        tools_names = Tool.TOOLS_NAMES  # we import our tools names
        tools_qty = len(tools_names)
        paths_counter = self.count_paths()
        # random selection of samples among the paths locations
        random_list = random.sample(range(paths_counter), tools_qty)
        for k in enumerate(tools_names):  # iteration on tools
            # k is a tuple where only k[0] is interesting here
            k_random_counter = 0
            k_random_rank = random_list[k[0]]
            for y_l in range(self.height):
                for x_l in range(self.width):
                    # if we are on a path
                    if self.grid.iloc[y_l, x_l] == 0:
                        # if we are on the randomly selected location
                        if k_random_counter == k_random_rank:
                            # we position the tool here
                            tool = Tool(tools_names[k[0]], x_l, y_l)
                            # we add the tool in the list
                            tools.append(tool)
                        k_random_counter += 1
        return tools

    def save_grid_to_file(self, csv_file):
        """This method saves the labyrinth grid to an external CSV file.
        This is useful to modify the labyrinth in edit mode."""
        self.grid.to_csv(path_or_buf=csv_file, sep=';', index=False)

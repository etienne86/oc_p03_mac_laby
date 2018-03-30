#! /usr/bin/env python3
# coding: utf-8

"""This module contains the 'Labyrinth' class.
This includes game logics.

The game grid is represented with a pandas.Dataframe object,
containing integers:
'0' are paths
'1' are walls
'2' (only once in the pandas.Dataframe object) is the player (Mac Gyver)
'3' (only once in the pandas.Dataframe object) is the guard
'4' (only once in the pandas.Dataframe object) is the tube (4 characters)
'5' (only once in the pandas.Dataframe object) is the ether (5 characters)
'6' (only once in the pandas.Dataframe object) is the needle (6 characters)
"""

import math
import random

import numpy as np
import pandas as pd


class Labyrinth:
    """This class allows to create and modify a labyrinth."""

    def __init__(self, width, height, csv_file):
        """This special method is the class constructor."""
        self.height = height # type is int
        self.width = width # type is int
        # 'self.grid' type is pandas.Dataframe
        self.grid = self.initialize_grid_from_file(csv_file)
        self.player_is_alive = True
        self.ether_is_found = False
        self.needle_is_found = False
        self.tube_is_found = False
        self.player_wins = False

    def analyze_game_status(self):
        """This method determins if the game continues
        (nothing special happens), or if the player wins or loses."""
        (x2,y2) = self.determin_item_location(2) # player location
        (x3,y3) = self.determin_item_location(3) # guard location
        if (x2 == x3 and math.fabs(y2 - y3) == 1)\
        or (y2 == y3 and math.fabs(x2 - x3) == 1):
        # if player and guard are neighbours
            if self.ether_is_found\
            and self.needle_is_found\
            and self.tube_is_found:
            # if all three objects are found
                self.player_wins = True
            else:
                self.player_is_alive = False

    def count_value(self, value):
        """This methods returns the number of 'value' occurences
        in the labyrinth."""
        value_counter = 0
        for row in self.grid.values:
            for val in row:
                if val == value:
                    value_counter += 1
        return value_counter

    def determin_item_location(self, value):
        """This method returns a tuple (x,y) with the location of an item.
        Item can be '2' (player), '3' (guard), '4'/'5'/'6' (object to find)."""
        x,y = 0
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
        return (x,y)

    def find_ether(self):
        """This method modifies the attribute 'ether_is_found'
        when the ether is found."""
        if not self.ether_is_found:
            for column in self.grid:
                try:
                    i = column.index(5) # '5' is at most once in the labyrinth
                except ValueError: # for each column except the column with '5'
                    pass
                else:
                    self.ether_is_found = True

    def find_needle(self):
        """This method modifies the attribute 'needle_is_found'
        when the needle is found."""
        if not self.ether_is_found:
            for column in self.grid:
                try:
                    i = column.index(6) # '6' is only once in the labyrinth
                except ValueError: # for each column except the column with '6'
                    pass
                else:
                    self.ether_is_found = True

    def find_tube(self):
        """This method modifies the attribute 'tube_is_found'
        when the tube is found."""
        if not self.ether_is_found:
            for column in self.grid:
                try:
                    i = column.index(4) # '4' is only once in the labyrinth
                except ValueError: # for each column except the column with '4'
                    pass
                else:
                    self.ether_is_found = True

    def initialize_grid_from_file(self, csv_file):
        """This method creates the labyrinth grid from an external CSV file."""
        #grid_nd = np.ndarray(shape=(self.width, self.height), dtype=int)
        #grid_df = pd.DataFrame(grid_nd)
        grid_df = pd.read_csv(csv_file, sep=";") # grid initialization from CSV
        return grid_df

    def move_down(self):
        """This method moves the player one step down, if authorized."""
        for col in self.grid: # iteration over columns
            my_column = self.grid[col]
            try:
                i = my_column.index(2) # '2' is only once in the labyrinth
            except ValueError: # for each column except the column containing '2'
                pass
            else:
                if i+1 in [4,5,6]: # if the player finds an object
                    my_column[i+1] = 0 # this object is picked up
                if i+1 == 0:
                    # permutation of two values in the list
                    my_column[i+1], my_column[i] = my_column[i], my_column[i+1]

    def move_left(self):
        """This method moves the player one step left, if authorized."""
        for row in self.grid.iterrows(): # iteration over rows
            my_row = row[1]
            try:
                i = my_row.index(2) # '2' is only once in the labyrinth
            except ValueError: # for each row except the row containing '2'
                pass
            else:
                if i-1 in [4,5,6]: # if the player finds an object
                    my_row[i-1] = 0 # this object disappears
                    # permutation of two values in the list
                    my_row[i-1], my_row[i] = my_row[i], my_row[i-1]

    def move_right(self):
        """This method moves the player one step right, if authorized."""
        for row in self.grid.iterrows(): # iteration over rows
            my_row = row[1]
            try:
                i = my_row.index(2) # '2' is only once in the labyrinth
            except ValueError: # for each row except the row containing '2'
                pass
            else:
                if i+1 in [4,5,6]: # if the player finds an object
                    my_row[i+1] = 0 # this object disappears
                    # permutation of two values in the list
                    my_row[i+1], my_row[i] = my_row[i], my_row[i+1]

    def move_up(self):
        """This method moves the player one step up, if authorized."""
        for column in self.grid: # iteration over columns
            my_column = self.grid[col]
            try:
                i = my_column.index(2) # '2' is only once in the labyrinth
            except ValueError: # for each column except the column containing '2'
                pass
            else:
                if i-1 in [4,5,6]: # if the player finds an object
                    my_column[i-1] = 0 # this object disappears
                    # permutation of two values in the list
                    my_column[i-1], my_column[i] = my_column[i], my_column[i-1]

    def position_objects(self):
        """This method randomly positions the three objets in the labyrinth."""
        paths_counter = self.count_value(0)
        random_list = random.sample(range(paths_counter), 3)
        for obj in [4,5,6]: # iteration on objects to find in the labyrinth
            random_counter = 0
            random_rank = random_list[obj - 4]
            # first lap in loop 'obj in [4,5,6]': random_list[0]      
            # second lap in loop 'obj in [4,5,6]': random_list[1]
            # third/last lap in loop 'obj in [4,5,6]': random_list[2]
            for row in self.grid.values:
                for val in row:
                    if val == 0:
                        if random_counter == random_rank:
                            val = obj # we position the object here
                            break
                        else:
                            random_counter += 1

    def save_grid_to_file(self, csv_file):
        """This method saves the labyrinth grid to an external CSV file.
        This is useful to modify the labyrinth in edit mode."""
        self.grid.to_csv(path_or_buf=csv_file, sep=';')
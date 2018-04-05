#! /usr/bin/env python3
# coding: utf-8

"""This file has to be executed with Python to launch a labyrinth game."""

import os
import time

import pygame
from pygame.locals import *

from interface import Interface
from labyrinth import Labyrinth


LABY_SIZE = 15 # this constant is the square labyrinth side size
               # (number of sprites per side)
SPRITE_SIZE = 30 # this constant is the square sprite width/height in pixels
SCREEN_WIDTH = 800 # number of pixels
SCREEN_HEIGHT = 600 # number of pixels
ORIGIN = (0,0)


def main():
    """This function is the main function to be executed to play the game."""
    pygame.init()
    
    # we build the labyrinth, with the player and the tools to be found
    csv_path = os.path.join("data", "grid.csv")
    game_laby = Labyrinth(LABY_SIZE, LABY_SIZE, csv_path)
    game_laby.initialize_player_location()
    game_player = game_laby.player
    game_tools = game_laby.tools
   
    # we build the main window
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
    game_title = "Mac Gyver Labyrinth - by etienne86"
    back = pygame.image.load("sprites\\blue_sky.png").convert()
    window.blit(back, ORIGIN)
    pygame.display.flip()

    # we load our sprites
    mac_gyver = pygame.image.load("sprites\\mac_gyver.png").convert()
    mac_gyver.set_colorkey((255,255,255)) # we want white to be transparent
    sand_path = pygame.image.load("sprites\\path.png").convert()
    wall = pygame.image.load("sprites\\wall.png").convert()
    guard = pygame.image.load("sprites\\guard.png").convert()
    guard.set_colorkey((255,255,255)) # we want white to be transparent

    # window customization
    mac_gyver_surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
    mac_gyver_surface.blit(mac_gyver, ORIGIN)
    pygame.display.set_icon(mac_gyver_surface) # what is rect? surface?
    pygame.display.set_caption(game_title)
    pygame.display.flip()
    
    # our game interface - will be used later
    #game_interface = Interface(SCREEN_WIDTH, SCREEN_HEIGHT, back, game_title)
    
    # we display our labyrinth
    ## TO DO: see if I replace by a sub-fuction
    laby_origin = (50,100)
    x0 = laby_origin[0]
    y0 = laby_origin[1]
    for j in range(LABY_SIZE): # iteration over columns
        for i in range(LABY_SIZE): # iteration over rows
            x = x0 + (j * SPRITE_SIZE)
            y = y0 + (i * SPRITE_SIZE)
            item = game_laby.grid.iloc[i,j]
            if item == 0:
                sprite = sand_path
            elif item == 1:
                sprite = wall
            elif item == 2:
                sprite = sand_path
                window.blit(sprite, (x,y))
                sprite = guard
            elif item == 3:
                sprite = mac_gyver
            window.blit(sprite, (x,y))
    pygame.display.flip()



    time.sleep(10)

    pygame.quit()


if __name__ == "__main__":
    main()
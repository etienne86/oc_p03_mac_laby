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
SCREEN_ORIGIN = (0,0)


def main():
    """This function is the main function to be executed to play the game."""
    pygame.init()
    
    # we build our labyrinth
    csv_path = os.path.join("data", "grid.csv")
    game_labyrinth = Labyrinth(LABY_SIZE, LABY_SIZE, csv_path)
    game_labyrinth.position_objects() # random objects positioning
   
    # our main window
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
    game_title = "Mac Gyver Labyrinth - by etienne86"
    back = pygame.image.load("sprites\\blue_sky.png").convert()
    window.blit(back, SCREEN_ORIGIN)
    pygame.display.flip()
    
    # window customization
    mac_gyver = pygame.image.load("sprites\\mac_gyver.png").convert()
    mac_gyver.set_colorkey((255,255,255)) # we want white to be transparent
    
    pygame.display.set_icon(mac_gyver_surface) # what is rect? surface?
    pygame.display.set_caption(game_title)
    pygame.display.flip()
    
    # our game interface
    game_interface = Interface(SCREEN_WIDTH, SCREEN_HEIGHT, back, game_title)
    
    time.sleep(5)

    pygame.quit()


if __name__ == "__main__":
    main()
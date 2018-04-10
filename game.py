#! /usr/bin/env python3
# coding: utf-8

"""This file has to be executed with Python to launch a labyrinth game."""

import os

import pygame
from pygame.locals import *

from interface import Interface
from labyrinth import Labyrinth
from labyviewer import LabyViewer
from dashboard import Dashboard


def main():
    """This function is the main function to be executed to play the game."""
    pygame.init()

    # we build the labyrinth, with the player and the tools to be found
    csv_path = os.path.join("data", "grid.csv")
    width = height = LabyViewer.LABY_SIZE
    game_laby = Labyrinth(width, height, csv_path)
    game_laby.initialize_player_location()
    game_player = game_laby.player
    game_tools = game_laby.tools

    # we initialize the main window with our game interface
    window = pygame.display.set_mode((Interface.SCREEN_SIZE))
    game_back = pygame.image.load("sprites\\blue_sky.png").convert()
    game_labyviewer = LabyViewer(Interface.LABY_ORIGIN, game_laby,
                                 game_tools, Interface.SPRITE_SIZE)
    game_dashboard = Dashboard(Interface.DASHBOARD_ORIGIN, "game", Interface.SPRITE_SIZE)
    game_interface = Interface(game_back, game_labyviewer, game_dashboard)
    window.blit(game_back, Interface.SCREEN_ORIGIN)

    # we load our sprites
    mac_gyver = pygame.image.load("sprites\\mac_gyver.png").convert()
    mac_gyver.set_colorkey((255,255,255)) # set white as transparent
    sand_path = pygame.image.load("sprites\\path.png").convert()
    wall = pygame.image.load("sprites\\wall.png").convert()
    guard = pygame.image.load("sprites\\guard.png").convert()
    guard.set_colorkey((255,255,255)) # set white as transparent

    # window customization
    mac_g_alpha = pygame.image.load("sprites\\mac_gyver.png").convert_alpha()
    mac_g_alpha.set_colorkey((255,255,255)) # set white as transparent
    pygame.display.set_icon(mac_g_alpha)
    window_title = "Mac Gyverinth - game mode - by etienne86"
    pygame.display.set_caption(window_title)
    pygame.display.flip()
    
    # we display our labyrinth with walls, paths, guard and player
    sprites_dict = {"wall": wall, "sand_path": sand_path,
                    "guard": guard, "mac_gyver": mac_gyver}
    game_labyviewer.display_labyrinth(window, sprites_dict)

    # we display our tools in the labyrinth
    game_labyviewer.display_tools_in_labyrinth(window)

    # we locate the player in the labyrinth
    game_laby.initialize_player_location()

    # we display our dashboard
    game_dashboard.display_dashboard(window, game_tools)

    ## TO DO: sub-function
    x0 = Interface.LABY_ORIGIN[0]
    y0 = Interface.LABY_ORIGIN[1]
    x_player = x0 + (game_player.x_pos * Interface.SPRITE_SIZE)
    y_player = y0 + (game_player.y_pos * Interface.SPRITE_SIZE)

    cont = True
    while cont and game_player.is_alive:
        for event in pygame.event.get():
            # we update the authorized movements for the player
            game_laby.authorize_player_movements()
            if event.type == QUIT:
                cont = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    cont = False
                if event.key == K_UP:
                    if game_player.authorized_movements["up"]:
                        # we erase the player sprite
                        window.blit(sand_path, (x_player, y_player))
                        # we update the player location in the labyrinth
                        game_player.move("up")
                if event.key == K_DOWN:
                    if game_player.authorized_movements["down"]:
                        # we erase the player sprite
                        window.blit(sand_path, (x_player, y_player))
                        # we update the player location in the labyrinth
                        game_player.move("down")
                if event.key == K_LEFT:
                    if game_player.authorized_movements["left"]:
                        # we erase the player sprite
                        window.blit(sand_path, (x_player, y_player))
                        # we update the player location in the labyrinth
                        game_player.move("left")
                if event.key == K_RIGHT:
                    if game_player.authorized_movements["right"]:
                        # we erase the player sprite
                        window.blit(sand_path, (x_player, y_player))
                        # we update the player location in the labyrinth
                        game_player.move("right")
                # we update the player location on the screen
                x_player = x0 + (game_player.x_pos * Interface.SPRITE_SIZE)
                y_player = y0 + (game_player.y_pos * Interface.SPRITE_SIZE)
                window.blit(mac_gyver, (x_player, y_player))
                # we update the dashboard
                game_dashboard.display_dashboard(window, game_tools)
                # screen refresh
                pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
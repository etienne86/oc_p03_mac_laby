#! /usr/bin/env python3
# coding: utf-8

"""Please execute this file with Python to launch a labyrinth game."""

import os

import pygame
from pygame.locals import *

from interface import Interface
from labyrinth import Labyrinth
from labyviewer import LabyViewer
from dashboard import Dashboard


def game_loop(window, game_interface, game_laby, game_player, sprites_dict):
    """This function is the main loop used in game module."""

    # we enable key repeat
    pygame.key.set_repeat(200, 40)

    # we set some variables:
    # graphic variables
    x_0 = Interface.LABY_ORIGIN[0]
    y_0 = Interface.LABY_ORIGIN[1]
    # labyrinth variables
    x_player = x_0 + (game_player.x_pos * Interface.SPRITE_SIZE)
    y_player = y_0 + (game_player.y_pos * Interface.SPRITE_SIZE)

    cont = True
    while cont and game_player.is_alive and not game_player.wins:
        for event in pygame.event.get():
            # we update the authorized movements for the player
            game_laby.authorize_player_movements()
            if event.type == QUIT:
                cont = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    cont = False
                elif event.key == K_UP:
                    if game_player.authorized_movements["up"]:
                        # we erase the player sprite
                        window.blit(sprites_dict["sand_path"],
                                    (x_player, y_player))
                        # we update the player location in the labyrinth
                        game_player.move("up")
                elif event.key == K_DOWN:
                    if game_player.authorized_movements["down"]:
                        # we erase the player sprite
                        window.blit(sprites_dict["sand_path"],
                                    (x_player, y_player))
                        # we update the player location in the labyrinth
                        game_player.move("down")
                elif event.key == K_LEFT:
                    if game_player.authorized_movements["left"]:
                        # we erase the player sprite
                        window.blit(sprites_dict["sand_path"],
                                    (x_player, y_player))
                        # we update the player location in the labyrinth
                        game_player.move("left")
                elif event.key == K_RIGHT:
                    if game_player.authorized_movements["right"]:
                        # we erase the player sprite
                        window.blit(sprites_dict["sand_path"],
                                    (x_player, y_player))
                        # we update the player location in the labyrinth
                        game_player.move("right")
                # we check if the player find a tool
                game_laby.find_tool()
                # we check if the player wins or loses
                game_laby.analyze_game_status()
                # we update the player location on the screen
                x_player = x_0 + (game_player.x_pos * Interface.SPRITE_SIZE)
                y_player = y_0 + (game_player.y_pos * Interface.SPRITE_SIZE)
                window.blit(sprites_dict["mac_gyver"], (x_player, y_player))
                # we update the dashboard
                game_interface.display_dashboard(window, game_laby.tools)
                # screen refresh
                pygame.display.flip()

    if game_player.wins or not game_player.is_alive:
        if game_player.wins:
            game_interface.dashboard.logic_light = "green"
        elif not game_player.is_alive:
            game_interface.dashboard.logic_light = "red"
        game_interface.display_dashboard(window, game_laby.tools)
        pygame.display.flip()
        cont2 = True
        while cont2:
            for event in pygame.event.get():
                if event.type == QUIT:
                    cont2 = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        cont2 = False


def main():
    """This function is the main function to be executed to play the game."""

    pygame.init()

    # we build the labyrinth, with the player and the tools to be found
    csv_path = os.path.join("data", "grid.csv")
    game_laby = Labyrinth(LabyViewer.LABY_SIZE, LabyViewer.LABY_SIZE, csv_path)
    game_laby.initialize_player_location()
    game_player = game_laby.player
    game_tools = game_laby.tools

    # we initialize the main window with our game interface
    window = pygame.display.set_mode((Interface.SCREEN_WIDTH,
                                      Interface.SCREEN_HEIGHT))
    game_back = pygame.image.load("sprites\\backs\\blue_sky.png").convert()
    game_labyviewer = LabyViewer(game_laby)
    game_dashboard = Dashboard("game")
    game_interface = Interface(game_back, game_labyviewer, game_dashboard)
    window.blit(game_back, Interface.SCREEN_ORIGIN)

    # we load our sprites
    mac_gyver = pygame.image.load("sprites\\laby\\mac_gyver.png").convert()
    mac_gyver.set_colorkey((255, 255, 255))  # set white as transparent
    sand_path = pygame.image.load("sprites\\laby\\path.png").convert()
    wall = pygame.image.load("sprites\\laby\\wall.png").convert()
    guard = pygame.image.load("sprites\\laby\\guard.png").convert()
    guard.set_colorkey((255, 255, 255))  # set white as transparent

    # we improve our window
    mac_g_a = pygame.image.load("sprites\\laby\\mac_gyver.png").convert_alpha()
    mac_g_a.set_colorkey((255, 255, 255))  # set white as transparent
    pygame.display.set_icon(mac_g_a)
    pygame.display.set_caption("Mac Gyverinth - game mode - by etienne86")
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
    game_interface.display_dashboard(window, game_tools)

    # we execute our game loop
    game_loop(window, game_interface, game_laby, game_player, sprites_dict)

    pygame.quit()


if __name__ == "__main__":
    main()

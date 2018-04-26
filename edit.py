#! /usr/bin/env python3
# coding: utf-8

"""Please execute this file with Python to edit the labyrinth map."""

import os

import pygame
from pygame.locals import *

from interface import Interface
from labyrinth import Labyrinth
from labyviewer import LabyViewer
from dashboard import Dashboard


def edit_loop(window, edit_interface, edit_laby, sprites_dict, csv_path):
    """This function is the main loop used in edit module.
    We assume that pygame has been initialized."""

    # we enable key repeat
    pygame.key.set_repeat(200, 40)
    # we set some variables
    db_origin = Interface.DASHBOARD_ORIGIN
    laby_origin = Interface.LABY_ORIGIN
    side = Interface.SPRITE_SIZE
    select_spr = ""
    green_tick = pygame.image.load("sprites\\edit\\green_tick.png").convert()
    red_cross = pygame.image.load("sprites\\edit\\red_cross.png").convert()
    # we display a red cross next to each item
    for i in range(4):
        window.blit(red_cross, (db_origin[0] + side * 4,
                                db_origin[1] + ((2*i + (1 - 0.5*i)) * side)))
    # screen refresh
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type not in [QUIT, KEYDOWN, MOUSEBUTTONDOWN]:
                continue
            elif (event.type == KEYDOWN and event.key == K_ESCAPE)\
                    or event.type == QUIT:
                exit()
            # if we click left
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                x_click = event.pos[0]
                y_click = event.pos[1]
                # if we select a sprite
                if x_click >= db_origin[0] and x_click < db_origin[0] + side\
                        and select_spr == "":
                    # if we click on the "Wall" sprite
                    if y_click >= db_origin[1] + side * 1\
                            and y_click < db_origin[1] + side * 2:
                        select_spr = "wall"
                        window.blit(green_tick,
                                    (db_origin[0] + side * 4,
                                     db_origin[1] + side * 1))
                    # if we click on the "Path" sprite
                    elif y_click >= db_origin[1] + side * 2.5\
                            and y_click < db_origin[1] + side * 3.5:
                        select_spr = "sand_path"
                        window.blit(green_tick,
                                    (db_origin[0] + side * 4,
                                     db_origin[1] + side * 2.5))
                    # if we click on the "Start" sprite (m_gyver)
                    elif y_click >= db_origin[1] + side * 4\
                            and y_click < db_origin[1] + side * 5:
                        select_spr = "m_gyver"
                        window.blit(green_tick,
                                    (db_origin[0] + side * 4,
                                     db_origin[1] + side * 4))
                    # if we click on the "Exit" sprite (guard)
                    elif y_click >= db_origin[1] + side * 5.5\
                            and y_click < db_origin[1] + side * 6.5:
                        select_spr = "guard"
                        window.blit(green_tick,
                                    (db_origin[0] + side * 4,
                                     db_origin[1] + side * 5.5))
                    # screen refresh
                    pygame.display.flip()
                # if we want to replace a sprite in the map
                elif x_click >= laby_origin[0]\
                        and x_click < laby_origin[0] + side * edit_laby.width\
                        and y_click >= laby_origin[1]\
                        and y_click < laby_origin[1] + side * edit_laby.height:
                    sprites_int = {"sand_path": 0, "wall": 1,
                                   "guard": 2, "m_gyver": 3}
                    # if a sprite is selected
                    if select_spr != "":
                        # we update the labyrinth
                        edit_laby.grid.iloc[int((y_click -\
                                                 laby_origin[1]) / side),
                                            int((x_click -\
                                                 laby_origin[0]) / side)]\
                                            = sprites_int[select_spr]
                        # we save the labyrinth
                        edit_laby.save_grid_to_file(csv_path)
                        # we update the labyrinth viewer
                        # this first blit is useful for "m_gyver" and "guard"
                        window.blit(sprites_dict["sand_path"],
                                    (int((x_click - laby_origin[0]) / side)\
                                            * side + laby_origin[0],
                                     int((y_click - laby_origin[1]) / side)\
                                            * side + laby_origin[1]))
                        # this second blit is the "main" blit
                        window.blit(sprites_dict[select_spr],
                                    (int((x_click - laby_origin[0]) / side)\
                                            * side + laby_origin[0],
                                     int((y_click - laby_origin[1]) / side)\
                                            * side + laby_origin[1]))

            # if we click right
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                # we unselect the selected sprite
                select_spr = ""
                # we erase the "green tick"
                window.blit(red_cross,
                            (db_origin[0] + side * 4,
                             db_origin[1] + side * 1))
                window.blit(red_cross,
                            (db_origin[0] + side * 4,
                             db_origin[1] + side * 2.5))
                window.blit(red_cross,
                            (db_origin[0] + side * 4,
                             db_origin[1] + side * 4))
                window.blit(red_cross,
                            (db_origin[0] + side * 4,
                             db_origin[1] + side * 5.5))
            # we analyze the map to update the logic light in the dashboard
            if edit_laby.analyze_playability():
                edit_interface.dashboard.logic_light = "green"
            else:
                edit_interface.dashboard.logic_light = "red"
            # we display our dashboard
            edit_interface.display_dashboard(window)
            # screen refresh
            pygame.display.flip()


def main():
    """This function is the main function to be executed to edit the map."""

    pygame.init()

    # we build the labyrinth
    csv_path = os.path.join("data", "grid.csv")
    edit_laby = Labyrinth(LabyViewer.LABY_WIDTH, LabyViewer.LABY_HEIGHT,
                          csv_path)

    # we initialize the main window with our game interface
    window = pygame.display.set_mode((Interface.SCREEN_WIDTH,
                                      Interface.SCREEN_HEIGHT))
    edit_back = pygame.image.load("sprites\\backs\\sea.png").convert()
    edit_labyviewer = LabyViewer(edit_laby)
    edit_dashboard = Dashboard("edit")
    edit_interface = Interface(edit_back, edit_labyviewer, edit_dashboard)
    window.blit(edit_back, Interface.SCREEN_ORIGIN)

    # we load our sprites
    m_gyver = pygame.image.load("sprites\\laby\\m_gyver.png").convert()
    m_gyver.set_colorkey((255, 255, 255))  # set white as transparent
    sand_path = pygame.image.load("sprites\\laby\\path.png").convert()
    wall = pygame.image.load("sprites\\laby\\wall.png").convert()
    guard = pygame.image.load("sprites\\laby\\guard.png").convert()
    guard.set_colorkey((255, 255, 255))  # set white as transparent

    # we improve our window
    mac_g_a = pygame.image.load("sprites\\laby\\m_gyver.png").convert_alpha()
    mac_g_a.set_colorkey((255, 255, 255))  # set white as transparent
    pygame.display.set_icon(mac_g_a)
    pygame.display.set_caption("Mac Gyverinth - edit mode - by etienne86")
    pygame.display.flip()

    # we display our labyrinth with walls, paths, guard and player
    sprites_dict = {"wall": wall, "sand_path": sand_path,
                    "guard": guard, "m_gyver": m_gyver}
    edit_labyviewer.display_labyrinth(window, sprites_dict)

    # we display our dashboard
    edit_interface.display_dashboard(window)

    # we execute our edit loop
    edit_loop(window, edit_interface, edit_laby, sprites_dict, csv_path)

    pygame.quit()


if __name__ == "__main__":
    main()

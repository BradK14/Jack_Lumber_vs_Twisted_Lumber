"""
Jack Lumber vs Twisted Lumber.py
This is the main file used to run the game.  The game is ran with the help of pygame.
"""

import pygame
import MapGenerator as mg
import GameFunctions as gf
from pygame.sprite import Group
from Classes.Screen import Screen
from Classes.UserInterface import UserInterface
from Classes.WorldSettings import WorldSettings
from Classes.JackLumber import JackLumber


def vs_Twisted_Lumber():
    # Initialize pygame modules
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)

    # Initialize the world settings and load assets
    w_settings = WorldSettings()

    # Create the Screen
    screen = Screen(w_settings)
    pygame.display.set_caption('Jack Lumber vs. Twisted Lumber')

    # Create the user interface
    UI = UserInterface(w_settings)

    # Create the playable character Jack Lumber
    jack = JackLumber(w_settings, 0, 0, False)

    # Create containers for each asset needed
    enemies = Group()
    bg_blocks = Group()
    surfaces = Group()
    ranged_attacks = Group()

    # Create the map
    mg.load_map(w_settings, bg_blocks, surfaces, jack, enemies)

    # Create our timers
    fps_timer = pygame.time.Clock()  # This clock specifically used for frame rate
    cur_time = 0
    
    # Begin the main loop for the game
    run = True
    while run:
        if run:
            cur_time = pygame.time.get_ticks()
            run = gf.check_events(joystick, jack)
            gf.update_character_inputs(cur_time, jack)
            gf.update_ai(cur_time, jack, enemies)
            gf.update_positions(w_settings, surfaces, ranged_attacks, jack, enemies)
            gf.update_animations(cur_time, ranged_attacks, jack, enemies)
            gf.update_screen(screen, UI, bg_blocks, surfaces, ranged_attacks, jack, enemies)
        fps_timer.tick(w_settings.fps)

    # End game
    pygame.quit()


# Run the game
vs_Twisted_Lumber()

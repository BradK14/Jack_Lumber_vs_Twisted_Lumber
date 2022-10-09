"""
Jack Lumber vs Twisted Lumber.py
This is the main file used to run the game.  The game is ran with the help of pygame.
"""

import pygame
import MapGenerator as mg
import GameFunctions as gf
from pygame.sprite import Group
from Classes.Controller import Controller
from Classes.Screen import Screen
from Classes.UserInterface import UserInterface
from Classes.WorldSettings import WorldSettings
from Classes.JackLumber import JackLumber
from Classes.TwistedLumber import TwistedLumber


def vs_Twisted_Lumber():
    # Initialize pygame modules
    pygame.init()
    pygame.joystick.init()

    # Find if there is a controller being used
    if pygame.joystick.get_count() > 0:
        joystick = Controller(pygame.joystick.Joystick(0))
    else:
        joystick = Controller()

    # Initialize the world settings and load assets
    w_settings = WorldSettings()

    # Create the Screen
    screen = Screen(w_settings)
    pygame.display.set_caption('Jack Lumber vs. Twisted Lumber')

    # Create the user interface
    UI = UserInterface(w_settings)

    # Create the playable character Jack Lumber
    jack = JackLumber(w_settings, 0, 0, False)

    # Create a boss for him to fight
    boss = TwistedLumber(w_settings, 0, 0, True)

    # Create containers for each asset needed
    enemies = Group()
    enemies.add(boss)  # Immediately include the boss
    bg_blocks = Group()
    surfaces = Group()
    ranged_attacks = Group()
    leaves = Group()

    # Create the map
    mg.load_map(w_settings, bg_blocks, surfaces, jack, boss)

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
            gf.update_ai(cur_time, leaves, jack, enemies)
            gf.update_positions(w_settings, surfaces, ranged_attacks, leaves, jack, enemies, cur_time)
            gf.update_animations(cur_time, ranged_attacks, jack, enemies)
            gf.update_screen(screen, UI, bg_blocks, surfaces, ranged_attacks, leaves, jack, boss, enemies)
        fps_timer.tick(w_settings.fps)

    # End game
    pygame.quit()


# Run the game
vs_Twisted_Lumber()

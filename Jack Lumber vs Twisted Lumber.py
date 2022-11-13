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
    #boss = TwistedLumber(w_settings, 0, 0, True)
    boss = None

    # Create containers for each asset needed
    enemies = Group()
    #enemies.add(boss)  # Immediately include the boss
    bg_blocks = Group()
    surfaces = Group()
    background = pygame.Surface([w_settings.screen_width, w_settings.screen_height])
    ranged_attacks = Group()
    leaves = Group()

    # Create the map
    mg.load_map_start(w_settings, bg_blocks, surfaces, background, jack)
    in_start_area = True
    game_over = False

    # Create our timers
    fps_timer = pygame.time.Clock()  # This clock specifically used for frame rate
    cur_time = 0
    last_frame = 0
    new_frame = 0
    paused = False
    toggle_pause = False
    pause_already_toggled = False
    
    # Begin the main loop for the game
    run = True
    while run:
        if run:
            last_frame = new_frame
            new_frame = pygame.time.get_ticks()
            run, ready_to_load_next_area, toggle_pause, pause_already_toggled = gf.check_events(joystick, jack, in_start_area, game_over, toggle_pause, pause_already_toggled)
            if toggle_pause:
                toggle_pause = False
                if paused:
                    paused = False
                else:
                    paused = True
            elif ready_to_load_next_area:
                in_start_area, boss = gf.load_next_area(w_settings, in_start_area, jack, enemies, ranged_attacks, leaves)
                game_over = False
            if not paused and not game_over:
                cur_time += new_frame - last_frame
                time_passed = new_frame - last_frame
                gf.update_character_inputs(cur_time, time_passed, jack)
                gf.update_ai(cur_time, time_passed, leaves, jack, enemies)
                gf.update_positions(w_settings, surfaces, ranged_attacks, leaves, jack, enemies, cur_time, time_passed)
                gf.update_animations(cur_time, ranged_attacks, jack, enemies)
                game_over = gf.update_screen(screen, in_start_area, UI, background, ranged_attacks, leaves, jack, boss, enemies)
                if not in_start_area:
                    game_over = gf.check_for_game_over(screen, UI, jack, boss)
        fps_timer.tick(w_settings.fps)

    # End game
    pygame.quit()


# Run the game
vs_Twisted_Lumber()

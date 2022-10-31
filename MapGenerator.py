"""
MapGenerator.py
This file contains functions that handle the creation and placement of blocks, background, characters, and whatever else that is needed in a level.
The first half is helper functions that make map creation easier.
The second half is for functions used to create maps.
"""

import pygame
from Classes.TwistedLumber import TwistedLumber
from Classes.BackgroundBlock import BackgroundBlock
from Classes.Surface import Surface


""" Helper functions """
def create_bg_blocks(w_settings, bg_blocks, x, y, width, height):
    for w in range(width):
        for h in range(height):
            bg_blocks.add(BackgroundBlock(w_settings, x + (w * w_settings.BackgroundBlock_width), y + (h * w_settings.BackgroundBlock_height)))


""" Maps """
# Map 1
def load_map_start(w_settings, bg_blocks, surfaces, jack):
    # Background
    create_bg_blocks(w_settings, bg_blocks, 0, 0, 60, 34)

    # Foreground
    surfaces.add(Surface(w_settings, 0, 1016, 60, 2))  # Floor
    surfaces.add(Surface(w_settings, 0, 0, 60, 2))  # Ceiling
    surfaces.add(Surface(w_settings, -64, 64, 4, 30))  # Left wall
    surfaces.add(Surface(w_settings, 1856, 64, 4, 30))  # Right wall

    # Position Jack Lumber
    jack.x = w_settings.buom * 8
    jack.y = 1016 - w_settings.JL_height
    jack.rect.x = int(jack.x)
    jack.rect.y = int(jack.y)

def reload_map_start(w_settings, jack):
    # Position Jack Lumber
    jack.health = w_settings.JL_health
    jack.facing_left = False
    jack.x = w_settings.buom * 8
    jack.y = 1016 - w_settings.JL_height
    jack.rect.x = int(jack.x)
    jack.rect.y = int(jack.y)

# Map 2 (Keeps the block set-up from Map 1 but repositions the boss enemy and Jack Lumber
def load_map_vs_twisted_lumber(w_settings, jack, boss):
    # Position Jack Lumber
    jack.health = w_settings.JL_health
    jack.facing_left = False
    jack.x = w_settings.buom * 8
    jack.y = 1016 - w_settings.JL_height
    jack.rect.x = int(jack.x)
    jack.rect.y = int(jack.y)

    # Position the Boss
    boss.health = w_settings.TL_health
    boss.x = 1856 - (w_settings.TL_width * 2)
    boss.y = 1016 - w_settings.TL_height
    boss.rect.x = int(boss.x)
    boss.rect.y = int(boss.y)

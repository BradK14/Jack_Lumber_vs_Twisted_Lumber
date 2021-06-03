"""
MapGenerator.py
This file contains functions that handle the creation and placement of blocks, background, characters, and whatever else that is needed in a level.
The first half is helper functions that make map creation easier.
The second half is for functions used to create maps.
"""

import pygame
from Classes.BackgroundBlock import BackgroundBlock
from Classes.Surface import Surface


# Helper functions
def create_bg_blocks(w_settings, bg_blocks, x, y, width, height):
    for w in range(width):
        for h in range(height):
            bg_blocks.add(BackgroundBlock(w_settings, x + (w * w_settings.BackgroundBlock_width), y + (h * w_settings.BackgroundBlock_height)))


# Maps
# Map 1
def load_map(w_settings, bg_blocks, surfaces, jack):
    # Background
    create_bg_blocks(w_settings, bg_blocks, 0, 0, 60, 34)

    # Foreground
    surfaces.add(Surface(w_settings, 0, 1016, 60, 2))  # Floor
    surfaces.add(Surface(w_settings, 0, 0, 60, 2))  # Ceiling
    surfaces.add(Surface(w_settings, 0, 64, 2, 30))  # Left wall
    surfaces.add(Surface(w_settings, 1856, 64, 2, 30))  # Right wall

    # Position Jack Lumber
    jack.x = 300
    jack.y = 300
    jack.rect.x = 300
    jack.rect.y = 300

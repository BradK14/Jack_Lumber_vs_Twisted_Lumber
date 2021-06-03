"""
Surface.py
This file contains the class for Surface.  Surfaces are pieces of geometry used for level design.
Characters should be able to interact with surfaces in ways such as standing on them or bumping into them.
The purpose of these surfaces, rather than just using the blocks themselves is to minimize confusion for the 
collision detection by using one large hit box instead of many.
"""

import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from Classes.Block import Block


class Surface(Sprite):
    def __init__(self, w_settings, x, y, width, height):
        super(Surface, self).__init__()

        # Create a group for the blocks
        self.blocks = Group()

        # Create a grid of blocks starting at the x, y position, in a grid based on width and height
        for w in range(width):
            for h in range(height):
                self.blocks.add(Block(w_settings, x + (w * w_settings.GrassyBlock_width), y + (h * w_settings.GrassyBlock_height)))

        # Save the position
        self.x = x
        self.y = y

        # The total width and height are based on the blocks
        self.width = width * w_settings.GrassyBlock_width
        self.height = height * w_settings.GrassyBlock_height

        # Make one hit box for the entire collection of blocks, so they act as one surface
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # There is no image as we are displaying the blocks

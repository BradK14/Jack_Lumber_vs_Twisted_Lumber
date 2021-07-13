"""
TwistedLumber.py
This file contains the class for TwistedLumber.  This is the enemy in the game.  Everything defining his ai is found here.
"""

import pygame
from Classes.Character import Character


class TwistedLumber(Character):
    def __init__(self, w_settings, x, y, facing_left):
        super(TwistedLumber, self).__init__(w_settings, x, y, facing_left)

        # Apply constants from w_settings
        self.width = self.w_settings.TL_width
        self.height = self.w_settings.TL_height

        # Set up the image and rect
        if self.facing_left:
            self.image = self.w_settings.TL_left_image
        else:
            self.image = self.w_settings.TL_right_image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

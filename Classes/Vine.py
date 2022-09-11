"""
Vine.py
This file contains the class for Vine.  Vines are used by Twisted Lumber to attach to a surface
"""

import pygame
from pygame.sprite import Sprite


class Vine(Sprite):
    def __init__(self, w_settings, x, y):
        super(Vine, self).__init__()

        # Save passed in information and apply constants from w_settings
        self.w_settings = w_settings
        self.x = x
        self.y = y

        # Set up the image and rect
        self.image = self.w_settings.TL_vine_image
        self.rect = pygame.Rect(self.x, self.y, self.w_settings.TL_vine_width, self.w_settings.TL_vine_height)

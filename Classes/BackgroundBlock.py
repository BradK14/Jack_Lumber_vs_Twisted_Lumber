"""
BackgroundBlock.py
This file contains the class BackgroundBlock.  BackgroundBlock is used purely for decoration in the game and should have no effect on characters.
"""

import pygame
from pygame.sprite import Sprite


class BackgroundBlock(Sprite):
    def __init__(self, w_settings, x, y):
        super(BackgroundBlock, self).__init__()

        # Save passed in information and apply constants from w_settings
        self.w_settings = w_settings
        self.x = x
        self.y = y

        # Set up the image and rect
        self.image = self.w_settings.BackgroundBlock_image
        self.rect = pygame.Rect(self.x, self.y, self.w_settings.BackgroundBlock_width, self.w_settings.BackgroundBlock_height)
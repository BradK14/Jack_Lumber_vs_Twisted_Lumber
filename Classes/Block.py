"""
Block.py
This file contains the class for Block.  Blocks are interactable surfaces that the characters can stand on.
"""

import pygame
from pygame.sprite import Sprite


class Block(Sprite):
    def __init__(self, w_settings, x, y):
        super(Block, self).__init__()

        # Save passed in information and apply constants from w_settings
        self.w_settings = w_settings
        self.x = x
        self.y = y

        # Set up the image and rect
        self.image = self.w_settings.GrassyBlock_image
        self.rect = pygame.Rect(self.x, self.y, self.w_settings.GrassyBlock_width, self.w_settings.GrassyBlock_height)
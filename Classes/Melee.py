"""
Melee.py
This file contains the class Melee.  Melee is to be used within the JackLumber class.  It represents his melee attack.
"""

import pygame
from pygame.sprite import Sprite
from Classes.Animation import Animation


class Melee(Sprite):
    def __init__(self, charged):
        super(Melee, self).__init__()

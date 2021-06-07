"""
Melee.py
This file contains the class Melee.
Melee is to be used within the JackLumber class.  It represents his melee attack.
"""

import pygame
from pygame.sprite import Sprite
from Classes.Animation import Animation


class Melee(Sprite):
    def __init__(self, w_settings, jack_rect, facing_left):
        super(Melee, self).__init__()
        self.w_settings = w_settings
        self.facing_left = facing_left

        # Set up for these variables is different with child class
        self.width = 0
        self.height = 0
        self.anim = None

        self.set_up()

        # Position the attack relative to Jack Lumber's position
        if self.facing_left:
            self.x = jack_rect.centerx - self.width
        else:
            self.x = jack_rect.centerx
        self.y = int(jack_rect.centery - self.height / 2)

        # Set up the rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def set_up(self):
        self.width = self.w_settings.JL_melee_width
        self.height = self.w_settings.JL_melee_height

        self.anim = Animation(self.w_settings.JL_melee_left_anim,
                              self.w_settings.JL_melee_anim_size,
                              self.w_settings.JL_melee_anim_rates,
                              self.w_settings.JL_melee_right_anim)

    def reposition(self, jack_rect, facing_left):
        self.facing_left = facing_left

        if self.facing_left:
            self.x = jack_rect.centerx - self.width
        else:
            self.x = jack_rect.centerx
        self.y = int(jack_rect.centery - self.height / 2)

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update_anim(self, cur_time):
        self.image = self.anim.play_once_var_dir(cur_time, self.facing_left)

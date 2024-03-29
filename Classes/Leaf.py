"""
Leaf.py
This file contains the class Leaf
Leaf is used to define the leaf attacks generated by Twisted Lumber
When no child class is used leaves fall slowly to the bottom of the screen
"""

import pygame
from pygame.sprite import Sprite
from Classes.Delay import Delay

class Leaf(Sprite):
    def __init__(self, w_settings, x, y, facing_left, cur_time, start_angle=None):
        super(Leaf, self).__init__()
        # Saving information passed in
        self.w_settings = w_settings
        self.x = x
        self.y = y
        self.facing_left = facing_left
        self.damage = self.w_settings.TL_leaf_damage

        # Create rect and image
        self.rect = pygame.Rect(self.x, self.y, self.w_settings.TL_leaf_width, self.w_settings.TL_leaf_height)
        if facing_left:
            self.image = self.w_settings.TL_leaf_left_image
        else:
            self.image = self.w_settings.TL_leaf_right_image

        # Variable to save current velocity
        self.y_vel = 0

        # A delay to slow down the leaf initially
        self.init_delay = Delay(self.w_settings.TL_slow_leaf_period)
        self.init_delay.begin(cur_time)

        # Variables to check if the leaf needs to be deleted
        self.off_bottom = False
        self.off_top = False
        self.off_left = False
        self.off_right = False

    def update_pos(self, cur_time, time_passed):
        if self.init_delay.is_active(cur_time):
            self.y_vel += (self.w_settings.fall_acceleration * time_passed) / 32
        else:
            self.y_vel += (self.w_settings.fall_acceleration * time_passed) / 16
        self.y += self.y_vel
        self.rect.y = int(self.y)

        if self.rect.top > self.w_settings.screen_height:
            self.off_bottom = True

    def ready_to_delete(self):
        if self.off_bottom:
            return True
        return False

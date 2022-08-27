"""
TwistedLumber.py
This file contains the class for TwistedLumber.  This is the enemy in the game.  Everything defining his ai is found here.
"""

import pygame
from Classes.Character import Character
from Classes.Delay import Delay
from random import seed
from random import randint

seed(1)

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

        # Set up delays
        self.wait_delay = Delay(self.w_settings.TL_wait_period)
        self.jump_delay = Delay(self.w_settings.TL_jump_period)
        self.cur_delay = None

        # States
        self.jumping = False
        if self.facing_left:
            self.jump_dir = -1
        else:
            self.jump_dir = 1

    # Update position
    def update_pos(self):
        if self.jumping and not self.grounded:
            self.x += self.w_settings.TL_x_vel * self.jump_dir
            self.rect.x = int(self.x)
        else:
            self.jumping = False

        self.y_velocity += self.w_settings.fall_acceleration
        self.y += self.y_velocity
        self.rect.y = int(self.y)

    # Set the image in use
    def update_animation(self):
        if self.facing_left:
            self.image = self.w_settings.TL_left_image
        else:
            self.image = self.w_settings.TL_right_image

    # Helper functions to check if our general delay variables are active
    def cur_delay_is_active(self, cur_time):
        if self.cur_delay is not None:
            if self.cur_delay.is_active(cur_time):
                return True
        return False

    def decide_next_move(self, cur_time, jack = None):
        if self.grounded:  # Can only begin a new action while touching the ground
            if not self.cur_delay_is_active(cur_time):
                if self.cur_delay is not None:
                    self.cur_delay.reset()

                # Face towards Jack
                if jack is not None:
                    if jack.x < self.x:
                        self.facing_left = True
                    else:
                        self.facing_left = False

                # Choose an action at random
                randchoice = randint(1, 100)
                if randchoice < 51:  # 50% chance to do nothing
                    self.cur_delay = self.wait_delay
                    self.wait()
                elif randchoice >= 51:  # 50% chance to jump towards Jack
                    self.cur_delay = self.jump_delay
                    self.jump(jack)

                self.cur_delay.begin(cur_time)

    def wait(self):
        pass

    def jump(self, jack):
        self.jumping = True
        self.grounded = False
        self.y_velocity += self.w_settings.TL_init_jump_vel

        if self.facing_left:
            self.jump_dir = -1
        else:
            self.jump_dir = 1

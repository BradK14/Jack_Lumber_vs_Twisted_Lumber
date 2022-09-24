"""
Ranged.py
This file contains the class Ranged.
Ranged is used to define Jack Lumber's ranged attack
"""

import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from Classes.Animation import Animation


class Ranged(Sprite):
    def __init__(self, w_settings, jack_rect, facing_left):
        super(Ranged, self).__init__()
        self.w_settings = w_settings
        self.facing_left = facing_left

        self.width = 0
        self.height = 0
        self.damage = 0
        self.anim = None

        self.set_up()

        if self.facing_left:
            self.x = jack_rect.centerx - self.width
        else:
            self.x = jack_rect.centerx
        self.y = int(jack_rect.centery - self.height / 2)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Keep a list of enemies already damaged by this attack
        self.enemies = Group()

    def set_up(self):
        self.width = self.w_settings.JL_ranged_width
        self.height = self.w_settings.JL_ranged_height
        self.damage = self.w_settings.JL_ranged_damage

        self.anim = Animation(self.w_settings.JL_ranged_left_anim,
                              self.w_settings.JL_ranged_anim_size,
                              self.w_settings.JL_ranged_anim_rates,
                              self.w_settings.JL_ranged_right_anim)

    def damage_once(self, enemy):
        do_damage = True
        for e in self.enemies:
            if enemy is e:
                do_damage = False
                break

        if do_damage:
            enemy.health -= self.damage
            self.enemies.add(enemy)

    def update_position(self):
        if self.facing_left:
            self.x += self.w_settings.JL_ranged_vel * -1
        else:
            self.x += self.w_settings.JL_ranged_vel
        self.rect.x = int(self.x)

    def update_animation(self, cur_time):
        self.image = self.anim.play_var_dir(cur_time, self.facing_left)

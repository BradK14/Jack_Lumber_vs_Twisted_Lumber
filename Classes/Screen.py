"""
Screen.py
This file contains the class Screen.  This class handles the creation and management of displaying everything to the screen.
"""

import pygame


class Screen(object):
    def __init__(self, w_settings):
        self.w_settings = w_settings
        self.width = self.w_settings.full_screen_width
        self.height = self.w_settings.full_screen_height
        self.game_width = self.w_settings.screen_width
        self.game_height = self.w_settings.screen_height
        self.full_screen = self.w_settings.full_screen
        self.screen = self.w_settings.screen

    def new_frame(self):
        self.screen.fill((255, 255, 255))

    def blit_obj(self, obj):
        self.screen.blit(obj.image, obj.rect)

    def blit_img_rect(self, image, rect):
        self.screen.blit(image, rect)

    def blit_img(self, image, location):
        self.screen.blit(image, location)

    def display_frame(self):
        self.full_screen.blit(pygame.transform.scale(self.screen, (self.width, self.height)), (0, 0))
        pygame.display.flip()

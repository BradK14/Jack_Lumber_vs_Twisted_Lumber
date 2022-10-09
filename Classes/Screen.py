"""
Screen.py
This file contains the class Screen.  This class handles the creation and management of displaying everything to the screen.
"""

import pygame


class Screen(object):
    def __init__(self, w_settings):
        self.w_settings = w_settings
        self.width = self.w_settings.screen_width
        self.height = self.w_settings.screen_height
        self.full_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.Surface((self.width, self.height))

    def new_frame(self):
        self.screen.fill((255, 255, 255))
        #self.full_screen.fill((255, 255, 255))

    def blit_obj(self, obj):
        self.screen.blit(obj.image, obj.rect)
        #self.full_screen.blit(obj.image, obj.rect)

    def blit_img_rect(self, image, rect):
        self.screen.blit(image, rect)
        #self.full_screen.blit(image, rect)

    def display_frame(self):
        self.full_screen.blit(pygame.transform.scale(self.screen, (self.width, self.height)), (0, 0))
        pygame.display.flip()

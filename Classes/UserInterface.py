"""
UserInterface.py
This file contains the class UserInterface.  UserInterface handles overlays on the screen to provide information to the user.
"""

import pygame


class UserInterface(object):
    def __init__(self, w_settings):
        self.w_settings = w_settings

        # Keep screen proportions handy for anchoring assets
        self.screen_width = self.w_settings.screen_width
        self.screen_height = self.w_settings.screen_height

        # Gather overlay images
        self.charge_M_image = self.w_settings.charge_M_image
        self.charge_R_image = self.w_settings.charge_R_image

        # Gather sizes of images
        self.charge_M_width = self.w_settings.charge_M_width
        self.charge_M_height = self.w_settings.charge_M_height
        self.charge_R_width = self.w_settings.charge_R_width
        self.charge_R_height = self.w_settings.charge_R_height

        # Create a rect for each image at an appropriate location
        # Charge images on the left side of the screen
        self.charge_M_rect = pygame.Rect(self.w_settings.buom, int(self.screen_height / 2 - self.w_settings.buom * 3.5),
                                         self.charge_M_width, self.charge_M_height)
        self.charge_R_rect = pygame.Rect(self.w_settings.buom, int(self.screen_height / 2 - self.w_settings.buom / 2),
                                         self.charge_R_width, self.charge_R_height)

    def display(self, screen, jack):
        if jack.melee_charged:
            self.charge_M_rect.x = jack.rect.x
            self.charge_M_rect.y = jack.rect.y - self.charge_M_height * 2
            screen.blit_img_rect(self.charge_M_image, self.charge_M_rect)

        if jack.ranged_charged:
            self.charge_R_rect.x = jack.rect.right - self.charge_R_width
            self.charge_R_rect.y = jack.rect.y - self.charge_R_height * 2
            screen.blit_img_rect(self.charge_R_image, self.charge_R_rect)


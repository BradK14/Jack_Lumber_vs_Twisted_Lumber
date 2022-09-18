"""
UserInterface.py
This file contains the class UserInterface.  UserInterface handles overlays on the screen to provide information to the user.
"""

import pygame
import math


class UserInterface(object):
    def __init__(self, w_settings):
        self.w_settings = w_settings

        # Keep screen proportions handy for anchoring assets
        self.screen_width = self.w_settings.screen_width
        self.screen_height = self.w_settings.screen_height

        # Gather overlay images
        self.charge_M_image = self.w_settings.charge_M_image
        self.charge_R_image = self.w_settings.charge_R_image
        self.num_0_image = self.w_settings.num_0_image
        self.num_1_image = self.w_settings.num_1_image
        self.num_2_image = self.w_settings.num_2_image
        self.num_3_image = self.w_settings.num_3_image
        self.num_4_image = self.w_settings.num_4_image
        self.num_5_image = self.w_settings.num_5_image
        self.num_6_image = self.w_settings.num_6_image
        self.num_7_image = self.w_settings.num_7_image
        self.num_8_image = self.w_settings.num_8_image
        self.num_9_image = self.w_settings.num_9_image

        # Gather sizes of images
        self.charge_M_width = self.w_settings.charge_M_width
        self.charge_M_height = self.w_settings.charge_M_height
        self.charge_R_width = self.w_settings.charge_R_width
        self.charge_R_height = self.w_settings.charge_R_height
        self.text_width = self.w_settings.text_width
        self.text_height = self.w_settings.text_height

        # Create a rect for each image at an appropriate location
        # Charge images on the left side of the screen
        self.charge_M_rect = pygame.Rect(self.w_settings.buom, int(self.screen_height / 2 - self.w_settings.buom * 3.5),
                                         self.charge_M_width, self.charge_M_height)
        self.charge_R_rect = pygame.Rect(self.w_settings.buom, int(self.screen_height / 2 - self.w_settings.buom / 2),
                                         self.charge_R_width, self.charge_R_height)

        # Main character health numbers (3 to represent percent of health left) on top left of the screen
        dist_from_top_of_screen = int(self.w_settings.buom * 2)
        self.jack_health_1_rect = pygame.Rect(int(self.w_settings.buom / 2), dist_from_top_of_screen,
                                              self.text_width, self.text_height)
        self.jack_health_2_rect = pygame.Rect(self.jack_health_1_rect.right, dist_from_top_of_screen,
                                              self.text_width, self.text_height)
        self.jack_health_3_rect = pygame.Rect(self.jack_health_2_rect.right, dist_from_top_of_screen,
                                              self.text_width, self.text_height)

        # Boss character health numbers on top right of the screen
        self.boss_health_1_rect = pygame.Rect(int(self.screen_width - (self.text_width * 3 + self.w_settings.buom / 2)), dist_from_top_of_screen,
                                              self.text_width, self.text_height)
        self.boss_health_2_rect = pygame.Rect(self.boss_health_1_rect.right, dist_from_top_of_screen,
                                              self.text_width, self.text_height)
        self.boss_health_3_rect = pygame.Rect(self.boss_health_2_rect.right, dist_from_top_of_screen,
                                              self.text_width, self.text_height)

    def display(self, screen, jack, boss):
        # Display Jack's charged states
        if jack.melee_charged:
            self.charge_M_rect.x = jack.rect.x
            self.charge_M_rect.y = jack.rect.y - self.charge_M_height * 2
            screen.blit_img_rect(self.charge_M_image, self.charge_M_rect)

        if jack.ranged_charged:
            self.charge_R_rect.x = jack.rect.right - self.charge_R_width
            self.charge_R_rect.y = jack.rect.y - self.charge_R_height * 2
            screen.blit_img_rect(self.charge_R_image, self.charge_R_rect)

        # Display Jack and the boss' health
        characters = [jack, boss]
        health_rects = [[self.jack_health_1_rect, self.jack_health_2_rect, self.jack_health_3_rect],
                        [self.boss_health_1_rect, self.boss_health_2_rect, self.boss_health_3_rect]]
        for x in range(0, 2):
            health_percent = math.ceil(characters[x].health / characters[x].max_health * 100)
            for y in range(0, 3):
                num = int((health_percent / (10 ** (2 - y))) % 10)
                if num is 1:
                    screen.blit_img_rect(self.num_1_image, health_rects[x][y])
                elif num is 2:
                    screen.blit_img_rect(self.num_2_image, health_rects[x][y])
                elif num is 3:
                    screen.blit_img_rect(self.num_3_image, health_rects[x][y])
                elif num is 4:
                    screen.blit_img_rect(self.num_4_image, health_rects[x][y])
                elif num is 5:
                    screen.blit_img_rect(self.num_5_image, health_rects[x][y])
                elif num is 6:
                    screen.blit_img_rect(self.num_6_image, health_rects[x][y])
                elif num is 7:
                    screen.blit_img_rect(self.num_7_image, health_rects[x][y])
                elif num is 8:
                    screen.blit_img_rect(self.num_8_image, health_rects[x][y])
                elif num is 9:
                    screen.blit_img_rect(self.num_9_image, health_rects[x][y])
                elif y is 0 and health_percent < 100 or y is 1 and health_percent < 10:
                    pass
                else:
                    screen.blit_img_rect(self.num_0_image, health_rects[x][y])

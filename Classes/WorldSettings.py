"""
WorldSettings.py
This file contains the class WorldSettings.  WorldSettings contains the many constants used throughout the program.  It is also used to load in the assets at the beginning of the program.
Much of the program uses the constants found here, so it should be created immediately and passed into most of the functions throughout the program.
"""

import pygame


class WorldSettings(object):
    def __init__(self):
        """Screen size"""
        self.screen_width = 1920
        self.screen_height = 1080

        """Frames per second"""
        self.fps = 60
        self.fps_t = 16 + (2 / 3)  # fps translated to pygame ticks

        """Sizes of everything"""
        # buom stands for the basic unit of measurement used for the sizes of objects in this game
        self.buom = 32

        # Jack Lumber's size
        self.JackLumber_width = self.buom * 2
        self.JackLumber_height = self.JackLumber_width * 2

        # Jack Lumber attack sizes
        self.JackLumber_melee_width = int(self.JackLumber_width / 2)
        self.JackLumber_melee_height = self.JackLumber_height
        self.JackLumber_charged_melee_width = int(self.JackLumber_melee_width * 1.5)
        self.JackLumber_charged_melee_height = int(self.JackLumber_melee_height * 1.5)

        self.JackLumber_ranged_width = self.buom
        self.JackLumber_ranged_height = self.JackLumber_ranged_width
        self.JackLumber_charged_ranged_width = self.JackLumber_ranged_width * 2
        self.JackLumber_charged_ranged_height = self.JackLumber_charged_ranged_width

        # Jack Lumber's charge state indicator sizes
        self.charge_M_width = self.buom
        self.charge_M_height = self.charge_M_width
        self.charge_R_width = self.charge_M_width
        self.charge_R_height = self.charge_M_width
        self.charge_D_width = self.charge_M_width
        self.charge_D_height = self.charge_M_width

        # Block sizes
        self.GrassyBlock_width = self.buom
        self.GrassyBlock_height = self.GrassyBlock_width

        # Background block sizes
        self.BackgroundBlock_width = self.buom
        self.BackgroundBlock_height = self.BackgroundBlock_width

        """Load non-animated images"""
        self.JackLumber_left_image = pygame.transform.scale(pygame.image.load('Images/Jack Lumber.png'), (self.JackLumber_width, self.JackLumber_height))
        self.JackLumber_right_image = pygame.transform.flip(self.JackLumber_left_image, True, False)
        self.JackLumber_jump_left_image = pygame.transform.scale(pygame.image.load('Images/Jack Lumber Jump.png'), (self.JackLumber_width, self.JackLumber_height))
        self.JackLumber_jump_right_image = pygame.transform.flip(self.JackLumber_jump_left_image, True, False)
        self.JackLumber_dash_stage_2_left_image = pygame.transform.scale(pygame.image.load('Images/Jack Lumber invincidash-4.png'), (self.JackLumber_width, self.JackLumber_height))
        self.JackLumber_dash_stage_2_right_image = pygame.transform.flip(self.JackLumber_dash_stage_2_left_image, True, False)

        self.charge_M_image = pygame.transform.scale(pygame.image.load('Images/Charge Display-M.png'), (self.charge_M_width, self.charge_M_height))
        self.charge_R_image = pygame.transform.scale(pygame.image.load('Images/Charge Display-R.png'), (self.charge_R_width, self.charge_R_height))
        self.charge_D_image = pygame.transform.scale(pygame.image.load('Images/Charge Display-D.png'), (self.charge_D_width, self.charge_D_height))

        self.GrassyBlock_image = pygame.transform.scale(pygame.image.load('Images/Grassy Block.png'), (self.GrassyBlock_width, self.GrassyBlock_height))

        self.BackgroundBlock_image = pygame.transform.scale(pygame.image.load('Images/Background Block.png'), (self.BackgroundBlock_width, self.BackgroundBlock_height))

        """Animations (variables for animation sizes just below animation lists)"""
        # Jack Lumber walk animation
        self.JackLumber_walk_left_anim = (pygame.transform.scale(pygame.image.load('Images/Jack Lumber Walking-1.png'),
                                                                 (self.JackLumber_width, self.JackLumber_height)),
                                          pygame.transform.scale(pygame.image.load('Images/Jack Lumber Walking-2.png'),
                                                                 (self.JackLumber_width, self.JackLumber_height)),
                                          pygame.transform.scale(pygame.image.load('Images/Jack Lumber Walking-3.png'),
                                                                 (self.JackLumber_width, self.JackLumber_height)),
                                          pygame.transform.scale(pygame.image.load('Images/Jack Lumber Walking-4.png'),
                                                                 (self.JackLumber_width, self.JackLumber_height)),
                                          pygame.transform.scale(pygame.image.load('Images/Jack Lumber Walking-5.png'),
                                                                 (self.JackLumber_width, self.JackLumber_height)))
        self.JackLumber_walk_right_anim = (pygame.transform.flip(self.JackLumber_walk_left_anim[0], True, False),
                                           pygame.transform.flip(self.JackLumber_walk_left_anim[1], True, False),
                                           pygame.transform.flip(self.JackLumber_walk_left_anim[2], True, False),
                                           pygame.transform.flip(self.JackLumber_walk_left_anim[3], True, False),
                                           pygame.transform.flip(self.JackLumber_walk_left_anim[4], True, False))
        self.JackLumber_walk_anim_size = 5
        self.JackLumber_walk_anim_rates = (90, 90, 90, 90, 90)

        # Jack Lumber dash stage 1 animation
        self.JackLumber_dash_start_left_anim = (pygame.transform.scale(pygame.image.load('Images/Jack Lumber invincidash-1.png'),
                                                                       (self.JackLumber_width, self.JackLumber_height)),
                                                pygame.transform.scale(pygame.image.load('Images/Jack Lumber invincidash-2.png'),
                                                                       (self.JackLumber_width, self.JackLumber_height)),
                                                pygame.transform.scale(pygame.image.load('Images/Jack Lumber invincidash-3.png'),
                                                                       (self.JackLumber_width, self.JackLumber_height)))
        self.JackLumber_dash_start_right_anim = (pygame.transform.flip(self.JackLumber_dash_start_left_anim[0], True, False),
                                                 pygame.transform.flip(self.JackLumber_dash_start_left_anim[1], True, False),
                                                 pygame.transform.flip(self.JackLumber_dash_start_left_anim[2], True, False))
        self.JackLumber_dash_start_anim_size = 3
        self.JackLumber_dash_start_anim_rates = (75, 75, 150)

        # Jack Lumber invincidash stage 2 animation
        self.JackLumber_invincidash_stage_2_left_anim = (pygame.transform.scale(pygame.image.load('Images/Jack Lumber invincidash-5.png'),
                                                                                (self.JackLumber_width, self.JackLumber_height)),
                                                         pygame.transform.scale(pygame.image.load('Images/Jack Lumber invincidash-6.png'),
                                                                                (self.JackLumber_width, self.JackLumber_height)))
        self.JackLumber_invincidash_stage_2_right_anim = (pygame.transform.flip(self.JackLumber_invincidash_stage_2_left_anim[0], True, False),
                                                          pygame.transform.flip(self.JackLumber_invincidash_stage_2_left_anim[1], True, False))
        self.JackLumber_invincidash_stage_2_anim_size = 2
        self.JackLumber_invincidash_stage_2_anim_rates = (90, 90)

        # Jack Lumber final invincidash animation
        self.JackLumber_invincidash_left_anim = (pygame.transform.scale(pygame.image.load('Images/Jack Lumber Invincijump-1.png'),
                                                                        (self.JackLumber_width, self.JackLumber_height)),
                                                 pygame.transform.scale(pygame.image.load('Images/Jack Lumber Invincijump-2.png'),
                                                                        (self.JackLumber_width, self.JackLumber_height)))
        self.JackLumber_invincidash_right_anim = (pygame.transform.flip(self.JackLumber_invincidash_left_anim[0], True, False),
                                                  pygame.transform.flip(self.JackLumber_invincidash_left_anim[1], True, False))
        self.JackLumber_invincidash_anim_size = 2
        self.JackLumber_invincidash_anim_rates = (90, 90)

        # Jack Lumber's melee and charged melee attack animations
        self.JackLumber_melee_right_anim = (pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-1.png'),
                                                                   (self.JackLumber_melee_width,
                                                                    self.JackLumber_melee_height)),
                                            pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-2.png'),
                                                                   (self.JackLumber_melee_width,
                                                                    self.JackLumber_melee_height)),
                                            pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-3.png'),
                                                                   (self.JackLumber_melee_width,
                                                                    self.JackLumber_melee_height)),
                                            pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-4.png'),
                                                                   (self.JackLumber_melee_width,
                                                                    self.JackLumber_melee_height)),
                                            pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-5.png'),
                                                                   (self.JackLumber_melee_width,
                                                                    self.JackLumber_melee_height)),
                                            pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-6.png'),
                                                                   (self.JackLumber_melee_width,
                                                                    self.JackLumber_melee_height)),
                                            pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-7.png'),
                                                                   (self.JackLumber_melee_width,
                                                                    self.JackLumber_melee_height)))
        self.JackLumber_melee_left_anim = (pygame.transform.flip(self.JackLumber_melee_right_anim[0], True, False),
                                           pygame.transform.flip(self.JackLumber_melee_right_anim[1], True, False),
                                           pygame.transform.flip(self.JackLumber_melee_right_anim[2], True, False),
                                           pygame.transform.flip(self.JackLumber_melee_right_anim[3], True, False),
                                           pygame.transform.flip(self.JackLumber_melee_right_anim[4], True, False),
                                           pygame.transform.flip(self.JackLumber_melee_right_anim[5], True, False),
                                           pygame.transform.flip(self.JackLumber_melee_right_anim[6], True, False))
        self.JackLumber_charged_melee_right_anim = (pygame.transform.scale(self.JackLumber_melee_right_anim[0],
                                                                           (self.JackLumber_charged_melee_width,
                                                                            self.JackLumber_charged_melee_height)),
                                                    pygame.transform.scale(self.JackLumber_melee_right_anim[1],
                                                                           (self.JackLumber_charged_melee_width,
                                                                            self.JackLumber_charged_melee_height)),
                                                    pygame.transform.scale(self.JackLumber_melee_right_anim[2],
                                                                           (self.JackLumber_charged_melee_width,
                                                                            self.JackLumber_charged_melee_height)),
                                                    pygame.transform.scale(self.JackLumber_melee_right_anim[3],
                                                                           (self.JackLumber_charged_melee_width,
                                                                            self.JackLumber_charged_melee_height)),
                                                    pygame.transform.scale(self.JackLumber_melee_right_anim[4],
                                                                           (self.JackLumber_charged_melee_width,
                                                                            self.JackLumber_charged_melee_height)),
                                                    pygame.transform.scale(self.JackLumber_melee_right_anim[5],
                                                                           (self.JackLumber_charged_melee_width,
                                                                            self.JackLumber_charged_melee_height)),
                                                    pygame.transform.scale(self.JackLumber_melee_right_anim[6],
                                                                           (self.JackLumber_charged_melee_width,
                                                                            self.JackLumber_charged_melee_height)))
        self.JackLumber_charged_melee_left_anim = (pygame.transform.flip(self.JackLumber_charged_melee_right_anim[0], True, False),
                                                   pygame.transform.flip(self.JackLumber_charged_melee_right_anim[1], True, False),
                                                   pygame.transform.flip(self.JackLumber_charged_melee_right_anim[2], True, False),
                                                   pygame.transform.flip(self.JackLumber_charged_melee_right_anim[3], True, False),
                                                   pygame.transform.flip(self.JackLumber_charged_melee_right_anim[4], True, False),
                                                   pygame.transform.flip(self.JackLumber_charged_melee_right_anim[5], True, False),
                                                   pygame.transform.flip(self.JackLumber_charged_melee_right_anim[6], True, False))
        self.JackLumber_melee_anim_size = 7
        self.JackLumber_melee_anim_rates = (int(self.fps_t), int(self.fps_t), int(self.fps_t), int(self.fps_t),
                                                 int(self.fps_t), int(self.fps_t), int(self.fps_t))

        # Jack Lumber's ranged and charged ranged attack animations
        self.JackLumber_ranged_right_anim = (pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-1.png'),
                                                                   (self.JackLumber_ranged_width,
                                                                    self.JackLumber_ranged_height)),
                                             pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-2.png'),
                                                                    (self.JackLumber_ranged_width,
                                                                     self.JackLumber_ranged_height)),
                                             pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-3.png'),
                                                                    (self.JackLumber_ranged_width,
                                                                     self.JackLumber_ranged_height)),
                                             pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-4.png'),
                                                                    (self.JackLumber_ranged_width,
                                                                     self.JackLumber_ranged_height)),
                                             pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-5.png'),
                                                                    (self.JackLumber_ranged_width,
                                                                     self.JackLumber_ranged_height)),
                                             pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-6.png'),
                                                                    (self.JackLumber_ranged_width,
                                                                     self.JackLumber_ranged_height)),
                                             pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-7.png'),
                                                                    (self.JackLumber_ranged_width,
                                                                     self.JackLumber_ranged_height)),
                                             pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-8.png'),
                                                                    (self.JackLumber_ranged_width,
                                                                     self.JackLumber_ranged_height)))
        self.JackLumber_ranged_left_anim = (pygame.transform.flip(self.JackLumber_ranged_right_anim[0], True, False),
                                            pygame.transform.flip(self.JackLumber_ranged_right_anim[1], True, False),
                                            pygame.transform.flip(self.JackLumber_ranged_right_anim[2], True, False),
                                            pygame.transform.flip(self.JackLumber_ranged_right_anim[3], True, False),
                                            pygame.transform.flip(self.JackLumber_ranged_right_anim[4], True, False),
                                            pygame.transform.flip(self.JackLumber_ranged_right_anim[5], True, False),
                                            pygame.transform.flip(self.JackLumber_ranged_right_anim[6], True, False),
                                            pygame.transform.flip(self.JackLumber_ranged_right_anim[7], True, False))
        self.JackLumber_charged_ranged_right_anim = (pygame.transform.scale(self.JackLumber_ranged_right_anim[0],
                                                                           (self.JackLumber_charged_ranged_width,
                                                                            self.JackLumber_charged_ranged_height)),
                                                     pygame.transform.scale(self.JackLumber_ranged_right_anim[1],
                                                                           (self.JackLumber_charged_ranged_width,
                                                                            self.JackLumber_charged_ranged_height)),
                                                     pygame.transform.scale(self.JackLumber_ranged_right_anim[2],
                                                                           (self.JackLumber_charged_ranged_width,
                                                                            self.JackLumber_charged_ranged_height)),
                                                     pygame.transform.scale(self.JackLumber_ranged_right_anim[3],
                                                                           (self.JackLumber_charged_ranged_width,
                                                                            self.JackLumber_charged_ranged_height)),
                                                     pygame.transform.scale(self.JackLumber_ranged_right_anim[4],
                                                                           (self.JackLumber_charged_ranged_width,
                                                                            self.JackLumber_charged_ranged_height)),
                                                     pygame.transform.scale(self.JackLumber_ranged_right_anim[5],
                                                                           (self.JackLumber_charged_ranged_width,
                                                                            self.JackLumber_charged_ranged_height)),
                                                     pygame.transform.scale(self.JackLumber_ranged_right_anim[6],
                                                                           (self.JackLumber_charged_ranged_width,
                                                                            self.JackLumber_charged_ranged_height)),
                                                     pygame.transform.scale(self.JackLumber_ranged_right_anim[7],
                                                                           (self.JackLumber_charged_ranged_width,
                                                                            self.JackLumber_charged_ranged_height)))
        self.JackLumber_charged_left_anim = (pygame.transform.flip(self.JackLumber_charged_ranged_right_anim[0], True, False),
                                             pygame.transform.flip(self.JackLumber_charged_ranged_right_anim[1], True, False),
                                             pygame.transform.flip(self.JackLumber_charged_ranged_right_anim[2], True, False),
                                             pygame.transform.flip(self.JackLumber_charged_ranged_right_anim[3], True, False),
                                             pygame.transform.flip(self.JackLumber_charged_ranged_right_anim[4], True, False),
                                             pygame.transform.flip(self.JackLumber_charged_ranged_right_anim[5], True, False),
                                             pygame.transform.flip(self.JackLumber_charged_ranged_right_anim[6], True, False),
                                             pygame.transform.flip(self.JackLumber_charged_ranged_right_anim[7], True, False))
        self.JackLumber_ranged_anim_size = 8
        self.JackLumber_melee_anim_rates = (int(self.fps_t), int(self.fps_t), int(self.fps_t), int(self.fps_t),
                                                 int(self.fps_t), int(self.fps_t), int(self.fps_t), int(self.fps_t))

        """Speeds of everything"""
        # Positives will either move down or to the right, multiplying by -1 will change it to the left or up
        self.fall_acceleration = 7

        self.JackLumber_init_jump_vel = -70
        self.JackLumber_x_vel = 20
        self.JackLumber_dash_vel = self.JackLumber_x_vel * 3

        """Timed delays for characters, objects, and gameplay events"""
        # Only one of these Jack lumber delays can be active at once
        self.JackLumber_damage_reaction_period = 500
        self.JackLumber_dash_stage_1_period = 300
        self.JackLumber_dash_stage_2_period = 800
        self.JackLumber_dashing_period = 150

        # These delays can happen at the same time
        self.JackLumber_charge_M_period = 1000
        self.JackLumber_charge_R_period = 1000
        self.JackLumber_charge_D_period = 1000
        self.JackLumber_damaged_invinc_period = 1000

"""
WorldSettings.py
This file contains the class WorldSettings.  WorldSettings contains the many constants used throughout the program.  It is also used to load in the assets at the beginning of the program.
Much of the program uses the constants found here, so it should be created immediately and passed into most of the functions throughout the program.
"""

import pygame


class WorldSettings(object):
    def __init__(self):
        """ Screen size """
        self.screen_width = 1920
        self.screen_height = 1080

        """ Frames per second """
        self.fps = 60
        self.fps_t = 16 + (2 / 3)  # fps translated to pygame ticks

        """ Sizes of everything """
        # buom stands for the basic unit of measurement used for the sizes of objects in this game
        self.buom = 32

        # Jack Lumber's size
        self.JL_width = self.buom * 2
        self.JL_height = self.JL_width * 2

        # Jack Lumber attack sizes
        self.JL_melee_width = self.JL_width * 2
        self.JL_melee_height = self.JL_height
        self.JL_charged_melee_width = int(self.JL_melee_width * 1.5)
        self.JL_charged_melee_height = int(self.JL_melee_height * 1.5)

        self.JL_ranged_width = self.buom
        self.JL_ranged_height = self.JL_ranged_width
        self.JL_charged_ranged_height = self.JL_height
        self.JL_charged_ranged_width = self.JL_charged_ranged_height

        # Jack Lumber's charge state indicator sizes
        self.charge_M_width = int(self.buom / 2)
        self.charge_M_height = self.charge_M_width
        self.charge_R_width = self.charge_M_width
        self.charge_R_height = self.charge_M_width
        self.charge_D_width = self.charge_M_width
        self.charge_D_height = self.charge_M_width

        # UI related sizes
        self.text_width = int(self.buom * 2)
        self.text_height = self.text_width

        # Twisted Lumber's size
        self.TL_width = int(self.JL_width * 2)
        self.TL_height = int(self.TL_width * 2)

        # Twisted Lumber's attack sizes
        self.TL_leaf_width = self.buom
        self.TL_leaf_height = self.TL_leaf_width
        self.TL_vine_width = int(self.buom / 2)
        self.TL_vine_height = int(self.TL_vine_width * 2)

        # Block sizes
        self.GrassyBlock_width = self.buom
        self.GrassyBlock_height = self.GrassyBlock_width

        # Background block sizes
        self.BackgroundBlock_width = self.buom
        self.BackgroundBlock_height = self.BackgroundBlock_width

        """ Timed delays for characters, objects, and gameplay events """
        # Only one of these Jack lumber delays can be active at once
        self.JL_damage_reaction_period = 500
        self.JL_dash_stage_1_period = 300
        self.JL_dash_stage_2_period = 800
        self.JL_dashing_period = 300
        self.JL_melee_period = 300
        self.JL_melee_life_period = int(self.JL_melee_period / 3)
        self.JL_ranged_period = int(self.JL_melee_period * 2 / 3)

        # These delays can happen at the same time
        self.JL_charge_M_period = 1000
        self.JL_charge_R_period = 1000
        self.JL_charge_D_period = 1000
        self.JL_damaged_invinc_period = 1000

        # Twisted Lumber delays
        self.TL_wait_period = 500
        self.TL_jump_period = 1000
        self.TL_leaf_dart_period = 1500
        self.TL_leaf_dart_part1_period = int(self.TL_leaf_dart_period * 2 / 3)
        self.TL_leaf_dart_wait_period = self.TL_leaf_dart_part1_period
        self.TL_leaf_spiral_period = int(self.TL_leaf_dart_period * 2)
        self.TL_slow_leaf_period = int(self.TL_leaf_spiral_period / 2)
        self.TL_falling_leaves_attack_period = self.TL_leaf_spiral_period
        self.TL_ceiling_shake_period = 3000
        self.TL_create_vine_period = 1  # Every Frame
        self.TL_create_falling_leaf_period = 200

        """ Load non-animated images """
        # Jack Lumber images
        self.JL_left_image = pygame.transform.scale(pygame.image.load('Images/Jack Lumber.png'), (self.JL_width, self.JL_height))
        self.JL_right_image = pygame.transform.flip(self.JL_left_image, True, False)
        self.JL_jump_left_image = pygame.transform.scale(pygame.image.load('Images/Jack Lumber Jump.png'), (self.JL_width, self.JL_height))
        self.JL_jump_right_image = pygame.transform.flip(self.JL_jump_left_image, True, False)
        self.JL_dash_stage_2_left_image = pygame.transform.scale(pygame.image.load('Images/Jack Lumber invincidash-4.png'), (self.JL_width, self.JL_height))
        self.JL_dash_stage_2_right_image = pygame.transform.flip(self.JL_dash_stage_2_left_image, True, False)

        # Twisted Lumber images
        self.TL_left_image = pygame.transform.scale(pygame.image.load('Images/Twisted Lumber-1.png'), (self.TL_width, self.TL_height))
        self.TL_right_image = pygame.transform.flip(self.TL_left_image, True, False)
        self.TL_attack_left_image = pygame.transform.scale(pygame.image.load('Images/Twisted Lumber-2.png'), (self.TL_width, self.TL_height))
        self.TL_attack_right_image = pygame.transform.flip(self.TL_attack_left_image, True, False)
        self.TL_leaf_left_image = pygame.transform.scale(pygame.image.load('Images/TL_Leaf.png'), (self.TL_leaf_width, self.TL_leaf_height))
        self.TL_leaf_right_image = pygame.transform.flip(self.TL_leaf_left_image, True, False)
        self.TL_vine_image = pygame.transform.scale(pygame.image.load('Images/TL_Vine.png'), (self.TL_vine_width, self.TL_vine_height))

        # Charge notification images
        self.charge_M_image = pygame.transform.scale(pygame.image.load('Images/Charge Display-M.png'), (self.charge_M_width, self.charge_M_height))
        self.charge_R_image = pygame.transform.scale(pygame.image.load('Images/Charge Display-R.png'), (self.charge_R_width, self.charge_R_height))
        self.charge_D_image = pygame.transform.scale(pygame.image.load('Images/Charge Display-D.png'), (self.charge_D_width, self.charge_D_height))

        # UI related images
        self.num_0_image = pygame.transform.scale(pygame.image.load('Images/Num_0.png'), (self.text_width, self.text_height))
        self.num_1_image = pygame.transform.scale(pygame.image.load('Images/Num_1.png'), (self.text_width, self.text_height))
        self.num_2_image = pygame.transform.scale(pygame.image.load('Images/Num_2.png'), (self.text_width, self.text_height))
        self.num_3_image = pygame.transform.scale(pygame.image.load('Images/Num_3.png'), (self.text_width, self.text_height))
        self.num_4_image = pygame.transform.scale(pygame.image.load('Images/Num_4.png'), (self.text_width, self.text_height))
        self.num_5_image = pygame.transform.scale(pygame.image.load('Images/Num_5.png'), (self.text_width, self.text_height))
        self.num_6_image = pygame.transform.scale(pygame.image.load('Images/Num_6.png'), (self.text_width, self.text_height))
        self.num_7_image = pygame.transform.scale(pygame.image.load('Images/Num_7.png'), (self.text_width, self.text_height))
        self.num_8_image = pygame.transform.scale(pygame.image.load('Images/Num_8.png'), (self.text_width, self.text_height))
        self.num_9_image = pygame.transform.scale(pygame.image.load('Images/Num_9.png'), (self.text_width, self.text_height))

        # Foreground block image
        self.GrassyBlock_image = pygame.transform.scale(pygame.image.load('Images/Grassy Block.png'), (self.GrassyBlock_width, self.GrassyBlock_height))

        # Background block image
        self.BackgroundBlock_image = pygame.transform.scale(pygame.image.load('Images/Background Block.png'), (self.BackgroundBlock_width, self.BackgroundBlock_height))

        """ Animations (variables for animation sizes just below animation lists) """
        # Jack Lumber walk animation
        self.JL_walk_left_anim = (pygame.transform.scale(pygame.image.load('Images/Jack Lumber Walking-1.png'),
                                                         (self.JL_width, self.JL_height)),
                                  pygame.transform.scale(pygame.image.load('Images/Jack Lumber Walking-2.png'),
                                                                 (self.JL_width, self.JL_height)),
                                  pygame.transform.scale(pygame.image.load('Images/Jack Lumber Walking-3.png'),
                                                                 (self.JL_width, self.JL_height)),
                                  pygame.transform.scale(pygame.image.load('Images/Jack Lumber Walking-4.png'),
                                                                 (self.JL_width, self.JL_height)),
                                  pygame.transform.scale(pygame.image.load('Images/Jack Lumber Walking-5.png'),
                                                                 (self.JL_width, self.JL_height)))
        self.JL_walk_right_anim = (pygame.transform.flip(self.JL_walk_left_anim[0], True, False),
                                   pygame.transform.flip(self.JL_walk_left_anim[1], True, False),
                                   pygame.transform.flip(self.JL_walk_left_anim[2], True, False),
                                   pygame.transform.flip(self.JL_walk_left_anim[3], True, False),
                                   pygame.transform.flip(self.JL_walk_left_anim[4], True, False))
        self.JL_walk_anim_size = 5
        self.JL_walk_anim_rates = (90, 90, 90, 90, 90)

        # Jack Lumber dash stage 1 animation
        self.JL_dash_start_left_anim = (pygame.transform.scale(pygame.image.load('Images/Jack Lumber invincidash-1.png'),
                                                               (self.JL_width, self.JL_height)),
                                        pygame.transform.scale(pygame.image.load('Images/Jack Lumber invincidash-2.png'),
                                                                       (self.JL_width, self.JL_height)),
                                        pygame.transform.scale(pygame.image.load('Images/Jack Lumber invincidash-3.png'),
                                                                       (self.JL_width, self.JL_height)))
        self.JL_dash_start_right_anim = (pygame.transform.flip(self.JL_dash_start_left_anim[0], True, False),
                                         pygame.transform.flip(self.JL_dash_start_left_anim[1], True, False),
                                         pygame.transform.flip(self.JL_dash_start_left_anim[2], True, False))
        self.JL_dash_start_anim_size = 3
        self.JL_dash_start_anim_rates = (75, 75, 150)

        # Jack Lumber invincidash stage 2 animation
        self.JL_invincidash_stage_2_left_anim = (pygame.transform.scale(pygame.image.load('Images/Jack Lumber invincidash-5.png'),
                                                                        (self.JL_width, self.JL_height)),
                                                 pygame.transform.scale(pygame.image.load('Images/Jack Lumber invincidash-6.png'),
                                                                                (self.JL_width, self.JL_height)))
        self.JL_invincidash_stage_2_right_anim = (pygame.transform.flip(self.JL_invincidash_stage_2_left_anim[0], True, False),
                                                  pygame.transform.flip(self.JL_invincidash_stage_2_left_anim[1], True, False))
        self.JL_invincidash_stage_2_anim_size = 2
        self.JL_invincidash_stage_2_anim_rates = (90, 90)

        # Jack Lumber final invincidash animation
        self.JL_invincidash_left_anim = (pygame.transform.scale(pygame.image.load('Images/Jack Lumber Invincijump-1.png'),
                                                                (self.JL_width, self.JL_height)),
                                         pygame.transform.scale(pygame.image.load('Images/Jack Lumber Invincijump-2.png'),
                                                                        (self.JL_width, self.JL_height)))
        self.JL_invincidash_right_anim = (pygame.transform.flip(self.JL_invincidash_left_anim[0], True, False),
                                          pygame.transform.flip(self.JL_invincidash_left_anim[1], True, False))
        self.JL_invincidash_anim_size = 2
        self.JL_invincidash_anim_rates = (90, 90)

        # Jack Lumber's melee and charged melee attack animations
        self.JL_melee_right_anim = (pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-1.png'),
                                                           (self.JL_melee_width,
                                                                    self.JL_melee_height)),
                                    pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-3.png'),
                                                                   (self.JL_melee_width,
                                                                    self.JL_melee_height)),
                                    pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-5.png'),
                                                                   (self.JL_melee_width,
                                                                    self.JL_melee_height)),
                                    pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-4.png'),
                                                                   (self.JL_melee_width,
                                                                    self.JL_melee_height)),
                                    pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-5.png'),
                                                                   (self.JL_melee_width,
                                                                    self.JL_melee_height)),
                                    pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-6.png'),
                                                                   (self.JL_melee_width,
                                                                    self.JL_melee_height)),
                                    pygame.transform.scale(pygame.image.load('Images/Jack Lumber Melee-7.png'),
                                                                   (self.JL_melee_width,
                                                                    self.JL_melee_height)))
        self.JL_melee_left_anim = (pygame.transform.flip(self.JL_melee_right_anim[0], True, False),
                                   pygame.transform.flip(self.JL_melee_right_anim[1], True, False),
                                   pygame.transform.flip(self.JL_melee_right_anim[2], True, False))
        self.JL_charged_melee_right_anim = (pygame.transform.scale(self.JL_melee_right_anim[0],
                                                                   (self.JL_charged_melee_width,
                                                                    self.JL_charged_melee_height)),
                                            pygame.transform.scale(self.JL_melee_right_anim[1],
                                                                   (self.JL_charged_melee_width,
                                                                    self.JL_charged_melee_height)),
                                            pygame.transform.scale(self.JL_melee_right_anim[2],
                                                                   (self.JL_charged_melee_width,
                                                                    self.JL_charged_melee_height)))
        self.JL_charged_melee_left_anim = (pygame.transform.flip(self.JL_charged_melee_right_anim[0], True, False),
                                           pygame.transform.flip(self.JL_charged_melee_right_anim[1], True, False),
                                           pygame.transform.flip(self.JL_charged_melee_right_anim[2], True, False))
        self.JL_melee_anim_size = 3
        JL_melee_anim_rate = self.JL_melee_life_period / self.JL_melee_anim_size
        self.JL_melee_anim_rates = (JL_melee_anim_rate, JL_melee_anim_rate, JL_melee_anim_rate, JL_melee_anim_rate,
                                    JL_melee_anim_rate, JL_melee_anim_rate, JL_melee_anim_rate)

        # Jack Lumber's ranged and charged ranged attack animations
        self.JL_ranged_right_anim = (pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-1.png'),
                                                            (self.JL_ranged_width,
                                                                    self.JL_ranged_height)),
                                     pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-2.png'),
                                                                    (self.JL_ranged_width,
                                                                     self.JL_ranged_height)),
                                     pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-3.png'),
                                                                    (self.JL_ranged_width,
                                                                     self.JL_ranged_height)),
                                     pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-4.png'),
                                                                    (self.JL_ranged_width,
                                                                     self.JL_ranged_height)),
                                     pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-5.png'),
                                                                    (self.JL_ranged_width,
                                                                     self.JL_ranged_height)),
                                     pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-6.png'),
                                                                    (self.JL_ranged_width,
                                                                     self.JL_ranged_height)),
                                     pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-7.png'),
                                                                    (self.JL_ranged_width,
                                                                     self.JL_ranged_height)),
                                     pygame.transform.scale(pygame.image.load('Images/Jack Lumber Ranged-8.png'),
                                                                    (self.JL_ranged_width,
                                                                     self.JL_ranged_height)))
        self.JL_ranged_left_anim = (pygame.transform.flip(self.JL_ranged_right_anim[0], True, False),
                                    pygame.transform.flip(self.JL_ranged_right_anim[1], True, False),
                                    pygame.transform.flip(self.JL_ranged_right_anim[2], True, False),
                                    pygame.transform.flip(self.JL_ranged_right_anim[3], True, False),
                                    pygame.transform.flip(self.JL_ranged_right_anim[4], True, False),
                                    pygame.transform.flip(self.JL_ranged_right_anim[5], True, False),
                                    pygame.transform.flip(self.JL_ranged_right_anim[6], True, False),
                                    pygame.transform.flip(self.JL_ranged_right_anim[7], True, False))
        self.JL_charged_ranged_right_anim = (pygame.transform.scale(self.JL_ranged_right_anim[0],
                                                                    (self.JL_charged_ranged_width,
                                                                            self.JL_charged_ranged_height)),
                                             pygame.transform.scale(self.JL_ranged_right_anim[1],
                                                                            (self.JL_charged_ranged_width,
                                                                            self.JL_charged_ranged_height)),
                                             pygame.transform.scale(self.JL_ranged_right_anim[2],
                                                                            (self.JL_charged_ranged_width,
                                                                            self.JL_charged_ranged_height)),
                                             pygame.transform.scale(self.JL_ranged_right_anim[3],
                                                                            (self.JL_charged_ranged_width,
                                                                            self.JL_charged_ranged_height)),
                                             pygame.transform.scale(self.JL_ranged_right_anim[4],
                                                                            (self.JL_charged_ranged_width,
                                                                            self.JL_charged_ranged_height)),
                                             pygame.transform.scale(self.JL_ranged_right_anim[5],
                                                                            (self.JL_charged_ranged_width,
                                                                            self.JL_charged_ranged_height)),
                                             pygame.transform.scale(self.JL_ranged_right_anim[6],
                                                                            (self.JL_charged_ranged_width,
                                                                            self.JL_charged_ranged_height)),
                                             pygame.transform.scale(self.JL_ranged_right_anim[7],
                                                                            (self.JL_charged_ranged_width,
                                                                            self.JL_charged_ranged_height)))
        self.JL_charged_ranged_left_anim = (pygame.transform.flip(self.JL_charged_ranged_right_anim[0], True, False),
                                            pygame.transform.flip(self.JL_charged_ranged_right_anim[1], True, False),
                                            pygame.transform.flip(self.JL_charged_ranged_right_anim[2], True, False),
                                            pygame.transform.flip(self.JL_charged_ranged_right_anim[3], True, False),
                                            pygame.transform.flip(self.JL_charged_ranged_right_anim[4], True, False),
                                            pygame.transform.flip(self.JL_charged_ranged_right_anim[5], True, False),
                                            pygame.transform.flip(self.JL_charged_ranged_right_anim[6], True, False),
                                            pygame.transform.flip(self.JL_charged_ranged_right_anim[7], True, False))
        self.JL_ranged_anim_size = 8
        self.JL_ranged_anim_rates = (int(self.fps_t), int(self.fps_t), int(self.fps_t), int(self.fps_t),
                                     int(self.fps_t), int(self.fps_t), int(self.fps_t), int(self.fps_t))

        """ Speeds of everything """
        # Positives will either move down or to the right, multiplying by -1 will change it to the left or up
        self.fall_acceleration = 5

        # Jack Lumber speeds
        self.JL_init_jump_vel = -55  # Just enough to get him a little higher than his height
        self.JL_x_vel = 20
        self.JL_dash_vel = self.JL_x_vel * 2

        # Ranged attack speed
        self.JL_ranged_vel = 60

        # Twisted Lumber speeds
        self.TL_init_jump_vel = self.JL_init_jump_vel
        self.TL_x_vel = self.JL_x_vel
        self.TL_vine_rise_vel = -25
        self.TL_leaf_dart_speed = self.JL_ranged_vel
        self.TL_leaf_spiral_angle_vel = 0.1
        self.TL_leaf_spiral_init_radius_accel = 0.05
        self.TL_leaf_spiral_radius_accel = self.TL_leaf_spiral_init_radius_accel * 10

        """ Character stats (Health, damage, etc) """
        # Starting Health
        self.JL_health = 100
        self.TL_health = 100
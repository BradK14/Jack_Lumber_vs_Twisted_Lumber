"""
TwistedLumber.py
This file contains the class for TwistedLumber.  This is the enemy in the game.  Everything defining his ai is found here.
"""

import pygame
import math
from pygame.sprite import Group
from Classes.Character import Character
from Classes.Leaf import Leaf
from Classes.LeafDart import LeafDart
from Classes.LeafSpiral import LeafSpiral
from Classes.Vine import Vine
from Classes.Delay import Delay
from random import seed
from random import randint
from datetime import datetime

seed(datetime.now())

class TwistedLumber(Character):
    def __init__(self, w_settings, x, y, facing_left):
        super(TwistedLumber, self).__init__(w_settings, x, y, facing_left)

        # Apply constants from w_settings
        self.width = self.w_settings.TL_width
        self.height = self.w_settings.TL_height
        self.max_health = self.w_settings.TL_health
        self.health = self.max_health

        # Set up the image and rect
        if self.facing_left:
            self.image = self.w_settings.TL_left_image
        else:
            self.image = self.w_settings.TL_right_image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # For recording the current time
        self.cur_time = 0
        self.time_passed = 0

        # Set up delays for next attack
        self.wait_delay = Delay(self.w_settings.TL_wait_period)
        self.jump_delay = Delay(self.w_settings.TL_jump_period)
        self.leaf_dart_delay = Delay(self.w_settings.TL_leaf_dart_period)
        self.leaf_spiral_delay = Delay(self.w_settings.TL_leaf_spiral_period)
        self.falling_leaves_attack_delay = Delay(self.w_settings.TL_falling_leaves_attack_period)
        self.ceiling_shake_delay = Delay(self.w_settings.TL_ceiling_shake_period)
        self.cur_delay = None  # Only used for the attack delays
        self.vines_to_create = 0

        # Set up delays for determining Twisted Lumbers image
        self.leaf_dart_part1_delay = Delay(self.w_settings.TL_leaf_dart_part1_period)

        # Set up other delays
        self.create_falling_leaf_delay = Delay(self.w_settings.TL_create_falling_leaf_period)

        # States
        self.jumping = False
        self.firing_leaf_dart = False
        self.firing_leaf_spiral = False
        self.creating_vines = False
        self.rising_by_vines = False
        self.ceiling_shake = False
        if self.facing_left:
            self.jump_dir = -1
        else:
            self.jump_dir = 1

        # Objects directly attached to this character
        self.newest_vine = None
        self.vines = Group()

    # Update position
    def update_pos(self, time_passed):
        # First save previous position
        self.previous_position = [self.rect.left, self.rect.top, self.rect.right, self.rect.bottom]

        # Positioning based off jumping move
        if self.jumping and not self.grounded:
            self.x += self.w_settings.TL_x_vel * time_passed * self.jump_dir
            self.rect.x = int(self.x)
        else:
            self.jumping = False

        # Positioning based off falling leaves attack
        if self.rising_by_vines:
            self.y_velocity = self.w_settings.TL_vine_rise_vel * time_passed

        # Only reposition if not using these moves
        if not self.ceiling_shake and not self.creating_vines:
            self.y_velocity += self.w_settings.fall_acceleration * time_passed
            self.y += self.y_velocity
            self.rect.y = int(self.y)

    # Set the image in use
    def update_animation(self, cur_time):
        if self.firing_leaf_dart and self.leaf_dart_part1_delay.is_active(cur_time) or self.firing_leaf_spiral or self.creating_vines or self.ceiling_shake:
            if self.facing_left:
                self.image = self.w_settings.TL_attack_left_image
            else:
                self.image = self.w_settings.TL_attack_right_image
        else:
            if self.facing_left:
                self.image = self.w_settings.TL_left_image
            else:
                self.image = self.w_settings.TL_right_image

    def check_attack_collisions(self, surfaces, ranged_attacks, melee_attack):
        # For creating a vine
        if self.newest_vine is None:
            pass
        elif self.creating_vines:
            for surface in surfaces:
                if self.newest_vine.rect.colliderect(surface):
                    self.creating_vines = False
                    self.newest_vine = None
                    self.rising_by_vines = True
                    self.grounded = False
                    break

        # For taking damage from Jack's melee attacks
        if melee_attack is not None:
            if self.rect.colliderect(melee_attack.rect):
                melee_attack.damage_once(self)

        # For taking damage from Jack's ranged attacks
        for ranged_attack in ranged_attacks:
            if self.rect.colliderect(ranged_attack.rect):
                ranged_attack.damage_once(self)

        # Check to see if Twisted Lumber is dead
        if self.health <= 0:
            self.health = 0

    def decide_next_move(self, cur_time, time_passed, leaves, jack=None):
        # Set the time
        self.cur_time = cur_time
        self.time_passed = time_passed

        if self.grounded:  # Can only begin a new action while touching the ground
            if not self.cur_delay_is_active(cur_time):
                if self.cur_delay is not None:
                    self.cur_delay.reset()
                # Reset states and animations
                self.firing_leaf_dart = False
                self.firing_leaf_spiral = False
                if self.cur_delay is self.falling_leaves_attack_delay:
                    self.vines.empty()
                    self.newest_vine = None
                    self.creating_vines = False

                # Face towards Jack
                if jack is not None:
                    if jack.x < self.x:
                        self.facing_left = True
                    else:
                        self.facing_left = False

                # Choose an action at random
                randchoice = randint(1, 100)
                if randchoice <= 10:  # 10% chance to do nothing 10
                    self.cur_delay = self.wait_delay
                    self.wait()
                elif randchoice <= 35:  # 25% chance to jump towards Jack: 35
                    self.cur_delay = self.jump_delay
                    self.jump()
                elif randchoice <= 65:  # 30% chance to fire a leaf towards Jack: 65
                    self.cur_delay = self.leaf_dart_delay
                    self.leaf_dart(cur_time, leaves)
                elif randchoice <= 85:  # 20% chance to send out a spiral of leaves: 85
                    self.cur_delay = self.leaf_spiral_delay
                    self.leaf_spiral(cur_time, leaves)
                elif randchoice > 85:  # 15% chance to send out a vine to the ceiling to make leaves rain down
                    self.cur_delay = self.falling_leaves_attack_delay
                    self.falling_leaves_attack(cur_time)

                self.cur_delay.begin(cur_time)

    def update_attacks(self, cur_time, leaves):
        # Part 1 of falling leaves attack
        if self.creating_vines:
            self.create_vine()

        # Part 2 of falling leaves attack
        if self.rising_by_vines:
            for vine in self.vines:
                if vine.rect.top > self.rect.centery:
                    self.vines.remove(vine)

        # Part 3 of falling leaves attack
        if self.ceiling_shake:
            if not self.cur_delay_is_active(cur_time):
                self.cur_delay.reset()
                self.ceiling_shake = False
                self.vines.empty()
            else:
                if not self.create_falling_leaf_delay.is_active(cur_time):
                    leaves.add(Leaf(self.w_settings,
                                    randint(0, self.w_settings.screen_width - self.w_settings.TL_leaf_width),
                                    0,
                                    self.facing_left,
                                    cur_time))
                    self.create_falling_leaf_delay.reset()
                    self.create_falling_leaf_delay.begin(cur_time)

    def wait(self):
        pass  # Do nothing on purpose

    def jump(self):
        self.jumping = True
        self.grounded = False
        self.y_velocity += self.w_settings.TL_init_jump_vel * self.time_passed

        if self.facing_left:
            self.jump_dir = -1
        else:
            self.jump_dir = 1

    def leaf_dart(self, cur_time, leaves):
        self.firing_leaf_dart = True
        self.leaf_dart_part1_delay.reset()
        self.leaf_dart_part1_delay.begin(cur_time)

        # Create one leaf on his back 2/3 up from the bottom and another 1/3 up from bottom
        num_leaves_minus_one = 3
        if self.facing_left:
            for num_leaf in range(1, num_leaves_minus_one):
                leaves.add(LeafDart(self.w_settings,
                                    self.rect.right - self.w_settings.TL_leaf_width,
                                    int(self.rect.top + self.w_settings.TL_height * num_leaf / num_leaves_minus_one - self.w_settings.TL_leaf_height / 2),
                                    self.facing_left,
                                    cur_time))
        else:
            for num_leaf in range(1, num_leaves_minus_one):
                leaves.add(LeafDart(self.w_settings,
                                    self.rect.left,
                                    int(self.rect.top + self.w_settings.TL_height * num_leaf / num_leaves_minus_one - self.w_settings.TL_leaf_height / 2),
                                    self.facing_left,
                                    cur_time))

    def leaf_spiral(self, cur_time, leaves):
        self.firing_leaf_spiral = True

        # Eight leaves evenly spaced between each other while spiraling
        max_leaves = 20
        for angle_pos in range(0, max_leaves):
            leaves.add(LeafSpiral(self.w_settings,
                                  self.rect.centerx,
                                  self.rect.centery,
                                  self.facing_left,
                                  cur_time,
                                  math.radians(angle_pos * int(360 / max_leaves))))

    def falling_leaves_attack(self, cur_time):
        self.creating_vines = True

    def create_vine(self):
        self.vines_to_create += self.w_settings.TL_create_vine_period / self.time_passed
        while self.vines_to_create >= 1:
            if self.newest_vine is None:
                self.newest_vine = Vine(self.w_settings,
                                        int(self.rect.centerx - self.w_settings.TL_vine_width / 2),
                                        self.rect.centery - self.w_settings.TL_vine_height)
            else:  # Continue creating vines over the top of the last one
                self.newest_vine = Vine(self.w_settings,
                                        self.newest_vine.rect.x,
                                        self.newest_vine.rect.top - self.w_settings.TL_vine_height)
            self.vines.add(self.newest_vine)
            self.vines_to_create -= 1

    # Helper function to check if our general delay variables are active
    def cur_delay_is_active(self, cur_time):
        if self.cur_delay is not None:
            if self.cur_delay.is_active(cur_time):
                return True
        return False

    def below_surface(self, surface):
        super(TwistedLumber, self).below_surface(surface)
        if self.rising_by_vines:
            self.rising_by_vines = False
            self.ceiling_shake = True
            self.cur_delay = self.ceiling_shake_delay
            self.cur_delay.reset()
            self.cur_delay.begin(self.cur_time)

    def blit_me(self, screen):
        screen.blit_obj(self)
        for vine in self.vines:
            screen.blit_img_rect(self.w_settings.TL_vine_image, vine)

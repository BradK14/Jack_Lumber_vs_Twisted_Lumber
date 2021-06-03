"""
JackLumber.py
This file contains the class for JackLumber.  Everything needed to manipulate the playable character is here.
"""

import pygame
from Classes.Character import Character
from Classes.Animation import Animation
from Classes.Delay import Delay


class JackLumber(Character):
    def __init__(self, w_settings, x, y, facing_left):
        super(JackLumber, self).__init__(w_settings, x, y, facing_left)

        # Apply constants from w_settings
        self.width = self.w_settings.JackLumber_width
        self.height = self.w_settings.JackLumber_height
        self.x_vel = self.w_settings.JackLumber_x_vel
        self.dash_vel = self.w_settings.JackLumber_dash_vel

        # Set up the image and rect
        if self.facing_left:
            self.image = self.w_settings.JackLumber_left_image
        else:
            self.image = self.w_settings.JackLumber_right_image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # A variable to refresh the current time for use in animations and delays
        self.cur_time = 0

        # Set up animation handling
        self.walk_left_anim = Animation(self.w_settings.JackLumber_walk_left_anim,
                                        self.w_settings.JackLumber_walk_anim_size,
                                        self.w_settings.JackLumber_walk_anim_rates)
        self.walk_right_anim = Animation(self.w_settings.JackLumber_walk_right_anim,
                                         self.w_settings.JackLumber_walk_anim_size,
                                         self.w_settings.JackLumber_walk_anim_rates)
        self.dash_stage_1_left_anim = Animation(self.w_settings.JackLumber_dash_start_left_anim,
                                                self.w_settings.JackLumber_dash_start_anim_size,
                                                self.w_settings.JackLumber_dash_start_anim_rates)
        self.dash_stage_1_right_anim = Animation(self.w_settings.JackLumber_dash_start_right_anim,
                                                 self.w_settings.JackLumber_dash_start_anim_size,
                                                 self.w_settings.JackLumber_dash_start_anim_rates)
        self.invincidash_stage_2_left_anim = Animation(self.w_settings.JackLumber_invincidash_stage_2_left_anim,
                                                       self.w_settings.JackLumber_invincidash_stage_2_anim_size,
                                                       self.w_settings.JackLumber_invincidash_stage_2_anim_rates)
        self.invincidash_stage_2_right_anim = Animation(self.w_settings.JackLumber_invincidash_stage_2_right_anim,
                                                       self.w_settings.JackLumber_invincidash_stage_2_anim_size,
                                                       self.w_settings.JackLumber_invincidash_stage_2_anim_rates)
        self.invincidash_left_anim = Animation(self.w_settings.JackLumber_invincidash_left_anim,
                                               self.w_settings.JackLumber_invincidash_anim_size,
                                               self.w_settings.JackLumber_invincidash_anim_rates)
        self.invincidash_right_anim = Animation(self.w_settings.JackLumber_invincidash_right_anim,
                                               self.w_settings.JackLumber_invincidash_anim_size,
                                               self.w_settings.JackLumber_invincidash_anim_rates)
        self.cur_anim = self.walk_left_anim

        # Set up various delays
        self.damage_reaction_delay = Delay(self.w_settings.JackLumber_damage_reaction_period)
        self.damaged_invinc_delay = Delay(self.w_settings.JackLumber_damaged_invinc_period)
        self.dash_stage_1_delay = Delay(self.w_settings.JackLumber_dash_stage_1_period)
        self.dash_stage_2_delay = Delay(self.w_settings.JackLumber_dash_stage_2_period)
        self.dashing_delay = Delay(self.w_settings.JackLumber_dashing_period)
        self.cur_delay = Delay(0)

        self.M_delay = Delay(self.w_settings.JackLumber_charge_M_period)
        self.R_delay = Delay(self.w_settings.JackLumber_charge_R_period)
        self.D_delay = Delay(self.w_settings.JackLumber_charge_D_period)

        # Set up bools to keep track of what controls are being used
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.dash_pressed = False
        self.jump_pressed = False
        self.melee_pressed = False
        self.ranged_pressed = False

        # Set up bools to keep track of the state of the character
        # self.facing_left and self.grounded are taken care of in parent class (Character)
        self.moving_x = False
        self.dashing_x = False
        self.dashing_up = False
        self.dashing_down = False
        self.jump_pressed_once = False
        self.dash_ready = False
        self.being_damaged = False
        self.melee_attacking = False
        self.ranged_attacking = False
        self.dash_stage_1 = False
        self.dash_stage_2 = False
        self.dashing = False
        self.melee_charged = False
        self.ranged_charged = False
        self.dash_charged = False
        self.dash_consumed = False  # True at the start of a dash when charged
        self.invincible = False

    def left_press(self, left_pressed):
        self.left_pressed = left_pressed

    def right_press(self, right_pressed):
        self.right_pressed = right_pressed

    def up_press(self, up_pressed):
        self.up_pressed = up_pressed

    def down_press(self, down_pressed):
        self.down_pressed = down_pressed

    def jump_press(self, jump_pressed):
        self.jump_pressed = jump_pressed

    def invincidash(self, dash_pressed):
        self.dash_pressed = dash_pressed

    # Here we sort out most of our bools based on input from the user and restrictions from delays
    def determine_state(self, cur_time):
        # Update the current time
        self.cur_time = cur_time
        # Check if Jack has fully charged any of his abilities
        if self.M_delay.is_active(self.cur_time):
            self.melee_charged = False
        else:
            self.M_delay.reset()
            self.melee_charged = True

        if self.R_delay.is_active(self.cur_time):
            self.ranged_charged = False
        else:
            self.R_delay.reset()
            self.ranged_charged = True

        if self.dash_stage_1 or self.dash_stage_2 or self.dashing:
            self.D_delay.reset()
            self.dash_charged = False
        elif self.D_delay.is_active(self.cur_time):
            self.dash_charged = False
        else:
            self.D_delay.reset()
            self.dash_charged = True

        # if we are in a state of delay from either being damaged, dash_stage_1, dash_stage_2, or dashing
        if self.cur_delay.is_active(self.cur_time):
            # Cancel delay if in dash stage 1 or 2 and we release the dash button
            if self.dash_stage_1 and not self.dash_pressed:
                self.dash_stage_1 = False
                self.cur_delay.reset()
                self.dash_consumed = False
                self.D_delay.begin(self.cur_time)
            elif self.dash_stage_2 and not self.dash_pressed:
                self.dash_stage_2 = False
                self.cur_delay.reset()
                self.dash_consumed = False
                self.D_delay.begin(self.cur_time)
            # Cancel delay and immediately enter last stage of dash
            elif self.dash_stage_2 and self.up_pressed:
                self.dash_stage_2 = False
                self.dashing = True
                self.dashing_up = True
                self.cur_delay.reset()
                self.cur_delay = self.dashing_delay
                self.cur_delay.begin(self.cur_time)
            elif self.dash_stage_2 and self.down_pressed:
                self.dash_stage_2 = False
                self.dashing = True
                self.dashing_down = True
                self.cur_delay.reset()
                self.cur_delay = self.dashing_delay
                self.cur_delay.begin(self.cur_time)
            elif self.dash_stage_2 and self.left_pressed:
                self.dash_stage_2 = False
                self.dashing = True
                self.dashing_x = True
                self.facing_left = True
                self.cur_delay.reset()
                self.cur_delay = self.dashing_delay
                self.cur_delay.begin(self.cur_time)
            elif self.dash_stage_2 and self.right_pressed:
                self.dash_stage_2 = False
                self.dashing = True
                self.dashing_x = True
                self.facing_left = False
                self.cur_delay.reset()
                self.cur_delay = self.dashing_delay
                self.cur_delay.begin(self.cur_time)
        else:  # Delay has run out or is inactive
            # Shift from dash stage 1 to dash stage 2
            if self.dash_stage_1:
                self.cur_delay.reset()
                self.dash_stage_1 = False
                self.dash_stage_2 = True
                if self.dash_consumed:
                    self.invincible = True
                self.cur_delay = self.dash_stage_2_delay
                self.cur_delay.begin(self.cur_time)
            # Exit dash stage 2
            elif self.dash_stage_2:
                self.cur_delay.reset()
                self.dash_stage_2 = False
                if self.dash_consumed:
                    self.invincible = False
                    self.dash_consumed = False
                self.D_delay.begin(self.cur_time)
            # Exit dashing
            elif self.dashing:
                self.cur_delay.reset()
                self.cur_delay = Delay(0)
                if self.dash_consumed:
                    self.invincible = False
                    self.dash_consumed = False
                self.D_delay.begin(self.cur_time)
                self.dashing = False
                self.dashing_up = False
                self.dashing_down = False
                self.dashing_x = False
                self.y_velocity = 0
            # Enter dash stage 1
            elif self.dash_pressed and self.dash_ready:
                self.dash_ready = False
                if self.dash_charged:
                    self.dash_consumed = True
                self.cur_delay = self.dash_stage_1_delay
                self.cur_delay.begin(self.cur_time)
                self.dash_stage_1 = True
                self.moving_x = False
            else:  # Regular movement allowed
                if self.left_pressed and not self.right_pressed:
                    self.moving_x = True
                    self.facing_left = True
                elif self.right_pressed and not self.left_pressed:
                    self.moving_x = True
                    self.facing_left = False
                else:
                    self.moving_x = False
                # Jump
                if self.jump_pressed and self.grounded:
                    if not self.jump_pressed_once:
                        self.jump_pressed_once = True
                        self.y_velocity = self.w_settings.JackLumber_init_jump_vel
                elif not self.jump_pressed:  # Must release the jump button at least once before attempting to jump again
                    self.jump_pressed_once = False

    # Update position
    def update_pos(self):
        """
        if self.being_damaged:
            self.moving_x = False
        """
        if self.dash_stage_1:
            self.y_velocity = 0
        elif self.dash_stage_2:
            self.y_velocity = 0
        elif self.dashing:
            if self.dashing_up:
                self.y += self.dash_vel * -1
                self.y_velocity = self.dash_vel * -1
            elif self.dashing_down:
                self.y += self.dash_vel
                self.y_velocity = self.dash_vel
            elif self.dashing_x:
                if self.facing_left:
                    self.x += self.dash_vel * -1
                    self.y_velocity = 0
                else:
                    self.x += self.dash_vel
                    self.y_velocity = 0
        else:
            if self.moving_x and self.facing_left:
                self.x += self.x_vel * -1
            elif self.moving_x and not self.facing_left:
                self.x += self.x_vel

            # Apply y axis acceleration and speed
            self.y_velocity += self.w_settings.fall_acceleration
            self.y += self.y_velocity

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update_animation(self):
        # Dash stage 1
        if self.dash_stage_1:
            if self.facing_left:
                if self.cur_anim != self.dash_stage_1_left_anim:
                    self.cur_anim.reset()
                    self.cur_anim = self.dash_stage_1_left_anim
                self.image = self.cur_anim.play_once(self.cur_time)
            elif not self.facing_left:
                if self.cur_anim != self.dash_stage_1_right_anim:
                    self.cur_anim.reset()
                    self.cur_anim = self.dash_stage_1_right_anim
                self.image = self.cur_anim.play_once(self.cur_time)
        # Dash stage 2
        elif self.dash_stage_2:
            if self.facing_left:
                if self.dash_consumed:
                    if self.cur_anim != self.invincidash_stage_2_left_anim:
                        self.cur_anim.reset()
                        self.cur_anim = self.invincidash_stage_2_left_anim
                    self.image = self.cur_anim.play(self.cur_time)
                else:
                    self.image = self.w_settings.JackLumber_dash_stage_2_left_image
            elif not self.facing_left:
                if self.dash_consumed:
                    if self.cur_anim != self.invincidash_stage_2_right_anim:
                        self.cur_anim.reset()
                        self.cur_anim = self.invincidash_stage_2_right_anim
                    self.image = self.cur_anim.play(self.cur_time)
                else:
                    self.image = self.w_settings.JackLumber_dash_stage_2_right_image
        # Invincidash
        elif self.dashing and self.dash_consumed:
            if self.facing_left:
                if self.cur_anim != self.invincidash_left_anim:
                    self.cur_anim.reset()
                    self.cur_anim = self.invincidash_left_anim
                self.image = self.cur_anim.play(self.cur_time)
            elif not self.facing_left:
                if self.cur_anim != self.invincidash_right_anim:
                    self.cur_anim.reset()
                    self.cur_anim = self.invincidash_right_anim
                self.image = self.cur_anim.play(self.cur_time)
        # Walking
        elif self.moving_x and self.grounded:
            if self.facing_left:
                if self.cur_anim != self.walk_left_anim:
                    self.cur_anim.reset()
                    self.cur_anim = self.walk_left_anim
                self.image = self.cur_anim.play(self.cur_time)
            elif not self.facing_left:
                if self.cur_anim != self.walk_right_anim:
                    self.cur_anim.reset()
                    self.cur_anim = self.walk_right_anim
                self.image = self.cur_anim.play(self.cur_time)
        else:
            self.cur_anim.reset()
            # In the air
            if self.facing_left and not self.grounded:
                self.image = self.w_settings.JackLumber_jump_left_image
            elif not self.grounded:
                self.image = self.w_settings.JackLumber_jump_right_image
            # Standing still
            elif self.facing_left:
                self.image = self.w_settings.JackLumber_left_image
            else:
                self.image = self.w_settings.JackLumber_right_image

    # Addition to limit dash to once per jump (infinite while on the ground)
    def on_top_of_surface(self, surface):
        super(JackLumber, self).on_top_of_surface(surface)
        self.dash_ready = True
        if self.cur_delay == self.dashing_delay:
            self.cur_delay.reset()
            self.cur_delay = Delay(0)
            self.dashing = False
            self.dashing_x = False
            self.dashing_up = False
            self.dashing_down = False
            self.y_velocity = 0
            if self.dash_consumed:
                self.invincible = False
                self.dash_consumed = False
            self.D_delay.begin(self.cur_time)

    # Bonk the bottom of a surface, kill upwards momentum
    def below_surface(self, surface):
        super(JackLumber, self).below_surface(surface)
        if self.cur_delay == self.dashing_delay:
            self.cur_delay.reset()
            self.cur_delay = Delay(0)
            self.dashing = False
            self.dashing_x = False
            self.dashing_up = False
            self.dashing_down = False
            self.y_velocity = 0
            if self.dash_consumed:
                self.invincible = False
                self.dash_consumed = False
            self.D_delay.begin(self.cur_time)

    def left_of_surface(self, surface):
        super(JackLumber, self).left_of_surface(surface)
        if self.cur_delay == self.dashing_delay:
            self.cur_delay.reset()
            self.cur_delay = Delay(0)
            self.dashing = False
            self.dashing_x = False
            self.dashing_up = False
            self.dashing_down = False
            self.y_velocity = 0
            if self.dash_consumed:
                self.invincible = False
                self.dash_consumed = False
            self.D_delay.begin(self.cur_time)

    def right_of_surface(self, surface):
        super(JackLumber, self).right_of_surface(surface)
        if self.cur_delay == self.dashing_delay:
            self.cur_delay.reset()
            self.cur_delay = Delay(0)
            self.dashing = False
            self.dashing_x = False
            self.dashing_up = False
            self.dashing_down = False
            self.y_velocity = 0
            if self.dash_consumed:
                self.invincible = False
                self.dash_consumed = False
            self.D_delay.begin(self.cur_time)

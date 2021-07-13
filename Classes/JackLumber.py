"""
JackLumber.py
This file contains the class for JackLumber.  Everything needed to manipulate the playable character is here.
"""

import pygame
from Classes.Character import Character
from Classes.Animation import Animation
from Classes.Delay import Delay
from Classes.Melee import Melee
from Classes.ChargedMelee import ChargedMelee
from Classes.Ranged import Ranged
from Classes.ChargedRanged import ChargedRanged


class JackLumber(Character):
    def __init__(self, w_settings, x, y, facing_left):
        super(JackLumber, self).__init__(w_settings, x, y, facing_left)

        # Apply constants from w_settings
        self.width = self.w_settings.JL_width
        self.height = self.w_settings.JL_height
        self.x_vel = self.w_settings.JL_x_vel
        self.dash_vel = self.w_settings.JL_dash_vel

        # Set up the image and rect
        if self.facing_left:
            self.image = self.w_settings.JL_left_image
        else:
            self.image = self.w_settings.JL_right_image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Variable to contain his melee attack
        self.melee = None

        # A variable to refresh the current time for use in animations and delays
        self.cur_time = 0

        # Set up animation handling
        self.walk_left_anim = Animation(self.w_settings.JL_walk_left_anim,
                                        self.w_settings.JL_walk_anim_size,
                                        self.w_settings.JL_walk_anim_rates)
        self.walk_right_anim = Animation(self.w_settings.JL_walk_right_anim,
                                         self.w_settings.JL_walk_anim_size,
                                         self.w_settings.JL_walk_anim_rates)
        self.dash_stage_1_left_anim = Animation(self.w_settings.JL_dash_start_left_anim,
                                                self.w_settings.JL_dash_start_anim_size,
                                                self.w_settings.JL_dash_start_anim_rates)
        self.dash_stage_1_right_anim = Animation(self.w_settings.JL_dash_start_right_anim,
                                                 self.w_settings.JL_dash_start_anim_size,
                                                 self.w_settings.JL_dash_start_anim_rates)
        self.invincidash_stage_2_left_anim = Animation(self.w_settings.JL_invincidash_stage_2_left_anim,
                                                       self.w_settings.JL_invincidash_stage_2_anim_size,
                                                       self.w_settings.JL_invincidash_stage_2_anim_rates)
        self.invincidash_stage_2_right_anim = Animation(self.w_settings.JL_invincidash_stage_2_right_anim,
                                                        self.w_settings.JL_invincidash_stage_2_anim_size,
                                                        self.w_settings.JL_invincidash_stage_2_anim_rates)
        self.invincidash_left_anim = Animation(self.w_settings.JL_invincidash_left_anim,
                                               self.w_settings.JL_invincidash_anim_size,
                                               self.w_settings.JL_invincidash_anim_rates)
        self.invincidash_right_anim = Animation(self.w_settings.JL_invincidash_right_anim,
                                                self.w_settings.JL_invincidash_anim_size,
                                                self.w_settings.JL_invincidash_anim_rates)
        self.cur_anim = self.walk_left_anim

        # Set up various delays
        self.damage_reaction_delay = Delay(self.w_settings.JL_damage_reaction_period)
        self.damaged_invinc_delay = Delay(self.w_settings.JL_damaged_invinc_period)
        self.dash_stage_1_delay = Delay(self.w_settings.JL_dash_stage_1_period)
        self.dash_stage_2_delay = Delay(self.w_settings.JL_dash_stage_2_period)
        self.dashing_delay = Delay(self.w_settings.JL_dashing_period)
        self.cur_delay = None

        self.melee_delay = Delay(self.w_settings.JL_melee_period)
        self.melee_life_delay = Delay(self.w_settings.JL_melee_life_period)
        self.ranged_delay = Delay(self.w_settings.JL_ranged_period)
        self.attack_delay = None

        self.M_delay = Delay(self.w_settings.JL_charge_M_period)
        self.R_delay = Delay(self.w_settings.JL_charge_R_period)

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
        self.air_dashing = False
        self.jump_pressed_already = False
        self.jumping = False
        self.wall_jumping = False
        self.dash_ready = False
        self.being_damaged = False
        self.charged_melee_attacking = False  # Used for determining if we can perform a wall jump
        # self.ranged_attacking = False
        self.dash_stage_1 = False
        self.dash_stage_2 = False
        self.dashing = False
        self.grounded_dashing = False  # Used to validate dash jumps
        self.melee_charged = False
        self.ranged_charged = False
        self.ranged_is_created = False  # Checked by the main loop to know whether or not to create a ranged attack
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

    """
    Determining the characters state 
    Here we sort out most of our bools based on input from the user and restrictions from delays
    """
    def determine_state(self, cur_time):
        # Update the current time
        self.cur_time = cur_time

        # Reset temporary markers
        self.charged_melee_attacking = False

        # Check if jump button has been released since the last jump
        if not self.jump_pressed:
            self.jump_pressed_already = False

        # Check if Jack has fully charged any of his attacks
        # Melee charge up
        if self.M_delay.is_active(self.cur_time):
            self.melee_charged = False
        else:
            self.M_delay.reset()
            self.melee_charged = True
        # Ranged charge up
        if self.R_delay.is_active(self.cur_time):
            self.ranged_charged = False
        else:
            self.R_delay.reset()
            self.ranged_charged = True

        # Melee reset when melee
        if not self.melee_life_delay.is_active(self.cur_time):
            del self.melee
            self.melee = None
            self.melee_life_delay.reset()

        # Melee and Ranged attacks
        if self.melee_pressed or self.ranged_pressed:
            # Allow regular movement
            self.set_regular_movement_states()
            # If dashing previously, cancel it and turn on air dash
            if self.cur_delay_is_active():
                self.reset_cur_delay()
                self.dashing_x = False
                self.dashing_up = False
                self.dashing_down = False
                self.dash_stage_1 = False
                self.dash_stage_2 = False
                self.dashing = False
                self.grounded_dashing = False
                self.air_dashing = True
            # Check if we are able to attack
            if not self.attack_delay_is_active():
                self.reset_attack_delay()
                if self.melee_pressed:
                    if self.melee_charged:
                        self.melee = ChargedMelee(self.w_settings, self.rect, self.facing_left)
                        self.charged_melee_attacking = True
                    else:
                        self.melee = Melee(self.w_settings, self.rect, self.facing_left)
                    self.melee_life_delay.begin(self.cur_time)
                    self.M_delay.reset()
                    self.M_delay.begin(self.cur_time)
                    self.attack_delay = self.melee_delay
                    self.attack_delay.begin(self.cur_time)
                # Ranged
                elif self.ranged_pressed:
                    self.ranged_is_created = True  # To be consumed in a function call
                    self.R_delay.reset()
                    self.R_delay.begin(self.cur_time)
                    self.attack_delay = self.ranged_delay
                    self.attack_delay.begin(self.cur_time)

        # if we are in a state of delay from either being damaged, dash_stage_1, dash_stage_2, or dashing
        elif self.cur_delay_is_active():
            '''
            # If attacking, allow regular movement
            if self.attack_delay == self.melee_delay or self.attack_delay == self.ranged_delay:
                self.set_regular_movement_states()
            '''
            # Cancel delay if in dash stage 1 or 2 and we release the dash button
            if (self.dash_stage_1 or self.dash_stage_2) and not self.dash_pressed:
                self.reset_cur_delay()
                self.dash_stage_1 = False
                self.dash_stage_2 = False
            # Cancel delay from dash stage 1 or 2 and immediately enter last stage of dash
            elif (self.dash_stage_1 or self.dash_stage_2) and\
                    (self.up_pressed or
                     self.down_pressed or
                     self.left_pressed or
                     self.right_pressed) and not\
                    ((self.left_pressed and self.right_pressed) and (not self.up_pressed or not self.down_pressed)):
                self.reset_cur_delay()
                self.dash_stage_1 = False
                self.dash_stage_2 = False
                self.set_dashing_states()
            # Dash Jump
            elif self.dashing and self.grounded_dashing and self.jump_pressed and not self.jump_pressed_already:
                self.air_dashing = True
                self.jumping = True
                self.jump_pressed_already = True
                self.reset_cur_delay()
                self.dashing = False
                self.dashing_x = False
            # Cancel dash by releasing the direction that we are dashing in
            elif self.dashing:
                if (self.dashing_up and not self.up_pressed) or\
                        (self.dashing_down and not self.down_pressed) or\
                        (self.dashing_x and self.facing_left and not self.left_pressed) or\
                        (self.dashing_x and not self.facing_left and not self.right_pressed):
                    self.reset_cur_delay()
                    self.dashing = False
                    self.dashing_up = False
                    self.dashing_down = False
                    self.dashing_x = False
                    self.air_dashing = True

        # Delay has run out or is inactive
        else:
            '''
            if self.cur_delay == self.melee_delay:
                self.reset_cur_delay()
                del self.melee
            '''
            # Shift from dash stage 1 to dash stage 2
            if self.dash_stage_1:
                self.reset_cur_delay()
                self.dash_stage_1 = False
                self.dash_stage_2 = True
                self.cur_delay = self.dash_stage_2_delay
                self.cur_delay.begin(self.cur_time)
            # Exit dash stage 2
            elif self.dash_stage_2:
                self.reset_cur_delay()
                self.dash_stage_2 = False
            # Exit dashing
            elif self.dashing:
                self.reset_cur_delay()
                self.dashing = False
                self.dashing_up = False
                self.dashing_down = False
                self.dashing_x = False
                self.air_dashing = True
                self.y_velocity = 0
            # Enter dash stage 1 or immediately dash
            elif self.dash_pressed and self.dash_ready:
                self.dash_ready = False
                if self.grounded:
                    self.grounded_dashing = True
                if (self.up_pressed or self.right_pressed or self.left_pressed or self.down_pressed) and not\
                        ((self.left_pressed and self.right_pressed) and (not self.up_pressed or not self.down_pressed)):
                    self.set_dashing_states()
                else:
                    self.cur_delay = self.dash_stage_1_delay
                    self.cur_delay.begin(self.cur_time)
                    self.dash_stage_1 = True
                    self.moving_x = False
            else:  # Regular movement allowed, and attacks are allowed
                self.set_regular_movement_states()
                '''
                # Melee
                if self.melee_pressed:
                    if self.melee_charged:
                        self.melee = ChargedMelee(self.w_settings, self.rect, self.facing_left)
                    else:
                        self.melee = Melee(self.w_settings, self.rect, self.facing_left)
                    self.M_delay.reset()
                    self.M_delay.begin(self.cur_time)
                    self.cur_delay = self.melee_delay
                    self.cur_delay.begin(self.cur_time)
                # Ranged
                elif self.ranged_pressed:
                    pass
                '''

    # Helper functions to reset our delay variables to None
    def reset_cur_delay(self):
        if self.cur_delay is not None:
            self.cur_delay.reset()
            del self.cur_delay
            self.cur_delay = None

    def reset_attack_delay(self):
        if self.attack_delay is not None:
            self.attack_delay.reset()
            del self.attack_delay
            self.attack_delay = None

    # Helper functions to check if our general delay variables are active
    def cur_delay_is_active(self):
        if self.cur_delay is not None:
            if self.cur_delay.is_active(self.cur_time):
                return True
        return False

    def attack_delay_is_active(self):
        if self.attack_delay is not None:
            if self.attack_delay.is_active(self.cur_time):
                return True
        return False

    # Use this to shift to a state of dashing
    def set_dashing_states(self):
        self.dashing = True
        self.cur_delay = self.dashing_delay
        self.cur_delay.begin(self.cur_time)
        # Dash up
        if self.up_pressed:
            self.dashing_up = True
            self.grounded_dashing = False
        # Dash down
        elif self.down_pressed:
            self.dashing_down = True
            self.grounded_dashing = False
        # Dash left or right
        elif self.left_pressed or self.right_pressed:
            self.dashing_x = True
            if self.left_pressed:  # Left
                self.facing_left = True
            else:  # Right
                self.facing_left = False

    # determine states helper function for normal movement
    def set_regular_movement_states(self):
        # Move left
        if self.left_pressed and not self.right_pressed:
            self.moving_x = True
            self.facing_left = True
        # Move right
        elif self.right_pressed and not self.left_pressed:
            self.moving_x = True
            self.facing_left = False
        # Don't move left or right
        else:
            self.moving_x = False
        # Jump
        # Jumping set to false when landing on a surface (check the on_top_of_surface function below)
        if self.jump_pressed:
            if not self.jump_pressed_already:  # This prevents repetitive jumping from holding down the jump button
                self.jumping = True
                self.jump_pressed_already = True
                if self.grounded:
                    self.grounded_dashing = False
        elif not self.jump_pressed:
            self.jumping = False
            self.jump_pressed_already = False

    # Create a ranged attack
    def create_ranged_attack(self):
        self.ranged_is_created = False  # Consume this value until user validly creates another
        if self.ranged_charged:
            return ChargedRanged(self.w_settings, self.rect, self.facing_left)
        else:
            return Ranged(self.w_settings, self.rect, self.facing_left)

    """ Character movement """
    def update_pos(self):  # Overrides parents (Character) update_pos function
        """
        if self.being_damaged:
            self.moving_x = False
        """
        # Beginning a dash or in dash stage 2
        if self.dash_stage_1 or self.dash_stage_2:
            self.y_velocity = 0
        # Dashing in some direction
        elif self.dashing:
            # Dashing up
            if self.dashing_up:
                self.y += self.dash_vel * -1
                self.y_velocity = self.dash_vel * -1
            # Dashing down
            elif self.dashing_down:
                self.y += self.dash_vel
                self.y_velocity = self.dash_vel
            elif self.dashing_x:
                # Dashing left
                if self.facing_left:
                    self.x += self.dash_vel * -1
                # Dashing right
                else:
                    self.x += self.dash_vel
                self.y_velocity = 0
        else:  # Regular Movement
            # Moving left
            if self.moving_x and self.facing_left:
                if self.air_dashing:
                    self.x += self.dash_vel * -1
                else:
                    self.x += self.x_vel * -1
            # Moving right
            elif self.moving_x and not self.facing_left:
                if self.air_dashing:
                    self.x += self.dash_vel
                else:
                    self.x += self.x_vel

            # Wall jump (do nothing as it is handled in check surfaces, jumping controls not allowed)
            if self.wall_jumping:
                pass
            # Dash jump
            elif self.jumping and self.grounded_dashing:
                self.y_velocity = self.w_settings.JL_init_jump_vel
                self.grounded_dashing = False  # STATE CHANGE
            # Jump
            elif self.jumping and self.grounded:
                self.y_velocity = self.w_settings.JL_init_jump_vel
            # Jump cancel
            elif not self.jumping and self.y_velocity < 0:
                self.y_velocity = 0
            # Apply y axis acceleration and speed
            self.y_velocity += self.w_settings.fall_acceleration
            self.y += self.y_velocity

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def check_surface_collisions(self, surfaces):
        super(JackLumber, self).check_surface_collisions(surfaces)
        # Move melee attack with Jack Lumber
        if self.melee is not None:
            self.melee.reposition(self.rect, self.facing_left)

    # Addition to limit dash to once per jump (infinite while on the ground)
    def on_top_of_surface(self, surface):
        super(JackLumber, self).on_top_of_surface(surface)
        self.dash_ready = True
        self.jumping = False
        self.air_dashing = False
        self.wall_jumping = False
        self.dash_to_surface_reset()

    # Bonk the bottom of a surface, kill upwards momentum
    def below_surface(self, surface):
        super(JackLumber, self).below_surface(surface)
        self.dash_to_surface_reset()

    def left_of_surface(self, surface):
        super(JackLumber, self).left_of_surface(surface)
        self.dash_to_surface_reset()
        if self.charged_melee_attacking:
            self.wall_jumping = True
            self.y_velocity = self.w_settings.JL_init_jump_vel * 1.25
            self.air_dashing = True

    def right_of_surface(self, surface):
        super(JackLumber, self).right_of_surface(surface)
        self.dash_to_surface_reset()
        if self.charged_melee_attacking:
            self.wall_jumping = True
            self.y_velocity = self.w_settings.JL_init_jump_vel * 1.25
            self.air_dashing = True

    # Cancel dash when dashing into a surface
    def dash_to_surface_reset(self):
        if self.cur_delay == self.dashing_delay:
            self.reset_cur_delay()
            self.dashing = False
            self.dashing_x = False
            self.dashing_up = False
            self.dashing_down = False
            self.y_velocity = 0

    """ Animations """
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
                self.image = self.w_settings.JL_dash_stage_2_left_image
            elif not self.facing_left:
                '''
                if self.dash_consumed:
                    if self.cur_anim != self.invincidash_stage_2_right_anim:
                        self.cur_anim.reset()
                        self.cur_anim = self.invincidash_stage_2_right_anim
                    self.image = self.cur_anim.play(self.cur_time)
                else:
                '''
                self.image = self.w_settings.JL_dash_stage_2_right_image
        # Invincidash
            '''
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
            '''
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
                self.image = self.w_settings.JL_jump_left_image
            elif not self.grounded:
                self.image = self.w_settings.JL_jump_right_image
            # Standing still
            elif self.facing_left:
                self.image = self.w_settings.JL_left_image
            else:
                self.image = self.w_settings.JL_right_image

        # Melee attack
        if self.melee is not None:
            self.melee.update_anim(self.cur_time)

    def blit_me(self, screen):
        screen.blit_obj(self)
        if self.melee is not None:
            screen.blit_obj(self.melee)

"""
Controller.py
This file contains the class Controller.  Controller boils down the functionality of any controller plugged in to a
variety of default controls needed to play this game.
"""


class Controller(object):
    def __init__(self, joystick=None):  # A dummy controller can be created with all values 0, None, or False
        # Save the controller
        self.joystick = joystick

        # Give default values to the D-pad and axes
        self.d_pad_x = 0
        self.d_pad_y = 0
        self.axis_x = 0
        self.axis_y = 0

        # Create variables for locations and values of all buttons
        self.jump_button_num = None
        self.dash_button_num = None
        self.melee_button_num = None
        self.ranged_button_num = None
        self.right_button_num = None
        self.left_button_num = None
        self.up_button_num = None
        self.down_button_num = None

        self.jump_button = False
        self.dash_button = False
        self.melee_button = False
        self.ranged_button = False
        self.right_button = False
        self.left_button = False
        self.up_button = False
        self.down_button = False

        # Create boolean variables to keep track of what our controller has
        self.has_d_pad = False
        self.has_axis = False
        self.button_d_pad = False

        # Find what controller is plugged in then give appropriate controls
        if self.joystick is not None:
            if self.joystick.get_name().find('PS4 Controller') is not -1 or self.joystick.get_name().find('Playstation 4 Controller') is not -1:
                self.PS4_Controller()
            elif self.joystick.get_name().find('Xbox 360 Controller') is not -1:
                self.Xbox_360_Controller()
            else:
                self.unknown_controller()

    # Init helper functions dependant on what controller is plugged in
    def PS4_Controller(self):
        self.button_d_pad = True
        self.has_axis = True
        self.jump_button_num = 0
        self.dash_button_num = 10
        self.melee_button_num = 2
        self.ranged_button_num = 1
        self.right_button_num = 14
        self.left_button_num = 13
        self.up_button_num = 11
        self.down_button_num = 12

    def Xbox_360_Controller(self):
        self.has_d_pad = True
        self.has_axis = True
        self.jump_button_num = 0
        self.dash_button_num = 5
        self.melee_button_num = 2
        self.ranged_button_num = 1

    def unknown_controller(self):
        # Check for directional controls
        if self.joystick.get_numhats() > 0:
            self.has_d_pad = True
        if self.joystick.get_numaxes() >= 2:
            self.has_axis = True

        # Three possible set ups depending on the number of buttons
        num_buttons = self.joystick.get_numbuttons()
        if num_buttons >= 10:  # Include directional buttons
            self.button_d_pad = True
            self.jump_button_num = 0
            self.dash_button_num = 5
            self.melee_button_num = 2
            self.ranged_button_num = 1
            self.right_button_num = 9
            self.left_button_num = 8
            self.up_button_num = 6
            self.down_button_num = 7
        elif num_buttons >= 6:  # Try to differentiate the dash button
            self.jump_button_num = 0
            self.dash_button_num = 5
            self.melee_button_num = 2
            self.ranged_button_num = 1
        elif num_buttons >= 4:  # Minimum buttons possible
            self.jump_button_num = 0
            self.dash_button_num = 3
            self.melee_button_num = 2
            self.ranged_button_num = 1

    # Setters
    def set_all_values(self):
        # Set directional variables
        if self.has_d_pad:
            self.d_pad_x, self.d_pad_y = self.joystick.get_hat(0)
        if self.has_axis:
            self.axis_x = self.joystick.get_axis(0)
            self.axis_y = self.joystick.get_axis(1)

        # Set button variables
        if self.button_d_pad:
            self.right_button = self.joystick.get_button(self.right_button_num)
            self.left_button = self.joystick.get_button(self.left_button_num)
            self.up_button = self.joystick.get_button(self.up_button_num)
            self.down_button = self.joystick.get_button(self.down_button_num)
        if self.jump_button_num is not None:
            self.jump_button = self.joystick.get_button(self.jump_button_num)
        if self.dash_button_num is not None:
            self.dash_button = self.joystick.get_button(self.dash_button_num)
        if self.melee_button_num is not None:
            self.melee_button = self.joystick.get_button(self.melee_button_num)
        if self.ranged_button_num is not None:
            self.ranged_button = self.joystick.get_button(self.ranged_button_num)

    # Getters
    def right_is_pressed(self):
        if self.d_pad_x is 1 or self.axis_x > 0.5 or self.right_button:
            return True
        return False

    def left_is_pressed(self):
        if self.d_pad_x is -1 or self.axis_x < -0.5 or self.left_button:
            return True
        return False

    def up_is_pressed(self):
        if self.d_pad_y is 1 or self.axis_y < -0.5 or self.up_button:
            return True
        return False

    def down_is_pressed(self):
        if self.d_pad_y is -1 or self.axis_y > 0.5 or self.down_button:
            return True
        return False

    def jump_is_pressed(self):
        return self.jump_button

    def dash_is_pressed(self):
        return self.dash_button

    def melee_is_pressed(self):
        return self.melee_button

    def ranged_is_pressed(self):
        return self.ranged_button

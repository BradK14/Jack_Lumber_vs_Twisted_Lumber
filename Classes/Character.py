"""
Character.py
This file contains the class Character.  Character is a parent class used to define common characterstics that all characters in the game have.
"""

from pygame.sprite import Sprite


class Character(Sprite):
    def __init__(self, w_settings, x, y, facing_left):
        super(Character, self).__init__()

        # Save passed in information
        self.w_settings = w_settings
        self.x = x
        self.y = y
        self.facing_left = facing_left

        # Initialize situational variables
        self.grounded = False  # Says whether or not a character is on top of a surface.

        # Set up speed variables
        self.y_velocity = 0

        # Dummy variables that are to be changed by child classes
        self.width = 0
        self.height = 0
        self.image = None
        self.rect = None

    # Update position
    def update_pos(self):
        self.y_velocity += self.w_settings.fall_acceleration
        self.y += self.y_velocity
        self.rect.y = int(self.y)

    # Each character will have the ability to recognize what side of a surface they collide with
    # May change the state of the character.  (Causes them to be grounded if on top of a surface)
    def check_surface_collisions(self, surfaces):
        # Keep track if we have touched any tops of surfaces
        touched_top_surface = False
        for surface in surfaces:
            if self.rect.colliderect(surface):
                # Top of a surface
                if self.rect.bottom > surface.rect.top and self.y_velocity >= self.rect.bottom - surface.rect.top:
                    touched_top_surface = True
                    self.on_top_of_surface(surface)
                # Below a surface
                elif surface.rect.bottom > self.rect.top and self.y_velocity * -1 >= surface.rect.bottom - self.rect.top:
                    self.below_surface(surface)
                # Left of a surface
                elif self.rect.right - surface.rect.left < surface.rect.right - self.rect.left:
                    self.left_of_surface(surface)
                # Right of a surface
                else:
                    self.right_of_surface(surface)

        # if we touched the tops of any surfaces then we are standing on the ground
        if touched_top_surface:
            self.grounded = True
        else:
            self.grounded = False

    # This marks the character as standing on top of a surface, kills their fall momentum, and places them on top of the surface
    def on_top_of_surface(self, surface):
        self.y = surface.rect.top - self.height
        self.y_velocity = 0
        self.rect.y = int(self.y)

    # Bonk the bottom of a surface, kill upwards momentum
    def below_surface(self, surface):
        self.y = surface.rect.bottom
        self.y_velocity = 0
        self.rect.y = int(self.y)

    # Place character to the left of a surface
    def left_of_surface(self, surface):
        self.x = surface.rect.left - self.width
        self.rect.x = int(self.x)

    # Place character to the right of a surface
    def right_of_surface(self, surface):
        self.x = surface.rect.right
        self.rect.x = int(self.x)

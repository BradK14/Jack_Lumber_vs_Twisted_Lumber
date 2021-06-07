"""
ChargedMelee.py
This file contains the class for ChargedMelee.
ChargedMelee is a sub class of the Melee class, and is different by its size, position, and damage that it deals.
"""

from Classes.Melee import Melee
from Classes.Animation import Animation


class ChargedMelee(Melee):
    def __init__(self, w_settings, jack_rect, facing_left):
        super(ChargedMelee, self).__init__(w_settings, jack_rect, facing_left)

    # Override part of the parent class constructor
    def set_up(self):
        self.width = self.w_settings.JL_charged_melee_width
        self.height = self.w_settings.JL_charged_melee_height

        self.anim = Animation(self.w_settings.JL_charged_melee_left_anim,
                              self.w_settings.JL_melee_anim_size,
                              self.w_settings.JL_melee_anim_rates,
                              self.w_settings.JL_charged_melee_right_anim)

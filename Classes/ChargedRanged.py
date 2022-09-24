"""
ChargedRanged.py
This file contains the class ChargedRanged.
ChargedRanged is the subclass of Ranged.  It is larger and does more damage than a normal ranged attack.
"""

from Classes.Ranged import Ranged
from Classes.Animation import Animation


class ChargedRanged(Ranged):
    def __init__(self, w_settings, jack_rect, facing_left):
        super(ChargedRanged, self).__init__(w_settings, jack_rect, facing_left)

    # Override part of the parent class constructor
    def set_up(self):
        self.width = self.w_settings.JL_charged_ranged_width
        self.height = self.w_settings.JL_charged_ranged_height
        self.damage = self.w_settings.JL_charged_ranged_damage

        self.anim = Animation(self.w_settings.JL_charged_ranged_left_anim,
                              self.w_settings.JL_ranged_anim_size,
                              self.w_settings.JL_ranged_anim_rates,
                              self.w_settings.JL_charged_ranged_right_anim)

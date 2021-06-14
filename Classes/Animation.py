"""
Animation.py
This file holds the class Animation.  Animation offers the user an easy way to implement animations.
"""


class Animation(object):
    def __init__(self, anim, anim_size, anim_rates, right_anim=None):
        self.anim = anim
        self.anim_size = anim_size
        self.next_anim = anim_rates
        self.right_anim = right_anim

        self.cur_index = 0
        self.last_anim = 0

        self.currently_playing = False

    # General needs of any type of animation playing, called internally by all play functions
    def play_set_up(self, cur_time):
        if not self.currently_playing:
            self.currently_playing = True
            self.last_anim = cur_time
            self.cur_index = 0
        if cur_time - self.last_anim > self.next_anim[self.cur_index]:
            self.last_anim = cur_time
            self.cur_index += 1

    # Begin or continue animation
    def play(self, cur_time):
        self.play_set_up(cur_time)
        if self.cur_index >= self.anim_size:
            self.cur_index = 0
        return self.anim[self.cur_index]

    # Begin or continue animation that can swap between two different directions mid animation
    def play_var_dir(self, cur_time, facing_left):
        self.play_set_up(cur_time)
        if self.cur_index >= self.anim_size:
            self.cur_index = 0
        if facing_left:
            return self.anim[self.cur_index]
        else:
            return self.right_anim[self.cur_index]

    # Plays animation once and freezes on last picture
    def play_once(self, cur_time):
        self.play_set_up(cur_time)
        if self.cur_index >= self.anim_size:
            self.cur_index -= 1  # The only difference from play is this line
        return self.anim[self.cur_index]

    # Plays animation once and can swap between two directions
    def play_once_var_dir(self, cur_time, facing_left):
        self.play_set_up(cur_time)
        if self.cur_index >= self.anim_size:
            self.cur_index -= 1
        if facing_left:
            return self.anim[self.cur_index]
        else:
            return self.right_anim[self.cur_index]

    # Resets the animation to the start
    def reset(self):
        self.currently_playing = False

"""
Delay.py
This file holds the class Delay.  Delay is used to keep track of any unique delays used in the game (not animations)
"""


class Delay(object):
    def __init__(self, delay_length):
        self.delay_length = delay_length

        self.started = False
        self.start_time = 0

    def begin(self, cur_time):
        if not self.started:
            self.started = True
            self.start_time = cur_time

    # Will return True as long as the delay is active, then False when the target time is reached (self.delay_length)
    def is_active(self, cur_time):
        if not self.started:
            return False
        if cur_time - self.start_time > self.delay_length:
            return False
        return True

    def reset(self):
        self.started = False

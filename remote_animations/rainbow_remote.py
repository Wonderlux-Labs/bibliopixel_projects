import random
import time
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from base_remote_strip import BaseRemoteStrip
from base_remote_strip import MidiTransform
from base_remote_strip import NumberUtils
from base_remote_strip import ColorMidiUtils
from bibliopixel import colors as bp_colors

class RainbowRemote(BaseRemoteStrip):
    """Generate rainbow wheel equally distributed over strip."""

    def __init__(self, layout, start=0, end=-1, **args):
        super(RainbowRemote, self).__init__(layout, start, end, **args)

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        for i in range(self._size):
            chunk_size = MidiTransform.remap_cc_value(self.count_control, 1, 20)
            chunks = self._size / chunk_size
            c = bp_colors.hue_helper(i + self.color_control, chunks, self._step)
            c_lev = MidiTransform.remap_cc_value(self.brightness_control, 0, 256)
            c = bp_colors.color_scale(c, c_lev)
            self.layout.set(self._start + i, c)

        self._step += amt
        overflow = self._step - 256
        if overflow >= 0:
            self._step = overflow

        delay_time = MidiTransform.remap_cc_value(self.delay_control, 0, 1)
        time.sleep(delay_time)

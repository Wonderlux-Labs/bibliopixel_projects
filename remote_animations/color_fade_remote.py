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

class ColorFadeRemote(BaseRemoteStrip):
    """Fill the dots progressively along the strip."""

    def wave_range(self, start, peak, step):
        main = [i for i in range(start, peak + 1, step)]
        return main + [i for i in reversed(main[0:len(main) - 1])]

    def __init__(self, layout, start=0, end=-1, **args):
        super(ColorFadeRemote, self).__init__(layout, start, end, **args)
        self._colors = [bp_colors.Red]
        self._levels = self.wave_range(200, 255, 25)
        self._level_count = len(self._levels)
        self._color_count = len(self._colors)

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        num_colors = int(MidiTransform.remap_cc_value(self.color_control, 1, 10))
        hue = int(MidiTransform.remap_cc_value(self.color_control, 1, 255))

        levels_count = int(MidiTransform.remap_cc_value(self.width_control, 5, 25))
        self._levels = self.wave_range(30, 255, levels_count)

        if num_colors > 1:
            hues = bp_colors.hue_gradient(0, hue, num_colors)
        else:
            hues = [hue]

        self._colors = list(map(lambda x: bp_colors.hue2rgb(x), hues))

        self._level_count = len(self._levels)
        self._color_count = len(self._colors)

        if self._step > self._level_count * self._color_count:
            self._step = 0

        c_index = (self._step // self._level_count) % self._color_count
        l_index = (self._step % self._level_count)

        color = self._colors[c_index]

        self.layout.fill(bp_colors.color_scale(color, self._levels[l_index]), self._start, self._end)

        self._step += amt

        delay_time = MidiTransform.remap_cc_value(self.delay_control, 0, 1)
        time.sleep(delay_time)

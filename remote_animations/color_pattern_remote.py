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

class ColorPatternRemote(BaseRemoteStrip):
    """Fill the dots progressively along the strip with alternating colors."""

    def __init__(self, layout, colors=[bp_colors.Red, bp_colors.Green, bp_colors.Blue],
                 width=1, dir=True):
        super(ColorPatternRemote, self).__init__(layout)
        self._colors = colors
        self._color_count = len(colors)
        self._width = width
        self._total_width = self._width * self._color_count
        self._dir = dir

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        num_colors = int(MidiTransform.remap_cc_value(self.count_control, 1, 10))
        hue = int(MidiTransform.remap_cc_value(self.color_control, 1, 255))
        self._width = int(MidiTransform.remap_cc_value(self.width_control, 1, 100))

        if num_colors > 1:
            hues = bp_colors.hue_gradient(hue, 255, num_colors)
        else:
            hues = [hue]

        self._colors = list(map(lambda x: bp_colors.hue2rgb(x), hues))
        self._color_count = len(self._colors)
        self._total_width = self._width * self._color_count

        for i in range(self._size):
            cIndex = ((i + self._step) % self._total_width) // self._width
            self.layout.set(i, self._colors[cIndex])
        self._step += amt * (1 if self._dir else -1)
        if self._dir and self._step >= self.layout.numLEDs:
            self._step = 0
        elif not self._dir and self._step < 0:
            self._step = self.layout.numLEDs - 1

        delay_time = MidiTransform.remap_cc_value(self.delay_control, 0, 1)
        time.sleep(delay_time)

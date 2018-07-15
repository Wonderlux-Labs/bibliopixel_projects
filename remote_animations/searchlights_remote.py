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

class SearchlightsRemote(BaseRemoteStrip):
    def __init__(self, layout, colors=[bp_colors.MediumSeaGreen, bp_colors.MediumPurple, bp_colors.MediumVioletRed], tail=2, start=0, end=-1):

        super(SearchlightsRemote, self).__init__(layout, start, end)

        self._colors = colors
        self._tail = tail + 1
        if self._tail >= self._size // 2:
            self._tail = (self._size // 2) - 1

    def pre_run(self):
        self._direction = [1, 1, 1]
        self._currentpos = [0, 0, 0]
        self._steps = [1, 1, 1]
        self._fadeAmt = 256 / self._tail

    def step(self, amt=1):
        self._tail = int(MidiTransform.remap_cc_value(self.count_control, 1, 50))
        self.get_color()
        hue = int( 255 * bp_colors.conversions.rgb_to_hsv(self._color)[0])
        hues = bp_colors.hue_gradient(hue, 255-hue, 3)
        self._colors = list(map(lambda x: bp_colors.hue2rgb(x), hues))
        self._ledcolors = [(0, 0, 0) for i in range(self._size)]
        self.layout.all_off()

        for i in range(0, 3):
            self._currentpos[i] = self._start + self._steps[i]

            # average the colors together so they blend
            self._ledcolors[self._currentpos[i]] = list(map(lambda x, y: (x + y) // 2, self._colors[i], self._ledcolors[self._currentpos[i]]))
            for j in range(1, self._tail):
                if self._currentpos[i] - j >= 0:
                    self._ledcolors[self._currentpos[i] - j] = list(map(lambda x, y: (x + y) // 2, self._ledcolors[self._currentpos[i] - j], bp_colors.color_scale(self._colors[i], 255 - (self._fadeAmt * j))))
                if self._currentpos[i] + j < self._size:
                    self._ledcolors[self._currentpos[i] + j] = list(map(lambda x, y: (x + y) // 2, self._ledcolors[self._currentpos[i] + j], bp_colors.color_scale(self._colors[i], 255 - (self._fadeAmt * j))))
            if self._start + self._steps[i] >= self._end:
                self._direction[i] = -1
            elif self._start + self._steps[i] <= 0:
                self._direction[i] = 1

            # advance each searchlight at a slightly different speed
            self._steps[i] += self._direction[i] * amt * int(random.random() > (i * 0.05))

        for i, thiscolor in enumerate(self._ledcolors):
            self.layout.set(i, thiscolor)

        delay_time = MidiTransform.remap_cc_value(self.delay_control, 0, 1)
        time.sleep(delay_time)

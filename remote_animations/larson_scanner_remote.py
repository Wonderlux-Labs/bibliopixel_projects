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

class LarsonScannerRemote(BaseRemoteStrip):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.)."""

    def __init__(self, layout, start=0, end=-1, **args):
        super(LarsonScannerRemote, self).__init__(layout, start, end, **args)
        self._min_tail = args.get('min_tail') or 2
        self._max_tail = args.get('max_tail') or 50
        self._max_randomness = args.get('max_randomness') or 100
        self._color = (255,255,255)
        self._random_color = (255,255,255)

    def pre_run(self):
        self._direction = -1
        self._last = 0
        self._step = 0
        self._random_counter = 0
        self._random_seed = 0

    def get_color(self):
        print('here')
        if self.use_rgb:
            self._color = ColorMidiUtils.three_cc_to_color(self.red_control, self.green_control, self.blue_control)

        if self._random_counter == 0:
            self._random_seed = (self.color_control + random.randint(0, self._randomness)) % 127

        color = ColorMidiUtils.one_cc_to_color(self._random_seed)
        c_lev = MidiTransform.remap_cc_value(self.brightness_control, 0, 256)

        self._color = bp_colors.color_scale(color, c_lev)


    def step(self, amt=1):
        self.layout.all_off()

        self._randomness = int(MidiTransform.remap_cc_value(self.randomness_control, 0, self._max_randomness))

        scaled_tail = int(MidiTransform.remap_cc_value(self.count_control, self._min_tail, self._max_tail))
        self._tail = scaled_tail

        scaled_fade = int(MidiTransform.remap_cc_value(self.utility_control_two, 1, 500))
        self._fadeAmt = scaled_fade // self._tail
        print('calling color')
        self.get_color()
        print('color is')
        print(self._color)

        self._last = self._start + self._step
        self.layout.set(self._last, self._color)

        for i in range(self._tail):
            self.layout.set(self._last - i, bp_colors.color_scale(self._color, 255 - (self._fadeAmt * i)))
            self.layout.set(self._last + i, bp_colors.color_scale(self._color, 255 - (self._fadeAmt * i)))

        if self._start + self._step >= self._end:
            self._direction = -self._direction
        elif self._step <= 0:
            self._direction = -self._direction

        self._step += self._direction * amt

        delay_time = MidiTransform.remap_cc_value(self.delay_control, 0, 1)
        time.sleep(delay_time)
        self._random_counter = (self._random_counter + 1) % 30

class LarsonRainbowRemote(LarsonScannerRemote):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow."""

    def __init__(self, layout, start=0, end=-1):
        super(LarsonRainbowRemote, self).__init__(layout, start, end)
        self._color_number = 0

    def get_color(self):
        color_seed = MidiTransform.remap_cc_value(self.color_control, 0, 10)
        amount_change = MidiTransform.remap_cc_value(self.utility_control_one, 0.1, 5)
        if amount_change == 5:
            amount_change = 0

        base_color = (self._color_number + color_seed) % 359
        self._color_number = (base_color + amount_change) % 359

        color = bp_colors.hue2rgb_360(self._color_number)
        c_lev = MidiTransform.remap_cc_value(self.brightness_control, 0, 256)

        self._color = bp_colors.color_scale(color, c_lev)

    def step(self, amt=1):
        super(LarsonRainbowRemote, self).step(amt)

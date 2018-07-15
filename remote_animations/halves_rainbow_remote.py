import random
import time
import os
import sys
import math

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from base_remote_strip import BaseRemoteStrip
from base_remote_strip import MidiTransform
from base_remote_strip import NumberUtils
from base_remote_strip import ColorMidiUtils
from bibliopixel import colors as bp_colors


class HalvesRainbowRemote(BaseRemoteStrip):

    def __init__(self, layout, start=0, end=-1, centre_out=True, rainbow_inc=4, **args):
        super(HalvesRainbowRemote, self).__init__(layout, start, end, **args)
        self._minLed = 0
        self._maxLed = end
        if self._maxLed < 0 or self._maxLed < self._minLed:
            self._maxLed = self.layout.numLEDs - 1
        self._positive = True
        self._step = 0
        self._centerOut = centre_out
        self._rainbowInc = rainbow_inc

    def pre_run(self):
        self._current = 0
        self._step = 0

    def step(self, amt=1):

        center = float(self._maxLed) / 2
        center_floor = math.floor(center)
        center_ceil = math.ceil(center)

        if self._centerOut:
            self.layout.fill(
                bp_colors.hue2rgb(self._step), int(center_floor - self._current), int(center_floor - self._current))
            self.layout.fill(
                bp_colors.hue2rgb(self._step), int(center_ceil + self._current), int(center_ceil + self._current))
        else:
            self.layout.fill(
                bp_colors.hue2rgb(self._step), int(self._current), int(self._current))
            self.layout.fill(
                bp_colors.hue2rgb(self._step), int(self._maxLed - self._current), int(self._maxLed - self._current))

        if self._step == len(bp_colors.conversions.HUE_RAINBOW) - 1:
            self._step = 0
        else:
            self._step += amt + self._rainbowInc
            if self._step > len(bp_colors.conversions.HUE_RAINBOW) - 1:
                self._step = 0

        if self._current == center_floor:
            self._current = self._minLed
        else:
            self._current += amt

        delay_time = MidiTransform.remap_cc_value(self.delay_control, 0, 1)
        time.sleep(delay_time)
